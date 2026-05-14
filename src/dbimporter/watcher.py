import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import numpy as np

from dbimporter.check_structure import Check


class Watcher:

    """
        Watches the specified directory for new files
    """

    def __init__(self, 
                 watch_path: Path,
                 checkopts: None):


        self.watch_path = watch_path
        self.checkopts = checkopts
        self.observer = Observer()



    def run(self):

        """
            Start running the handler that will look for incoming files
        """

        event_handler = Handler(self.checkopts)
        self.watch_path = self.watch_path
        self.observer.schedule(event_handler, self.watch_path, recursive = True)
        self.observer.start()

        try:
            while True:
                time.sleep(5)
                print("waiting for file...")
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    """
        Decide what to do when certain events are detected in the watched directory
    """

    def __init__(self,
                 checkopts): 
        
        self.checkopts = checkopts


    def on_any_event(self,event):

        if event.is_directory:

            return None

        if event.event_type == 'created':

            print("Watchdog received created event - % s." % event.src_path)

        elif event.event_type == 'modified':

            print("Watchdog received modified event - % s." % event.src_path)

            
            event_decider(event)
            

def event_decider(event):

    """
        Attempts to check file when it is detected and able to be read

        Parameters
        ----------

            event : 
                Details of the watchdog event that has been detected 
    """

    print("Attempting to open file...")

    try:
        Check(filename=event.src_path, automatic_start=True)

    except:
        #check what the error should be
        event_decider(event)