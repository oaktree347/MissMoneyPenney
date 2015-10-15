#!/usr/bin/env python

# Sithmail-Tipbot
# Copyright (C) 2015 Bren Briggs and Kevin McCabe

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import Legobot
import time
import sys
import os
import re
import requests
from requests_ntlm import HttpNtlmAuth
import xml.etree.ElementTree as ET
import random
import urllib2
import base64
import json
import datetime

__author__ = "Kevin McCabe"
__copyright__ = "Copyright 2014"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Development"

##########################################################################################
#
# Global Vars
#
##########################################################################################

TIP_DICT = {}
PYDIR = os.path.dirname(os.path.abspath(__file__))
SNARKS = []
LAST_SNARK = datetime.date
##########################################################################################
#
# FECN file Vars (initializing for explicivity)
#
##########################################################################################

HOST=''
HOSTPW=''
PORT=''
NICK =''
ROOM =''
ROOMPW =''
SNARKHOLDDOWN =''
ISSSL =''
        
##########################################################################################
#
# Dropin functions
#
##########################################################################################

def cointoss(msg):
    """
    Inputs:
      takes msg object

    Outputs:
      returns string to echo back to user in IRC

    Purpose:
      flip an imaginary coin or roll an imaginary x sided die
      Usage:
      !roll [# of sides]
    """

    if not msg.arg1:
        toss = random.randint(0,1)
        if toss == 0:
            returnVal = "Heads"
        else:
            returnVal = "Tails"
    else:
        if not is_num(msg.arg1):
            returnVal = "Incorrect syntax. You must use a (sane) number"
        elif is_num(msg.arg1) and not int(msg.arg1) >= 2:
            returnVal = "Do you live in Flatland? Is your name Edwin Abbott Abbott? No. Use more than two sides."
        elif is_num(msg.arg1) and int(msg.arg1) == 2:
            toss = random.randint(1,2)
            if toss == 1:
                returnVal = "Heads"
            else:
                returnVal = "Tails"
        else:
            toss = random.randint(1,int(msg.arg1))
            returnVal = str(toss)
    return returnVal

def tip_user(msg):
    """
    Inputs:
      takes msg which is a cMsg object

    Outputs:
      returns string to echo back to user in IRC

    Purpose:
      allows users to tip other users (must be in our engineer list) magical imaginary points
      Usage:
      !tip [cco] [x-points]
    """
    if msg.arg1 is None or msg.arg2 is None:
        #must have 2 args
        returnVal = fGetHelpText(msg.cmd)
        
    elif msg.arg1 in msg.userInfo:
        returnVal = "You can't tip yourself!"
    
    elif not is_num(msg.arg2):
        returnVal = "Incorrect Syntax, you must tip a number"
        
    else:
        #proper number of args
        if msg.arg1 in TIP_DICT:
            TIP_DICT[msg.arg1] += int(msg.arg2)
        else:
            TIP_DICT[msg.arg1] = int(msg.arg2)

        returnVal = "%s tipped, and now has %s internet points" % (msg.arg1, TIP_DICT[msg.arg1])
    return returnVal

def print_tips(msg):
    """
    Inputs:
        takes junk which is a cMsg object: optional and unused

    Outputs:
        returns string to echo back to user in IRC

    Purpose:
        allows users to view current tips.    Usage:
        !printtips
    """
    
    
    tips = ["%s: %s" % (k, v) for k, v in TIP_DICT.items()]
    if len(tips) == 0:
        returnVal = "No tips yet!"
    else:
        returnVal = "Current Tips: %s" % (", ".join(tips))
    return returnVal

def snark(msg):
    """
    Inputs:
        msg object which is unused

    Outputs:
        returns string to echo back to user in IRC

    Purpose:
        returns random snark to irc. Usage: !snark
    """
    return random.sample(SNARKS,1)[0]

def who_is_up(msg):
    """
    Inputs:
        msg object which is unused

    Outputs:
        returns string to echo back to user in IRC

    Purpose:
        allows users to view current tips.    Usage: !whoisup
    """
    return "tnay is up!"

def xkcd(msg):
    webpage = urllib2.urlopen('http://dynamic.xkcd.com/random/comic')
    webpage = webpage.read()
    print webpage
    comic = re.search(r'<div id="comic".*?\n?.*?(//im.+?)".+?\s?title="(.+?)"',webpage)
    if comic:
        altText = comic.group(2).replace("&#39;","'")
        returnVal = "%s %s" %(altText,"http:" + comic.group(1))
        return returnVal


##########################################################################################
#
# Supporting Functions
#
##########################################################################################

