import Pyro4
import sys, traceback, time, os, logging
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from subprocess import Popen
from Backend.Loader import Loader
import pexpect
import platform
@Pyro4.expose
class Pyro_Run():
    loader = None
    def __init__(self):
        self.loader = Loader.Loader()


    def load_workspace(self, file):
        return self.loader.loadworkspace(file)

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


    def createPackets(self,fileName):
        # projectPath = " PCAP/PCAPServices.py"
        # if platform.system() == 'Darwin':
        projectPath = "src/main/python/Backend/PCAP/PCAPServices.py"
        self.child = pexpect.spawn("python3.6 " + projectPath,encoding='utf-8')
        self.child.expect("loop",timeout=None)
        print("Creating")
        self.child.sendline("create " + fileName)
        self.child.expect("Done",timeout=None)

    def savePackets(self):
        print("saving")
        self.child.sendline("save")
        self.child.expect("saved",timeout=None)

    def dissectPackets(self):
        print("dissecting")
        self.child.sendline("dissect")
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
