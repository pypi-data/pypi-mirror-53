import os
import sys
from termcolor import cprint, colored, COLORS
import time
CLS = list(COLORS.keys())[1:-1]
LAST = ''

def colorL(*a, end='\n'):
    global LAST
    m = ''
    for i,v in enumerate(a):
        m += " "+ colored(str(v), CLS[i % len(CLS)] ) 
    if m == LAST:
        LAST = m
        end='\r'
    print(colored("[+] ", 'green',attrs=['bold']), m, end=end)

def notify(msg):
    if sys.platform.startswith("linux"):
        os.popen("notify-send '%s' " % msg)
    elif sys.platform.startswith("darw"):
        os.popen("terminal-notifier -message '%s' " % msg)
    else:
        colorL("%s" % msg)
