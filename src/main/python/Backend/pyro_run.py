import Pyro4
import sys, traceback, time, os, logging
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from subprocess import Popen
from Backend.Loader import Loader
import platform

if platform.system() == "Windows":
    import winpexpect
else:
    import pexpect
@Pyro4.expose
class Pyro_Run():
    loader = None
    workspace_file = None
    selected_project = None
    def __init__(self):
        self.loader = Loader.Loader()
    

    def set_workspace(self,workspace = None ,selected_project = None):
        if workspace != None:
            self.workspace_file = workspace
        else:
            self.workspace_file = self.get_current_workspace()['path']
        
        self.selected_project = selected_project
        print("project changed to {}/{}".format(self.workspace_file,self.selected_project))
        return self.workspace_file,self.selected_project

    def load_workspace(self, file):
        return self.loader.load_workspace(file)

    def get_current_workspace(self):
        return self.loader.workspace.JSON

    def new_workspace(self,ws_name,ws_created,ws_edited):
        return self.loader.new_workspace(ws_name,ws_created,ws_edited)

    def save_workspace(self):
        return self.loader.save_workspace()

    def close_workspace(self):
        return self.loader.close_workspace()

    def import_project(self,file):
        return self.loader.import_project(file)

    def new_project(self,name,author,desc,created,edited , protocol, change_protocol, src_port, dst_port):
        return self.loader.new_project(name,author,desc,created,edited,protocol,change_protocol,src_port,dst_port)

    def export_lua_script(self,workspace,project):
        self.loader.export_lua_script(workspace,project)

    def save_dissector_attributes(self,dissector,workspace,project):
        self.loader.save_dissector_attributes(dissector,workspace,project)

    def get_dissector_attributes(self,workspace,project):
        return self.loader.get_dissector_attributes(workspace,project)

    def createPackets(self,fileName):
        # projectPath = " PCAP/PCAPServices.py"
        # if platform.system() == 'Darwin':
        try:
            varSize= os.path.getsize(fileName)
        except Exception as e:
            print("File doesnt exist! ")
            return
        if(varSize >= 50e7):
            print("File size is huge,(" + str(varSize/1e6) + " MB) want to proceed?[Y/N]")
            answer = input()
            if(not answer) or (answer.lower()[0] != 'y'):
                return
        projectPath = "src/main/python/Backend/PCAP/PCAPServices.py"
        if platform.system() == "Windows":
            self.child = winpexpect.winspawn("python " + projectPath)
            print("created - w " )
        else:
            self.child = pexpect.spawn("python3.6 " + projectPath,encoding='utf-8')
            print("created")
        self.child.expect("loop")
        print("Creating")
        print(fileName + " file name")
        self.child.sendline("create " + fileName)
        self.child.expect("Done")

    def savePackets(self):
        print("saving")
        self.child.sendline("save")
        self.child.expect("saved")

    def dissectPackets(self):
        print("dissecting")
        print(self.workspace_file)
        print(self.selected_project)
        self.child.sendline("dissect {} {}".format(self.workspace_file,self.selected_project))
        
        print(self.child.read())

    def colorCode(self):
        print("Coloring")
        self.child.sendline("colorcode")
        self.child.expect("colored")

    def printPackets(self):
        self.child.sendline("print")
        print(self.child.read())

 
    

    def main(self):
        daemon = Pyro4.Daemon()
        Popen("pyro4-ns")
        time.sleep(5)
        ns = Pyro4.locateNS()
        uri = daemon.register(Pyro_Run)
        ns.register("pyro.service",uri)
        print("[+] Pyro4 URI: " + str(uri))
        daemon.requestLoop()


if __name__ == "__main__":
    main()
