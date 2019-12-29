#!/usr/bin/python3

""" filddle - v 0.1
    Author     - kaelkmk a.k.a Khaing Myel Khant
    License    - GNU General Public License v3.0
    Copyright © 2019 Khaing Myel Khant
"""

import sys
import os
import time
from datetime import datetime
import argparse
import shutil

VERSION = 'Filddle 2.0'
DIRCONFFILE = '.filddle.conf'
PLATFORM = sys.platform
OS = os.name

# for logging stuff
WHITE = '\033[97m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[34m'
END = '\033[0m'
LOAD = '[' + YELLOW + '*' + END + ']'
INPUT = '[' + YELLOW + '+' + END + ']'
SUCCESS = '[' + GREEN + '+' + END + ']'
WARNING = '[' + YELLOW + '!' + END + ']'
ERROR = '[' + RED + 'x' + END + ']'

# Enable ANSI
if PLATFORM == "win32":
    os.system("")

if PLATFORM == 'darwin':
    CONFIG = os.path.join(os.path.expanduser('~'), '.filddle-default.conf')
elif PLATFORM == 'win32' or OS == 'nt':
    CONFIG = os.path.join(os.getenv('userprofile'), 'filddle-default.conf')
elif PLATFORM == 'linux' or PLATFORM == 'linux2' or OS == 'posix':
    CONFIG = os.path.join(os.getenv('HOME'), '.filddle-default.conf')
else:
    CONFIG = os.path.join(os.getcwd(), '.filddle-default.conf')

def main():
    Filddle()

