import Pyro4
import sys, traceback, time, os, logging
sys.path.insert(1, "./")
sys.path.insert(1, "../../")
from subprocess import Popen
from Loader import Loader

@Pyro4.expose
class Pyro_Run():
    loader = None

    def __init__(self):
        self.loader = Loader.Loader()

    def parse_XML_to_workspace(self,file):
        self.loader.parsexmltoworkspace(file)

    def load_workspace(self, file):
        return self.loader.loadworkspace(file)

    def load_empty_worspace(self):
        return self.loader.runWithUnsavedWorkspace()

    def get_workspace_pool_count(self):
        return self.loader.get_workspace_pool_count()

    def get_workspace_data_from_pool(self, wsname):
        return self.loader.get_workspace_data_from_pool(wsname)

    def update_workspace_name(self, ws_currentname, ws_newname):
        self.loader.update_workspace(ws_currentname, ws_newname)

def main():
    daemon = Pyro4.Daemon()
    Popen("pyro4-ns")
    time.sleep(8)
    ns = Pyro4.locateNS()
    uri = daemon.register(Pyro_Run)
    ns.register("pyro.service",uri)
    print("[+] Pyro4 URI: " + str(uri))
    daemon.requestLoop()

if __name__ == "__main__":
    main()