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
    
  


def main():
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