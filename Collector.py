from gmail import GmailCommunicator


#Class used to collect messages from all added emails
class Collector:

	allMessages = None
	gmailCom = None
	collectedCreds = None 

	def __init__(self):
		self.allMessages = []
		self.gmailCom = GmailCommunicator()
		self.collectedCreds = []

	def addEmail(self):
		self.gmailCom.registerForm(self)
		self.searchSingleMail('is:unread',self.collectedCreds[len(self.collectedCreds)-1])

	def search(self,query):
		#Everytime we search we can reset the result of our cached messages already searched 
		#This is neccessary because otherwise some emails from other credentials 
		#will be counted multiple times
		self.allMessages = []
		for cred in self.collectedCreds:
			self.searchSingleMail(query,cred)

	def searchSingleMail(self,query,cred):
		self.gmailCom.loginForm( cred )
		self.gmailCom.collectTheNeededData(q=query,collector = self)


	def messageSummary ( self ):
		if len(self.allMessages) == 0:
			return "You have read all the emails already."
		msg = self.allMessages[0]
		print(msg)
		del(self.allMessages[0])
		return msg

	def getSize( self ):
		return len(self.allMessages)
