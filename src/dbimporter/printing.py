import time

class Printer():

    """
    Methods for prettier printing to console
    """

    def __init__(self,
                 default: bool = True,
                 colours = None):
        
        self.default = default
        self.colours = bcolours()

    def print_breakline(self):
        print("------------------------------")

    def wrap_text_star(self, text: str):
        wrap_stars = "*******"
        formatted_text = wrap_stars + " " + text + " " + wrap_stars
        print(formatted_text)
        return formatted_text
    
    def colour_warning(self, text: str):

        return f"{self.colours.WARNING}{text}{self.colours.ENDC}"
    
    def colour_logs(self, text: str, colourtype):

        return f"{colourtype}{text}{self.colours.ENDC}"
    
    def waiting_animation(self, text):
        
        t_end = time.time() + 5
        while time.time() < t_end:
            print(text, end='\r')
            text = text + "."
            time.sleep(0.5)

    
class bcolours:
    DEFAULT = '\x1b[39m' # default
    INFO = "\x1b[36m" # cyan
    WARNING = '\033[93m' # yellow
    ERROR = "\x1b[91m" # light red
    CRITICAL = "\x1b[31m" # red
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
