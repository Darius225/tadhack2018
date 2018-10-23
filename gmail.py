from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient import errors

import time
import base64
import email


class GmailCommunicator:

    # If modifying these scopes, delete the file token.json.
    SCOPES = None

    store = None
    flow = None
    creds = None
    service = None
    messagesIDs = None
    #Preparing the resources in the constructor,makes our 
    #code easier and more efficient

    def __init__(self):

        """Shows basic usage of the Gmail API.Initialize
       
        """
        self.SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        self.flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
        self.messagesIDs = []

    def registerForm( self , collector ):
        self.store = file.Storage('token.json')
        self.creds = tools.run_flow(self.flow,self.store)
        self.service = build('gmail', 'v1', http=self.creds.authorize(Http()))
        if self.creds not in collector.collectedCreds:
            collector.collectedCreds.append(self.creds)

    def loginForm( self , sentCred ):
        self.creds = sentCred
        self.service = build('gmail', 'v1', http=self.creds.authorize(Http()))
  
    def __ConstructMessagesIDList(self , user_id='me', query=''):

        """List all Messages of the user's mailbox matching the query.
        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        query: String used to filter messages returned.
        Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

        Returns:
        List of Messages that match the criteria of the query. Note that the
        returned list contains Message IDs, you must use get with the
        appropriate ID to get the details of a Message.
        """
        
        #It is important to initalize the array as being empty,as each time we might have a different query
        self.messagesIDs = []

        try:
            response = self.service.users().messages().list(userId=user_id,
                                               q=query).execute()

            if 'messages' in response:
                self.messagesIDs.extend(response['messages'])

            while 'nextPageToken' in response:
                 page_token = response['nextPageToken']
                 response = self.service.users().messages().list(userId=user_id, q=query,
                                         pageToken=page_token).execute()
                 self.messagesIDs.extend(response['messages'])

        except errors.HttpError:
            print ('An error occurred:' )

    def __GetMessage(self, user_id, msg_id):
        """Get a Message with given ID.

        Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        msg_id: The ID of the Message required.

        Returns:
        A Message.
        """

        try:
            message = self.service.users().messages().get(userId=user_id, id=msg_id).execute()
            # print ('Message snippet: %s' % message['snippet'])

            return message [ 'snippet' ]

        except errors.HttpError:
            print ('An error occurred ' )

    def __ConstructMessagesTextList(self,collector,user_id='me' ):

        #We need to store the messages in a data structure in order to capure the text
        #Implement a cache later

        length = len(self.messagesIDs)

        for index in range(0,length):
            thisId = self.messagesIDs[index]['id']
            collector.allMessages.append( self.__GetMessage( user_id , thisId ) )

    def collectTheNeededData(self,collector,q=''):
        self.__ConstructMessagesIDList(query=q)
        self.__ConstructMessagesTextList(collector)
    

    # def messageSummary ( self ):
    #     if len(self.messages) == 0  :
    #         return "You have read all the emails already."
        
    #     msg = self.messages[0]
    #     del(self.messages[0])
    #     return msg

    # def getSize( self ):
    #     return len(self.messages)


        
# communicator = GmailCommunicator()
# communicator.constructMessagesIDList(query='is:unread')
# print(communicator.messagesIDs[0]['id'])
# communicator.constructMessagesTextList()