from matrix_client.client import MatrixClient
from matrix_client.api import MatrixHttpApi
from Collector import Collector
import time

#Better to store predefined names in global variables
ourApi = "https://matrix.org"
roomId = "#TestRoom:matrix.org" 
password = "321123da"
user = "darius225"
userAddress="@darius225:matrix.org"
collector = Collector()
responses = { False : "Did not manage to login.Maybe you could try again !" , True : "Logged in succesfully" }


# Called when a message is received.
def on_message(room, event):
	    global userAddress
	    global collector
	    previousAddingEventId = None;
	    if event['type'] == "m.room.member":
	    	if event['membership'] == "join":
	    		print("{0} joined".format(event['content']['displayname']))
	    elif event['type'] == "m.room.message":
	    	if event['content']['msgtype'] == "m.text":
	    		if "Add gmail account" in event['content']['body'] and event['sender'] != userAddress :

	    			print("{0}: {1}".format(event['sender'], event['content']['body']))

	    			room.send_text("We will have a look at the unread messages on this account")

	    			currentEventId = event [ 'event_id' ]

	    			#We can add multiple emails
	    			if  currentEventId != previousAddingEventId: 
	    				collector.addEmail()

	    			room.send_text( "I can give summaries of the emails on this service. ")
	    			time.sleep(2)
	    			room.send_text( "You can type 'unread' to read the next unread email.There are currently " + str(collector.getSize()) + " unread emails" )
	    			time.sleep(2)
	    			room.send_text( "Or you can search an email by a term.You can do this by typing 'search:term' ." )
	    			time.sleep(2)
	    			room.send_text( "Looking forward to you asking me any question :) .")

	    			previousAddingEventId = currentEventId

	    		elif "unread" in event['content']['body'] and collector is not None and event['sender'] != userAddress :
	    			print(event['sender'] , userAddress )
	    			room.send_text("I will get shortly with a summary for the current unread message: " )
	    			time.sleep(2)
	    			msg = collector.messageSummary()
	    			room.send_text(msg)
	    			time.sleep(2)
	    			room.send_text("There are " + str(collector.getSize()) + " messages left to read." )

	    		elif "search:" in event['content']['body'] and event['sender'] != userAddress  :
	    			message = event ['content'] [ 'body'] [7:]
	    			print(message)
	    			room.send_text("I will search all the emails for " + message )
	    			collector.search(message)
	    			room.send_text("Search returned " + str(collector.getSize())+ " emails")
	    			room.send_text("Now type ViewEmail to see the first email from the query:")

	    		elif "ViewEmail" in event['content']['body'] and event['sender'] != userAddress  :
	    			room.send_text("I will come with the result fast.")
	    			time.sleep(1)
	    			room.send_text(collector.messageSummary())
	    			time.sleep(1)
	    			room.send_text("There are still " + str(collector.getSize()) + " messages to check")





	    else:
    		print(event['type'])

client = MatrixClient(ourApi)
token = client.login_with_password(username=user, password=password)
room = client.join_room(roomId)
room.send_text( " Add your app account to the chatbot. ")
room.send_text( " First let me know which app you want to synchronize. " )
room.send_text( " Currently,you can add more mails for gmail.You just have to type Add gmail account how many times you would like.")
room.add_listener(on_message)
client.start_listener_thread()
while True:
	i = 0
