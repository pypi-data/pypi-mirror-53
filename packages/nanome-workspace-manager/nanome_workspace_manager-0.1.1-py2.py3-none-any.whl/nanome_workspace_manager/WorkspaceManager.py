import nanome
from nanome.api.ui import LayoutNode
from nanome.util import Logs
from nanome.util.enums import NotificationTypes
from nanome._internal._network._serialization import _ContextSerialization, _ContextDeserialization
from nanome._internal._structure._serialization import _WorkspaceSerializer, _AtomSerializer
from nanome._internal._util._serializers import _DictionarySerializer, _StringSerializer, _ByteSerializer, _TypeSerializer, _LongSerializer

import struct
import sys
import os
import zlib
import traceback
from timeit import default_timer as timer
from hashlib import md5
import re

# This plugin uses undocumented network code, in order to reuse already available serialization code

MENU_PATH = os.path.join(os.path.dirname(__file__), 'menu.json')

DIR = os.path.expanduser('~/Documents/nanome-workspace-manager')
AUTH_PATH = os.path.join(DIR, 'accounts.txt')

WORKSPACE_DIR = os.path.join(DIR, 'workspaces')
if not os.path.exists(WORKSPACE_DIR):
    os.makedirs(WORKSPACE_DIR)

md5re = re.compile("^[a-f0-9]{32}$")

workspace_serializer = _WorkspaceSerializer()
dictionary_serializer = _DictionarySerializer()
dictionary_serializer.set_types(_StringSerializer(), _ByteSerializer())
atom_dictionary_serializer = _DictionarySerializer()
atom_dictionary_serializer.set_types(_LongSerializer(), _AtomSerializer())

