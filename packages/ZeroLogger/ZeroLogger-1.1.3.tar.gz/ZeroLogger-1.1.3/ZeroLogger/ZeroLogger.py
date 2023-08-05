install = []
import os
import sys

try: from colorama import Fore, init
except: install.append("colorama")

# Trying to install the needed modules if there not already
if install:
    to_install = " ".join(install)
    os.system(sys.executable + " -m pip install " + to_install)
    print("[STARTUP] INSTALLED MODULES: "+str(install))
    quit()

# colors!
init()

################## Functions ######################################
def warn(text):
    print("["+Fore.YELLOW+"WARN"+Fore.RESET+"] "+str(text))

def error(text):
    print("["+Fore.RED+"ERROR"+Fore.RESET+"] "+str(text))
    
def done_task(text):
    print("["+Fore.GREEN+"DONE"+Fore.RESET+"] "+str(text))

def info(text):
    print("["+Fore.WHITE+"INFO"+Fore.RESET+"] "+str(text))

def critical(text):
    print("["+Fore.RED+"CRITICAL"+Fore.RESET+"] "+str(text))
    quit()

################## END LOGGING ###################################
