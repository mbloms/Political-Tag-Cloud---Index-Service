# Using Twithon, install with sudo pip3 install twython
from twython import Twython,TwythonRateLimitError
import time
import ConnectionList as CL
import TwitterUsers as TU
import json

def main():
    getUsersFollowers()    


def getUsersFollowers():
    users = TU.TwitterUsers()
    for group in users.getGroups():
        # group[0] now contains name and [1] list of users
        for user in group[1]['users']:
            getFollowers(user)


def getFollowers(user):
    conn = CL.ConnectionList(filepath="config/access.conf") 

    cursor = -1 #default cursor
        
    while cursor != 0:
        
        currentCursor = cursor

        try:
            response = conn.connection().get_followers_ids(screen_name = str(user),cursor = cursor)

            for followerId in response['ids']:
                print(followerId)
                cursor = response['next_cursor']


        except TwythonRateLimitError:
            time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min
            cursor = currentCursor


    
main()