class WorkspaceManager(nanome.PluginInstance):

    ###################################
    ### Save + Load Logic
    ###################################

    def open_file_for_save(self, name):
        file_path = os.path.join(WORKSPACE_DIR, name)
        if os.path.exists(file_path):
            self.send_notification(NotificationTypes.error, "Workspace name already exists")
            self.btn_save.unusable = False
            self.update_content(self.btn_save)
            return

        file = open(file_path, "wb")
        def workspace_received(workspace):
            try:
                self.save_workspace(workspace, file)
            except:
                self.send_notification(NotificationTypes.error, "Failed to save workspace, check plugin")
                Logs.error("Failed to save workspace", traceback.format_exc())
            self.btn_save.unusable = False
            self.update_content(self.btn_save)
            file.close()
            self.refresh_menu()
            self.__timer = timer()

        self.request_workspace(workspace_received)

    def save_workspace(self, workspace, file):
        context = _ContextSerialization(0, _TypeSerializer.get_version_table())
        context.write_uint(0) # Version
        context.write_using_serializer(dictionary_serializer, _TypeSerializer.get_version_table())
        subcontext = context.create_sub_context()
        subcontext.payload["Atom"] = {}
        subcontext.write_using_serializer(workspace_serializer, workspace)
        context.write_using_serializer(atom_dictionary_serializer, subcontext.payload["Atom"])
        context.write_bytes(subcontext.to_array())

        to_write = context.to_array()
        compressed_data = zlib.compress(to_write)
        file.write(compressed_data)

        self.send_notification(NotificationTypes.success, "Workspace saved")

    def open_file_for_load(self, name):
        file_path = os.path.join(WORKSPACE_DIR, name)
        try:
            file = open(file_path, "rb")
        except:
            self.send_notification(NotificationTypes.error, "Couldn't open workspace")
            return

        data = file.read()
        file.close()
        try:
            decompressed_data = zlib.decompress(data)
            self.load_workspace(decompressed_data)
        except:
            self.send_notification(NotificationTypes.error, "Failed to load workspace, check plugin")
            Logs.error("Failed to load workspace", traceback.format_exc())

    def load_workspace(self, data):
        context = _ContextDeserialization(data, _TypeSerializer.get_version_table())
        context.read_uint()
        file_version_table = context.read_using_serializer(dictionary_serializer)
        version_table = _TypeSerializer.get_best_version_table(file_version_table)

        context = _ContextDeserialization(data, version_table)
        context.read_uint()
        context.read_using_serializer(dictionary_serializer)
        context.payload["Atom"] = context.read_using_serializer(atom_dictionary_serializer)
        workspace = context.read_using_serializer(workspace_serializer)

        self.update_workspace(workspace)

        self.send_notification(NotificationTypes.success, "Workspace loaded")

    ###################################
    ### UI
    ###################################

    def create_menu(self):
        self.menu = nanome.ui.Menu.io.from_json(MENU_PATH)
        menu = self.menu

        # pages + prefabs
        self.pg_auth = menu.root.find_node('AuthPage')
        self.pg_main = menu.root.find_node('MainPage')
        self.pfb_item = menu.root.find_node('ItemPrefab')

        self.pg_auth.enabled = self.__class__.enable_accounts
        self.pg_main.enabled = not self.__class__.enable_accounts

        # auth elements
        self.in_user = self.pg_auth.find_node('Username').get_content()
        self.in_pass = self.pg_auth.find_node('Password').get_content()
        self.btn_auth = self.pg_auth.find_node('Enter').get_content()
        self.btn_auth.register_pressed_callback(self.auth_callback)

        # main elements
        self.ls_workspaces = self.pg_main.find_node('List').get_content()
        self.in_name = self.pg_main.find_node('Name').get_content()
        self.btn_save = self.pg_main.find_node('Save').get_content()
        self.btn_save.register_pressed_callback(self.save_callback)

        self.update_menu(menu)

    def refresh_menu(self):
        if self.__class__.enable_accounts and self.user == None:
            return

        files = self.get_workspaces()
        file_names = set(map(lambda item: item.name, self.ls_workspaces.items))
        add_set = set(files)
        remove_files = file_names - add_set
        changed = False

        for file_name in remove_files:
            item_to_delete = None
            for item in self.ls_workspaces.items:
                if item.name == file_name:
                    item_to_delete = item
                    break
            if item_to_delete != None:
                self.ls_workspaces.items.remove(item_to_delete)
            changed = True

        add_files = add_set - file_names
        for file_name in add_files:
            new_item = self.pfb_item.clone()
            new_item.name = file_name
            label = new_item.find_node("Label").get_content()
            load = new_item.get_content()
            delete = new_item.find_node("Delete").get_content()
            changed = True

            if self.__class__.enable_accounts and not self.admin:
                label.text_value = file_name.split(' - ', 1)[1]
            else:
                label.text_value = file_name

            load.workspace = file_name
            delete.workspace = file_name
            load.register_pressed_callback(self.load_callback)
            delete.register_pressed_callback(self.delete_callback)

            self.ls_workspaces.items.append(new_item)

        if changed:
            self.update_content(self.ls_workspaces)

    def display_menu(self):
        self.menu.enabled = True
        self.update_menu(self.menu)

    ###################################
    ### Base Logic
    ###################################

    def start(self):
        self.user = None
        self.admin = False
        
        self.load_accounts()
        self.create_menu()
        self.__timer = timer()

    def on_run(self):
        self.display_menu()

    def update(self):
        if timer() - self.__timer >= 5.0:
            self.load_accounts()
            self.refresh_menu()
            self.__timer = timer()

    def load_accounts(self):
        if not self.__class__.enable_accounts:
            return

        try:
            with open(AUTH_PATH, 'r') as f:
                self.accounts = []
                for line in f.readlines():
                    account = line.rstrip().split(' ')
                    if len(account) != 3:
                        Logs.warning('Invalid account entry: \n' + line)
                        continue
                    self.accounts.append(account)
        except:
            # create default accounts file if none exists
            self.accounts = [['admin', 'admin', '1']]

        changed = False
        for account in self.accounts:
            if not md5re.match(account[1]):
                # password isn't hashed, hash it
                account[1] = md5(account[1].encode()).hexdigest()
                changed = True

        if changed:
            self.save_accounts()

    def save_accounts(self):
        with open(AUTH_PATH, 'w') as f:
            f.writelines('%s\n' % ' '.join(account) for account in self.accounts)

    def clean_filename(self, filename):
        # only allow filename to contain alphanum, "-", "_", and " "
        return re.sub('[^a-zA-Z0-9-_ ]', '', filename)

    def get_workspaces(self):
        files = [filename for filename in os.listdir(WORKSPACE_DIR)]
        if self.__class__.enable_accounts and not self.admin:
            files = list(filter(lambda f: f.split(' - ')[0] == self.user, files))
        return files

    ###################################
    ### Button Callbacks
    ###################################

    def auth_callback(self, button):
        username = self.in_user.input_text
        password = md5(self.in_pass.input_text.encode()).hexdigest()

        for account in self.accounts:
            if username == account[0] and password == account[1]:
                self.user = username
                self.admin = account[2] == '1'
                break

        if self.user:
            self.send_notification(NotificationTypes.success, "Welcome " + username)
            self.pg_auth.enabled = False
            self.pg_main.enabled = True
            self.refresh_menu()
            self.display_menu()
        else:
            self.send_notification(NotificationTypes.error, "Invalid login")

    def save_callback(self, button):
        name = self.clean_filename(self.in_name.input_text.strip())
        if name == '':
            self.send_notification(NotificationTypes.error, "Workspace name cannot be empty")
            return

        if self.__class__.enable_accounts:
            name = self.user + ' - ' + name

        self.btn_save.unusable = True
        self.update_content(self.btn_save)
        self.open_file_for_save(name)

    def load_callback(self, button):
        self.open_file_for_load(button.workspace)

    def delete_callback(self, button):
        try:
            os.remove(os.path.join(WORKSPACE_DIR, button.workspace))
        except:
            pass
        self.refresh_menu()
        self.__timer = timer()

class WorkspaceManagerAccounts(WorkspaceManager):
    enable_accounts = True
class WorkspaceManagerNoAccounts(WorkspaceManager):
    enable_accounts = False

def main():
    enable_accounts = True
    try:
        for i in range(len(sys.argv)):
            if sys.argv[i] in ["-d", "--disable-accounts"]:
                enable_accounts = False
    except:
        pass

    plugin_class = WorkspaceManagerAccounts if enable_accounts else WorkspaceManagerNoAccounts

    # Plugin
    plugin = nanome.Plugin("Workspace Manager", "Allows standalone VR headset to save and load workspaces", "Loading", False)
    plugin.set_plugin_class(plugin_class)
    plugin.run('127.0.0.1', 8888)

if __name__ == "__main__":
    main()
