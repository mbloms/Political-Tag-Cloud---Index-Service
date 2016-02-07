# Using Twithon, install with sudo pip3 install twython
from twython import Twython,TwythonRateLimitError
import time
import ConnectionList as cl

def main():
    
    f = ["socialdemokrat",
         "vansterpartiet",
         "miljopartiet",
         "sdriks",
         "nya_moderaterna",
         "liberalerna",
         "kdriks",
         "Centerpartiet"]
    

    getUsersFollowers(a)    


def getUsersFollowers(users):
    for u in users:
        getFollowers(u)


def getFollowers(user):
    conn = cl.ConnectionList(filepath="config/access.conf") 

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