def load_fecn():
    """
    Inputs:
      None, this function is run on load, it may also be run by doing !reread from a user
      who has authenticated appropriately

    Outputs:
      prints success/non success of loading each line that doesn't start with #

    Purpose:
      Loads in a config file from ./config.fecn, all variables are loaded into globals
    """

    try:
        fileLoc = "%s%s" % (PYDIR,"/config.fecn")
        f = None
        f = open(fileLoc, "r")
        info = f.read()
        f.close()

        for line in info.splitlines():
            if not line.strip():
                print "skpping blank fecn file line: %s" % line.strip()
                continue
            
            if line[0] == "#":
                print "skipping fecn file line: %s" % line
                continue
            
            var = re.search(r"^\s*[^#]?<(?P<type>.*?)>(?P<var_name>.*?)=(?P<var_value>.*)", line)
            
            if not var:
                print "couldn't load fecn file line: %s" % line
                continue
            
            #var to hold success for this line
            loaded = True
            
            #using groupdict to pull out a dict from regex
            var_dict = var.groupdict()
            
            #save in loop vars
            my_type = var_dict["type"].strip().lower()
            my_var_name = var_dict["var_name"].strip().upper()
            my_var_value = var_dict["var_value"].strip()
            
            #cast output to type specific variables
            if my_type == "int":
                globals()[my_var_name] = int(my_var_value)
                
            elif my_type =="str":
                globals()[my_var_name] = my_var_value
                
            elif my_type =="bool":
                if my_var_name.lower() in ["yes","true","y","1"]:
                    globals()[my_var_name] = True
                    
                elif my_var_name.lower() in ["false","no","0","n"]:
                    globals()[my_var_name] = False
            
            elif my_type == "json":
                globals()[my_var_name] = json.loads(my_var_value)
            
            else:
                loaded = False
                print "%s not loaded into globals because %s isn't recognized as a usable type" % (my_var_name % my_var_type)
            
            #report on success of line
            if loaded:
                print "loaded %s into globals as %s" % (my_var_name, str(my_var_value))
            
        returnVal = "Configuration re-applied"

    except Exception as e:
        returnVal = "an error occurred: %s" % str(e)
        raise
    
    finally:
        if f:
            f.close()
    
    print returnVal

def load_snark():
    global SNARKS
    snark = []
    f = open(PYDIR + "/snark.fecn", "r")
    for line in f:
        if line[0] == "#":
            pass #removed superfluous print statement
        else:
            snark.append(line.strip('\n'))
    f.close()
    SNARKS = snark


def is_num(val):
    try:
        if float(val) != int(val):
            return False

        test = int(val)
        test = int(float(val))

        return True
    except:
        return False

def get_html(u,p,url):
    s = requests.Session()
    s.auth = HttpNtlmAuth("cisco\\" + u, p)
    f = s.get(url)
    return f.text



##########################################################################################
#
# All config for your bot should be done in main()
#
##########################################################################################

def main():
    #load fecn file
    
    load_fecn()
    load_snark()
    #parameters needed to allow bot to connect to IRC room:
    room_info = [(ROOM,"")]    #Rooms we wish the bot to join, Must be a list of tuples, even for one item.  tuple has items ("roomname","roompw") if you don't have a password, just pass a blank string
    isSSL = True               #whether or not the bot will be connecting via SSL

    #create bot object, note the logging function option and hostpw are optional
    myBot = Legobot.legoBot(host = HOST, 
                            port = PORT, 
                            nick = NICK, 
                            chans = room_info)
    
    #run snark whenever someone puts in ! as the first char and no other function matches
    myBot.addDefaultFunc(snark, "!")

    #add functions manually to the bot
    #for addFunc, the first param is the trigger, second is the name of the function to run on match
    myBot.addFunc("!tip", tip_user, "Tip a specific user. Usage !tip [user]")
    myBot.addFunc("!roll", cointoss, "Roll a magical N-sided die. Usage !roll [optional #]")
    myBot.addFunc("!printtips", print_tips, "Displays current tips. Usage !printtips")
    myBot.addFunc("!snark", snark, "Returns something snarky. Usage !snark")
    myBot.addFunc("!xkcd", xkcd, "Pulls a random XKCD comic. Usage: !xkcd.")
    
    #Timer functions, they take cron like options
    # myBot.addTimerFunc(foo, sec = "0")
    # myBot.addTimerFunc(bar, min = "*/10", sec = "*/15")
    # myBot.addTimerFunc(baz, sec = "*/37")
    
        
    #have bot connect to IRC server and log into room(s) specified
    myBot.connect(isSSL)

if __name__ == '__main__':
    main()
