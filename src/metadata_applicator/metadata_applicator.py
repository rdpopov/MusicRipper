#!/home/rosko/dev/MusicRipper/bin/python3
import cmd_line_util


# TODO: use argparse for the arguments
class Song:
    def __init__(self,fname):
        self.fname = fname
        self.name = None
        self.artist = None
        self.album = None
        self.artwork_uri = None

    def getinfo(self,mdataFacade):
        # TODO: implement
        pass

def main():
    # TODO: add use of argparse module
    parser = cmd_line_util.GenericInput([], False)
    for ln in parser:
        print(ln)


if __name__ == "__main__":
    main()