class Filddle:
    """
        All format lists were taken from wikipedia and classifier v2.0, not all of them were added due to extensions
        not being exclusive to one format such as webm, or raw
        Audio 		- 	https://en.wikipedia.org/wiki/Audio_file_format
        Images 		- 	https://en.wikipedia.org/wiki/Image_file_formats
        Video 		- 	https://en.wikipedia.org/wiki/Video_file_format
        Documents 	-	https://en.wikipedia.org/wiki/List_of_Microsoft_Office_filename_extensions
    """

    def __init__(self):
        self.banner()
        self.description = "Organize and classify your files to different folders and specific folder "
        self.parser = argparse.ArgumentParser(prog="Filddle", description=self.description)
        self.parser.add_argument("-v", "--version", action="store_true",
                                 help="Show the version of the program")
        self.parser.add_argument("-st", "--specific-types", nargs="+", type=str,
                                 help="Organize the specific file types [ use with -sf ]")
        self.parser.add_argument("-sf", "--specific-folder", nargs=1, type=str,
                                 help="Organize specific files types into specific folder [ use with -st ]")
        self.parser.add_argument("-t", "--types", action="store_true",
                                 help="Show supported File Types and Formats")
        self.parser.add_argument("-l", "--log", action="store_true",
                                 help="Create a log file that notes organized files during this program")
        self.parser.add_argument("-p", type=str, dest="path", nargs=1,
                                 help="Path of the folder location to be organized")
        self.parser.add_argument("-d", nargs=1, type=float, dest="delay",
                                 help="Add some delay to check what is happening")
        self.parser.add_argument("--reset", action="store_true",
                                 help="Reset the configuration file")
        # parsing arguments
        self.args = self.parser.parse_args()
        self.delay = self.args.delay

        if self.args.path:
            self.path = self.args.path[0].replace("\\", "/") + "/"
        else:
            self.path = "./"

        # add some variables
        self.formats = {}
        self.count = 0

        # run
        if not self.args.path:
            print(WARNING, "You can use filddle.py -p 'path to specific folder'."
                           "I will use current path for classifying your files\n")
            print(WARNING, "Current Path: ", self.path+"\n")
        choice = input(INPUT + " Enter y to continue, n to quit: ")
        print()
        if 'y' in choice.lower():
            self.start_time = time.time()
            self.run()
        else:
            print(SUCCESS, "Good Luck ! ")
            sys.exit()

    def create_default_config(self):
        with open(CONFIG, 'w') as conf:
            conf.write("Programs: exe, jar, msi \n" +
                       "Scripts: py, pyc, asm, cs, php, java, class \n" +
                       "Music: mp3, acc, flac, ogg, wma, m4a, aiff, wav, amr \n" +
                       "Pictures: png, jpeg, gif, jpg, bmp, svg, webp, psd, tiff \n" +
                       "Documents: txt, pdf, doc, docx, odf, xls, xlsv, xlsx, " +
                       "ppt, pptx, ppsx, odp, odt, md, json, csv \n" +
                       "DEBPackages: deb \n" +
                       "RPMPackages: rpm"
                       )
            conf.close()
        print(SUCCESS, "CONFIG file created at ", CONFIG)
        return

    def check_config(self):
        if not os.path.isdir(os.path.dirname(CONFIG)):
            os.makedirs(os.path.dirname(CONFIG))
        if not os.path.isfile(CONFIG):
            print(WARNING, "Configuration is not created. Trying to create one ...")
            self.create_default_config()
        print(LOAD, ' Configuration found at ', CONFIG, ' ... ', end="")
        try:
            with open(CONFIG, 'r') as file:
                for items in file:
                    type = items.replace("\n", "")
                    key = type.split(":")[0].strip()
                    value = type.split(":")[1].strip()
                    self.formats[key] = value
        except ValueError as e:
            print(ERROR, "Configuration file is malformed, filddle.py --reset or check it")
        print("[ LOADED ]\n")
        return

    def show_executing_time(self):
        return str(round((time.time() - self.start_time) * 1000, 2))

    def remove_space(self, list):
        l = []
        for i in list:
            l.append(i.strip())
        return l

    def classify(self):
        # print("files: ", str(os.listdir(self.path)))
        # print(self.path + os.listdir(self.path)[1])
        for file in os.listdir(self.path):
            if os.path.isfile(self.path+file) and not file == sys.argv[0]:
                filename, file_ext = os.path.splitext(file)
                file_ext = file_ext.lower().replace(".", "")
                # print(filename, file_ext)
                for folder, ext_list in self.formats.items():
                    if file_ext in self.remove_space(ext_list.split(",")):
                        try:
                            if not os.path.exists(self.path + folder):
                                os.makedirs(self.path+folder)
                            shutil.move(self.path + file, self.path + folder + '/' + file)
                            self.count += 1
                            if self.args.delay:
                                if self.delay > 0:
                                    time.sleep(delay)
                            if self.args.log:
                                with open('fiddle.log', 'a') as log:
                                    log.write(str(datetime.now()) + " " * 2 + self.path + file + " ----> " + self.path + folder + '/' + file + "\n")
                        except Exception as e:
                            print("Cannot move - {} - {}".format(file, str(e)))
        return

    def run(self):
        if self.args.version:
            # PRINT VERSION
            print(VERSION)
            return False

        if bool(self.args.specific_types) ^ bool(self.args.specific_folder):
            print(ERROR, "Specific Folder and Specific Types need to be specified together\n")
            print(ERROR, "Program Terminated ...", self.show_executing_time(), 'ms')
            sys.exit()

        self.check_config()

        if self.args.reset:
            self.create_default_config()
            print(SUCCESS, "Config file is successfully restored")

        if self.args.specific_types and self.args.specific_folder:
            specific_folder = self.args.specific_folder
            self.formats = {specific_folder[0]: ','.join(c for c in self.args.specific_types)}

        if self.args.types:
            print("Supported Types \n" + "#" * 24)
            for k, v in self.formats.items():
                print(k, ":", v)
        self.classify()
        print()
        print(SUCCESS, "Finished ...", self.show_executing_time(), 'ms')
        return

    def banner(self):
        print("""%s          
        ███████╗██╗██╗     ██████╗ ██████╗ ██╗     ███████╗
        ██╔════╝██║██║     ██╔══██╗██╔══██╗██║     ██╔════╝
        █████╗  ██║██║     ██║  ██║██║  ██║██║     █████╗  
        ██╔══╝  ██║██║     ██║  ██║██║  ██║██║     ██╔══╝  
        ██║     ██║███████╗██████╔╝██████╔╝███████╗███████╗
        ╚═╝     ╚═╝╚══════╝╚═════╝ ╚═════╝ ╚══════╝╚══════╝
        %s                                          v0.1 kaelkmk\n""" % (GREEN, END))

if __name__ == "__main__":
    main()

    
