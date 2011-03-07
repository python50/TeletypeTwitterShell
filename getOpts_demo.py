#!/usr/bin/env python

import sys, os, tempfile, subprocess, shutil, getopt

versionNumber = "Insert Current Version Number Here"


def usage():
  print "\nUsage: twitshell.py [-p message_content] [-d]"
  print "Options:\n  -h\t\tShow this help and exit\n  -v\t\tVersion information\n  -p\t\tPost a tweet containing this content\n  -d\t\tDisplay recent replies"


def post(content):
  print "Pretending to post."
  print "Post content: " + content

def read_replies():
  print "Pretending to read replies"

def mainMenu():
  print "If nothing was entered, display main menu"


def main(argv):
  
  '''Get the options list'''
  try:
    opts, args = getopt.getopt(argv, "hvp:d", ["help", "version"] )
  #fail if the user screwed up
  except getopt.GetoptError:
    usage()
    sys.exit(2)
  
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      usage()
      sys.exit(0)
    if opt in ("-v", "--version"):
      print "Version: " + versionNumber
      sys.exit(0)
    if opt in ("-p"):
      post(arg)
      sys.exit(0)
    if opt in ("-d"):
      read_replies()
      sys.exit(0)
  
  mainMenu()
  
if __name__ == '__main__':
  main(sys.argv[1:])