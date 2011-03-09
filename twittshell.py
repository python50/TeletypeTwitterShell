#!/usr/bin/python

# What This Means: 
#	You can do whatever you want with (including modify, sell, distribute 
#	and GPL) it as long as you Give me credit for writing the program
#
#  Modified BSD License
# 
#  Copyright (c) 2010, Jason White
#  All rights reserved.
# 
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#      * Redistributions of source code must retain the above copyright
#        notice, this list of conditions and the following disclaimer.
#      * Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#      * Neither the name of Jason White nor the names of its contributors may 
# 	 be used to endorse or promote products derived from this software 
# 	 without specific prior written permission.
# 
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL Jason White BE LIABLE FOR ANY DIRECT, INDIRECT, 
#  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, 
#  OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF 
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
#  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#Python: sorry I'm a C guy commands shall end with ; as long as I'm here 
#  BatSteve: that's pretty stupid, you should be sorry about it
#Python: your code dosn't have too, however as long as I have to use C it wreaks havoc 
# on my code if I don't maintain such programming practices. Anyways look on the 
# bright side python doesn't even see the semicolons's or unnecessary parentheses
# Though I should use true and false more often in my code.

import time
import twitter
import sys
import getopt

#default: python50 my test account
consumer_key = '2x0h71VcEAk2dAdf886HmA';
consumer_secret = 'WWsaaEJOzCuRtUxhR2kU6LShZNyNBSufuKod91N1U';
access_key = '254290857-CrESL7rXpjMlJnaCqlTwANYS2J4dRObMbdqLTcM';
access_secret = 'voHU42UTprwkfEofwXFWtxnfUumwlxKMdAUB8fouIA';
encoding='utf-8';

if not consumer_key or not consumer_secret or not access_key or not access_secret:
	printl("error: consumer_key ,consumer_secret ,access_key ,access_secret need to be set");
	sys.exit(2);

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
	access_token_key=access_key, access_token_secret=access_secret,
	input_encoding=encoding);

message='';
last_deleted_message='';
last_status = twitter.Status();
current_timezone=(time.timezone/60)/60; # Timezone
status_update_delay=0;# 0 or api.MaximumHitFrequency() <- 8
last_reply_id=0;

version_number = "0.1d"; #Screw it ... .20 when word block and history are in ...
			 # I'm going with a numeric versioning system after this

#printl appends carriage returns ...
def printl(string):
	print (string+"\r");

#------------------------------------------------------------
#time date functions, returns string
def current_time_date():
	timen=time.gmtime();
	return str(timen[3]-current_timezone)+":"+str(timen[4])+" "+str(timen[1])+"-"+str(timen[2])+"-"+str(timen[0]);

def current_time():
	timen=time.gmtime();
	return str(timen[3]-current_timezone)+":"+str(timen[4]);

#------------------------------------------------------------
#usage text
def usage():
	printl("");
	printl("Usage: twitshell.py [-p message_content] [-r]");
	printl("Options:");
	printl("	-h		Show this help and exit --help");
	printl("	-v		Version information --version");
	printl("	-p [message]	Post a tweet containing [message] --post");
	printl("	-r		Read(and Display) recent replies --read");

#------------------------------------------------------------
#about text
def about():
	printl("Twitter Shell Version "+version_number);
	printl("	By Jason White, February 20 2011");
	printl("");
	printl("Special Thanks to:");
	printl("	Alphageek");
	printl("	BatSteve");# why don't you ever add yourself ?
	printl("	maglinvinn");
	printl("	MrTransistor");
	printl("	Quick_Ben");
	printl("	Sparky Projects");
	printl("	Tmb");
	printl("	Tysk");
	printl("	and everyone else in the forums !");
	printl("");
	printl("This program takes the output of a Teletype machine");
	printl("and allows the user to post it to twitter. It is a ");
	printl("fairly simple python script using the python-twitter");
	printl("module to interface with twitter");
	printl("");
	printl("This Program is licensed under the Modified BSD license");
	printl("	Program Copyright (C) 2011 Jason White\n");
#------------------------------------------------------------
#banner text
def banner():
	printl("	Twitter Shell Version "+version_number);
	printl(" Because the geek shall inherit the earth");
	printl("");

#------------------------------------------------------------
#bad command text
def bad_command():
	printl("Unknown command type ? or help for help");

#------------------------------------------------------------
#Help Me ! Text
def help():
	printl("Help Me ! - Commands:");
	printl("");
	printl("	[a] or about	- more info about this program");
	printl("	[d] or delete	- delete the last message");
	printl("	[h] or help	- this help text");
	printl("	[r] or read	- read replies");
	printl("	[u] or undelete	- undelete the last post, if it was deleted");
	printl("	[p] or post	- post a message to twitter");
	printl("	[q] or quit	- quit this program");
	printl("");
	printl("	Twitter Shell "+version_number+" For The Geek Group");
	printl("	 By Jason White February 20 2011\n");

