#!/usr/bin/env python
import json
#from spotify.util import json
import sys
from pprint import pprint
import os
import datetime
import re

def traversejson(_id, dic, outfiles,file):
    if type(dic) is dict and 'translations' in dic:
        for lang in dic['translations'].iterkeys():
            if lang == 'en':
                continue
            print >> outfiles[lang], ('#: %s' % file)
            print >> outfiles[lang], ('#. %s' % '|'.join(_id))
            print >> outfiles[lang], ('#, %s' % dic['approved']) 
            #Process special characters, smarter way - \n,\\n,\\&,\\r, \\\", \"
            msgctxt = dic['description'].replace("\n","\\n").replace("\\n","\\\\n").replace("\\r","\\\\r").replace("\\&","\\\\&").replace('\"','\\\"')
            msgid = dic['translations']['en'].replace("\n","\\n").replace("\\n","\\\\n").replace("\\r","\\\\r").replace("\\&","\\\\&").replace('\"','\\\"')
            msgstr = dic['translations'][lang].replace("\n","\\n").replace("\\n","\\\\n").replace("\\r","\\\\r").replace("\\&","\\\\&").replace('\"','\\\"')

            #msgctxt = re.sub(r'([\\\\]+(.))', r'\\\2', dic['description'])
            
            print >> outfiles[lang], ('msgctxt "%s|%s"' % (msgctxt.encode('utf-8'), '|'.join(_id)) )
            print >> outfiles[lang], ('msgid "%s"' % msgid.encode('utf-8'))
            print >> outfiles[lang], ('msgstr "%s"' % msgstr.encode('utf-8'))
            print >> outfiles[lang], ('\n'.encode('utf-8'))
        return
    for key in dic.keys():
        _id.append(key)
        traversejson(_id, dic[key], outfiles, file)
        _id.pop()

def parsesplang(file):
    #Move to current working project directory
   
    data=open(file,'r')

    curdir = (os.path.abspath(file)).split(file)[0] + 'po-' + file.split('.')[0]
    #print(curdir)

    if not os.path.exists(curdir):
        os.mkdir(curdir)
    
    os.chdir(curdir)

    splang = json.load(data)
    outfiles = {}

    for lang in splang['requiredLanguages']:
        if lang == 'en':
            continue
        outfiles[lang] = open('%s.po' % lang, 'w')
        #print header
        print >> outfiles[lang] ,('msgid ""\nmsgstr ""')
        print >> outfiles[lang] ,('"Project-Id-Version: %s.po\\n"' % lang)
        print >> outfiles[lang] ,('"Report-Msgid-Bugs-To: qa@spotify.com\\n"')
        print >> outfiles[lang] ,('"Project-Id-Version: %s.po\\n"' % lang)
        print >> outfiles[lang] ,('"POT-Creation-Date: %s\\n"\n"PO-Revision-Date: %s\\n"' % (datetime.datetime.now(), datetime.datetime.now()))
        print >> outfiles[lang] ,('"Last-Translator: Translation translation@spotify.net\\n"')
        print >> outfiles[lang] ,('"Language-Team: %s\\n"' %lang)
        print >> outfiles[lang] ,('"MIME-Version: 1.0\\n"\n"Content-Type: text/plain; charset=UTF-8\\n"\n"Content-Transfer-Encoding: 8bit\\n"\n')

    for string in splang['strings']:
        _id = []
        _id.append(string)
        traversejson(_id,splang['strings'][string],outfiles,file)

    for lang in outfiles:
        outfiles[lang].close()

    data.close()

if __name__ == '__main__':
    if len(sys.argv)<2:
        pprint("Enter the splangfile to be converted")
        sys.exit(1)
    elif not sys.argv[1].endswith('.splang'):
        pprint("Enter a splang file format")
        sys.exit(1)

    parsesplang(sys.argv[1])
