'''
Authors:
    Practicum Team
'''
import Pyro4
import sys, traceback, time, os, logging
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from subprocess import Popen
from Backend.Loader import Loader
import platform
if platform.system() == "Windows": #IMPORT WINPEXPECT OR PEXPECT DEPENDING ON OS
    import winpexpect
else:
    import pexpect

@Pyro4.expose
class Pyro_Run():
    '''
    This class is in charge of handling communication between UI and backend.

    Attributes;
        loader : instance of the Loader class
        workspace_file : path to the current loaded workspace
        selected_project : name of the currently selected project
    '''
    loader = None
    workspace_file = None
    selected_project = None
    def __init__(self):
        self.loader = Loader.Loader()

    def set_workspace(self,workspace = None ,selected_project = None):
        '''
        Sets the currently open workspace
        Args:
            workspace : path to workspace file
            selected_project : name of selected project
        Yields:
            workspace file set and selected project set
        '''
        #workspace set
        if workspace != None:
            self.workspace_file = workspace
        #workspace not setalready
        else:
            self.workspace_file = self.get_current_workspace()['path']
        self.selected_project = selected_project
        print("project changed to {}/{}".format(self.workspace_file,self.selected_project))
        return self.workspace_file,self.selected_project

    def load_workspace(self, file):
        '''
        Load workspace. Calls Loader -> load_workspace

        Args:
            file : path of workspace to be loaded
        '''
        return self.loader.load_workspace(file)

    def get_current_workspace(self):
        '''
        Get the currently open workspace.

        Yields:
            workspace as a json
        '''
        return self.loader.workspace.JSON

    def new_workspace(self,ws_name,ws_created,ws_edited):
        '''
        Create a new workspace. calls Loader -> new_workspace
        '''
        return self.loader.new_workspace(ws_name,ws_created,ws_edited)

    def save_workspace(self):
        '''
        Save the workspace. calls Loader -> save_workspace
        '''
        return self.loader.save_workspace()

    def close_workspace(self):
        '''
        Close a workspace. calls Loader -> close_workspace
        '''
        return self.loader.close_workspace()

    def import_project(self,file):
        '''
        Import project. calls loader -> import project
        '''
        return self.loader.import_project(file)

    def new_project(self,name,author,desc,created,edited , protocol, change_protocol, src_port, dst_port):
        '''
        Create a new project. Calls Loader-> new_project
        '''
        return self.loader.new_project(name,author,desc,created,edited,protocol,change_protocol,src_port,dst_port)

    def export_lua_script(self,workspace,project):
        '''
        Export a lua script for the current project. calls Loader -> export_lua_script
        '''
        self.loader.export_lua_script(workspace,project)

    def save_dissector_attributes(self,dissector,workspace,project):
        '''
        Save dissector attributes. call Loader->save_dissector_attributes
        '''
        self.loader.save_dissector_attributes(dissector,workspace,project)

    def get_dissector_attributes(self,workspace,project):
        '''
        Get dissector attributes. call Loader->get_dissector_attributes
        '''
        return self.loader.get_dissector_attributes(workspace,project)

    def createPackets(self,fileName):
        '''
        Create PCAP packets. delegate work to PCAP Services

        Args:
            filename : path to pcap file
        '''
        # projectPath = " PCAP/PCAPServices.py"
        # if platform.system() == 'Darwin':
        try:
            varSize= os.path.getsize(fileName)
        except Exception as e:
            print("File doesnt exist! ")
            return
        #pcap file too big to handle
        if(varSize >= 50e7):
            print("File size is huge,(" + str(varSize/1e6) + " MB) want to proceed?[Y/N]")
            answer = input()
            if(not answer) or (answer.lower()[0] != 'y'):
                return
        # projectPath = "src/main/python/Backend/PCAP/PCAPServices.py"
        projectPath="PCAPServices.py"
        #spawn a new process using the right library for the OS
        if platform.system() == "Windows":
            self.child = winpexpect.winspawn("python " + projectPath)
            print("created - w " )
        else:
            self.child = pexpect.spawn("python3.6 " + projectPath,encoding='utf-8')
            print("created")
        self.child.expect("loop")
        print("Creating")
        print(fileName + " file name")
        #Send signal to pcapservices
        self.child.sendline("create " + fileName)
        self.child.expect("Done")

    def savePackets(self):
        '''
        Save the PCAP packets
        '''
        print("saving")
        self.child.sendline("save")
        self.child.expect("saved")

    def dissectPackets(self):
        '''
        Send the signal to dissect packets
        '''
        print("dissecting")
        print(self.workspace_file)
        print(self.selected_project)
        self.child.sendline("dissect {} {}".format(self.workspace_file,self.selected_project))

        print(self.child.read())

    def colorCode(self):
        '''
        Send the signal to apply packet color coding
        '''
        print("Coloring")
        self.child.sendline("colorcode")
        self.child.expect("colored")

    def printPackets(self):
        '''
        Send the signal to print packets
        '''
        print("print")
        self.child.sendline("print")
        if platform.system() == "Windows": #IMPORT WINPEXPECT OR PEXPECT DEPENDING ON OS
            self.child.expect(winpexpect.EOF, timeout=600000)
        print(self.child.read())

    def main(self):
        '''
        main function of the pyro service
        '''
        #start pyro
        daemon = Pyro4.Daemon()
        Popen("pyro4-ns")
        time.sleep(5)
        ns = Pyro4.locateNS()
        #register namespace
        uri = daemon.register(Pyro_Run)
        ns.register("pyro.service",uri)
        print("[+] Pyro4 URI: " + str(uri))
        daemon.requestLoop()


if __name__ == "__main__":
    main()
