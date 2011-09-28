#!/usr/bin/env python
import json
#from spotify.util import json
import sys
from pprint import pprint
import os
import polib

def parsepo(dir):
    
    #change working directory to csplangrent directory
    os.chdir(dir)
    
    for folder in dir.split("."):
        if "po" in folder:
            splangfile = folder.split("-")[1].split("/")[0]

    #print splangfile, number of po files and the names of the po files
    #print ("The splangfile is %s" %splangfile)
    #print ("Number of po files are %d" %len([name for name in os.listdir(dir) if name.split(".")[1]=="po"])) 
    
    splang = {}
    splang["requiredLanguages"] = []
    splang["requiredLanguages"].append("en")
    splang["strings"] = {}
    pofiles = []
    
    #populate languages
    for name in os.listdir(dir):
        if name.split(".")[1] == "po":
            splang["requiredLanguages"].append(name.split(".")[0])
            pofiles.append(name)
    #print pofiles[0]
    try:
        po = polib.pofile(pofiles[0], encoding = 'utf-8')
    except IOError, e:
        print e
        print 'in ' + pofiles[0]
        return
    for entry in po:              
        csplang = splang["strings"]
        for comment in entry.comment.split("|"):
            if comment not in csplang:
                csplang[comment] = {}
            csplang = csplang[comment]
        csplang['translations'] = {}
    
    #print splang

    #populate strings
    for po_file in pofiles:
        try:
            po = polib.pofile(po_file)
        except IOError, e:
            print e
            print 'in' + po_file
        #probably a format error in po_file
        for entry in po:
            csplang = splang["strings"]
            for comment in entry.comment.split('|'):
                csplang = csplang[comment]
            if "en" not in  csplang["translations"].keys():
                csplang["approved"] = True if entry.flags[0]=="True" else False
                csplang["description"] = entry.msgctxt.split("|")[0]
                csplang["translations"]["en"] = entry.msgid
            csplang["translations"][po_file.split(".")[0]] = entry.msgstr
    
    data = open("%s.splang" %splangfile, "w")
    data.write(json.dumps(splang, sort_keys=True,indent=4))
    
    #json.loads(data) type error?

if __name__ == "__main__":
    if len(sys.argv)<2:
        pprint("Enter the po-directory to be merged")
        sys.exit(1)
    
    dir = sys.argv[1]
    if "." in sys.argv[1]:
        dir = sys.argv[1].replace(".",os.getcwd())
    
    #print("Current directory is %s" %dir)    
    
    parsepo(dir)
