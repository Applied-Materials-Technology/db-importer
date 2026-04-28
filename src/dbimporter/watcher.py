import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import numpy as np


class Watcher:

    """
    Watches the specified directory for new files
    """

    def __init__(self, 
                 watch_path: Path,
                 checker):


        self.watch_path = watch_path
        self.checker = checker
        self.observer = Observer()


    def run(self):

        event_handler = Handler(self.checker)
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

    def __init__(self, checker): 
        self.checker = checker

        print(self.checker)

    def on_any_event(self,event):

        if event.is_directory:

            return None

        if event.event_type == 'created':

            print("Watchdog received created event - % s." % event.src_path)

        elif event.event_type == 'modified':

            print("Watchdog received modified event - % s." % event.src_path)

            
            event_decider(event)
            

def event_decider(event):

    try:
        print("file")

    except:
        print("fail")

        event_decider(event)