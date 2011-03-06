#!/usr/bin/python
#Blah
# What This Means: 
#	You can do whatever you want with (including modify, sell, distribute 
#	and GPL) it as long as you Give me credit for writing the program
#
#	it restricts nothing other than not giving me some credit
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

import time
import twitter


consumer_key = '2x0h71VcEAk2dAdf886HmA'
consumer_secret = 'WWsaaEJOzCuRtUxhR2kU6LShZNyNBSufuKod91N1U'
access_key = '254290857-CrESL7rXpjMlJnaCqlTwANYS2J4dRObMbdqLTcM'
access_secret = 'voHU42UTprwkfEofwXFWtxnfUumwlxKMdAUB8fouIA'
encoding='utf-8'

if not consumer_key or not consumer_secret or not access_key or not access_secret:
	print "error: consumer_key ,consumer_secret ,access_key ,access_secret need to be set"	
	sys.exit(2)

api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
	access_token_key=access_key, access_token_secret=access_secret,
	input_encoding=encoding)

message= ''
last_deleted_message=''
last_status = twitter.Status()
current_timezone=(time.timezone/60)/60 # Timezone
status_update_delay=api.MaximumHitFrequency()
last_reply_id=0



#------------------------------------------------------------
#time date functions
def current_time_date():
	timen=time.gmtime()
	return str(timen[3]-current_timezone)+":"+str(timen[4])+" "+str(timen[1])+"-"+str(timen[2])+"-"+str(timen[0])

def current_time():
	timen=time.gmtime()
	return str(timen[3]-current_timezone)+":"+str(timen[4])

#------------------------------------------------------------
#About
def about():
	print "Twitter Shell Version .1"
	print "	By Jason White, February 20 2011"
	print ""
	print "Special Thanks to:"
	print "	Alphageek"
	print "	Quick_Ben"
	print "	maglinvinn"
	print "	MrTransistor"
	print "	Sparky Projects"
	print "	Tmb"	
	print "	Tysk"
	print "	and everyone else in the forums !"
	print ""
	print "This program takes the output of a Teletype machine"
	print "and allows the user to post it to twitter. It is a "
	print "fairly simple python script using the python-twitter"
	print "module to interface with twitter"
	print ""
	print "This Program is licensed under the Modified BSD license"
	print "	Program Copyright (C) 2011 Jason White\n"

#------------------------------------------------------------
#The Banner
def banner():
	print "	Twitter Shell Version .1"
	print " Because the geek shall inherit the earth"
	print ""

#------------------------------------------------------------
#The Bad command text, this could be made into a var but its cleaner as a function
def bad_cmd():
	#banner()
	print "Unknown command type ? or help for help"

#------------------------------------------------------------
#Help Me ! Text
def help():
	print "Help Me ! - Commands"
	print ""
	print "	about - more info about this program"
	print "	delete - delete the last message"  
	print "	help - print this help text"
	print "	read - read replies"
	print "	undelete - undelete the last post, if it was deleted"
	print "	post - post a message to twitter"
	print " quit - quit this program"
	print ""
	print "	Twitter Shell For The Geek Group"
	print "	 By Jason White February 20 2011\n"

#------------------------------------------------------------
# Gets input from the commandline
def command():
	cmd=str(raw_input(current_time()+" Command > ")).lower()  # make the command all lowercase for usage
	time.sleep(status_update_delay/8)
	print("")

	if not cmd: # command input was empty 
		return 2 # do nothing

	if cmd=="about":
		about()
		return 2

	if cmd=="?" or cmd=="help":
		help() # prints help text
		return 2

	if cmd=="post":
		print "Type message, maximum 140 characters, newline to finish"
		print "Feel free to include you name so others know who's posting"
		inputs=str(raw_input("> "))
		if not 10 <= len(inputs):
			print "Message must be more than 10 characters"

			while(1):
				i=str(raw_input("post anyways ? [Yes/No] ")).lower()
				if i=="yes":
					post(inputs+"...........")
					break
				if i=="no":
					break
				print "Yes or No"
			return 2

		if not len(inputs) <= 140:
			print "Message must be less than 140 characters"
			return 2
		post(inputs)
		return 2

	#deletes the last post
	if cmd=="delete":
		while(1):
			i=str(raw_input("Delete you last post ? [Yes/No]")).lower()
			if i=="yes":
				destroy(last_status)
				break
			if i=="no":
				break
			print "Please type Yes or No"
		return 2

	#undelete's the last post if it was deleted
	if cmd=="undelete":
		global last_deleted_message

		if not last_deleted_message=="":
			post(last_deleted_message)
			last_deleted_message=""
		return 2
		
	#read command
	if cmd=="read" or cmd=="view":
		read_replies()
		return 2


	#exit command
	if cmd=="exit" or cmd=="quit":
		q=str(raw_input("Really [Yes/No]\a")).lower()
		if q=="y" or q=="yes":
			print "Goodbye"
			return 0
		else:
			print "Thank You"
			return 2
	
	bad_cmd()
	return 2

#------------------------------------------------------------
#posts to twitter, prompts for deletion to allow the user to remove mistakes
def post(message):
	

	print "Processing ...\n"
	time.sleep(status_update_delay/4)		

	try:
		global last_status

		last = api.PostUpdate(message)
		last_status=last
	except UnicodeDecodeError:
		print "Your message could not be encoded.  Perhaps it contains non-ASCII characters? "
		print "Try explicitly specifying the encoding with the --encoding flag"
		sys.exit(2)

	limit=api.GetRateLimitStatus()
	print last.user.name+" just posted: "+last.text
	#print str(limit.get('remaining_hits'))+" posts until limit is reached" # I'm unsure if this really works ....
	#print "This Resets At: "+str(limit.get('reset_time'))
	#print "Hourly Limit: "+str(limit.get('hourly_limit'))
	time.sleep(status_update_delay/8)
	print
	print "remember: you can always use the delete command to remove your post and try again"

#------------------------------------------------------------
#destroy the last post
def destroy(status):
	global last_deleted_message
	last_deleted_message=status.text
	api.DestroyStatus(status.id)
	print "Processing ..."
	time.sleep(status_update_delay/4)
	print "Last Post Deleted"
#------------------------------------------------------------
#get replies

def replies(): #displays latest reply and # of replies
	global last_reply_id
	reply=api.GetReplies(None,last_reply_id)
	i=len(reply)-1
	print str(len(reply))+" New Replies: Type 'read' to read the replies"

def read_replies(): #displays latest reply and # of replies
	global last_reply_id

	reply=api.GetReplies(None,last_reply_id) #download replies every view of a reply
	i=len(reply)-1
	
	while 1:
		if i==-1:
			break

		last_reply_id=reply[i].id

		print "    "+reply[i].user.screen_name+" said: "+reply[i].text
		print "In reply to "+reply[i].in_reply_to_screen_name+": "+api.GetStatus(reply[i].in_reply_to_status_id).text+"\n"

		reply=api.GetReplies(None,last_reply_id) #download replies every view of a reply
		i=len(reply)-1
		
		time.sleep(2)

#------------------------------------------------------------
#its the main one ...
def main():
	print "\a"
	i=1
	while(1):

		if i==0:
			break
		if i==1:
			banner()
			replies()
			i=command()
		if i==2:
			replies()
			i=command()

		if i==None:
			print "error i is NULL"
			i=2;


if __name__ == "__main__":
	main()