#------------------------------------------------------------
# command: Gets input from the command line
def command():
	cmd=str(raw_input(current_time()+" Command >")).lower();  # make the command all lowercase for usage
	time.sleep(status_update_delay/8);
	printl("");

	# command input was empty 
	if not cmd:
		return True; # ignore

	#display about help
	if cmd=="about" or cmd=="a":
		about();
		return True;

	#get command help
	if cmd=="?" or cmd=="help" or cmd=="h":
		help(); # prints help text
		return True;

	#post tweet
	if cmd=="post" or cmd=="p":
		printl("Type message, maximum 140 characters, newline to finish");
		printl("Feel free to include you name so others know who's posting");
		inputs=str(raw_input("> "));
		if len(inputs) <= 10: #python_twitter wont accept it if its less than 10
			printl("Message must be more than 10 characters");
									
			while(1):
				i=str(raw_input("post anyways ? [Yes/No] ")).lower();
				if i=="yes":
					post(inputs+"...........");
					break;
				if i=="no":
					break;
				printl("Yes or No");
			return True

		if len(inputs) > 140:
			printl("Message must be less than 140 characters");
			return True;

		post(inputs);
		return True;

	#deletes the last post
	if cmd=="delete" or cmd=="d":
		while(1):
			i=str(raw_input("Delete you last post ? [Yes/No]")).lower();
			if i=="yes":
				delete(last_status);
				break;
			if i=="no":
				break;
			printl("Please type Yes or No");
		return 1;


	#undelete's the last post if it was deleted
	if cmd=="undelete" or cmd=="u":
		undelete();
		return True;
		
	#read command
	if cmd=="read" or cmd=="view" or cmd=="r":
		read_replies();
		return True;


	#exit command
	if cmd=="exit" or cmd=="quit" or cmd=="q":
		q=str(raw_input("Really [Yes/No]\a")).lower();

		if q=="y" or q=="yes":
			printl("Goodbye");
			return False;
		else:
			printl("Thank You");
			return True;
	
	bad_command(); #it wasn't a recognized command
	return True;

#------------------------------------------------------------
#posts to twitter, prompts for deletion to allow the user to remove mistakes
def post(message):
	

	printl("Processing ...\n");
	time.sleep(status_update_delay/4);	

	try:
		global last_status;

		last = api.PostUpdate(message);
		last_status=last;
	except UnicodeDecodeError:
		printl("Your message could not be encoded.  Perhaps it contains non-ASCII characters?");
		printl("Try explicitly specifying the encoding with the --encoding flag");
		sys.exit(2);

	printl(last.user.name+" just posted: "+last.text);
	#limit=api.GetRateLimitStatus(); # I'm unsure if this really works ....
	#printl(str(limit.get('remaining_hits'))+" posts until limit is reached");
	#printl("This Resets At: "+str(limit.get('reset_time')));
	#printl("Hourly Limit: "+str(limit.get('hourly_limit')));
	time.sleep(status_update_delay/8);
	printl("");
	printl("remember: you can always use the delete command to remove your post and try again");

#------------------------------------------------------------
#destroy the last post
def delete(status):
	global last_deleted_message;
	last_deleted_message=status.text;
	api.DestroyStatus(status.id);
	printl("Processing ...");
	time.sleep(status_update_delay/4);
	printl("Last Post Deleted");

def undelete():
	global last_deleted_message;

	if not last_deleted_message=="":
		post(last_deleted_message);
		last_deleted_message="";
#------------------------------------------------------------
#get replies

def replies(): #displays # of replies
	global last_reply_id;
	reply=api.GetReplies(None,last_reply_id);
	printl(str(len(reply))+" New Replies: Type 'read' to read the replies");

def read_replies(): #displays latest replies
	global last_reply_id;

	reply_list=api.GetReplies(None,last_reply_id); #download replies every view of a reply
	
	reply_list.reverse();
	
	for reply in reply_list:

		printl("    "+reply.user.screen_name+" said: "+reply.text);
		
		if reply.in_reply_to_status_id != None:
			printl("In reply to "+reply.in_reply_to_screen_name+":"+api.GetStatus(reply.in_reply_to_status_id).text+"\n");
		else:
			printl("In reply to no one ?\n");
		
		last_reply_id=reply.id;
		
		time.sleep(2);

#------------------------------------------------------------
#its the main one ...
def main(argv):
  
	'''Get the options list'''
	try:
		opts, args = getopt.getopt(argv, "hvrp:", ["help", "version","read","post="] );
    
	except getopt.GetoptError:
		usage();
		sys.exit(2);
  
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage();
			sys.exit(0);
		if opt in ("-v", "--version"):
			printl("Version: "+version_number);
			sys.exit(0);
		if opt in ("-p","--post"):
			post(str(arg));
			sys.exit(0);
		if opt in ("-r","--read"):
			read_replies();
			sys.exit(0);

	'''Main Interactive Command Prompt'''  
	printl("\a");
	loop_forever = True; #you can blame _python_ _coding_ style for this one  
	first_start = True;

	while(loop_forever):
		if first_start:
			banner();
			first_start = False;
		replies();
		loop_forever = command();


if __name__ == "__main__":
	main(sys.argv[1:])
