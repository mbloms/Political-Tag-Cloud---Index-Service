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
    
    get_users_followers(f)    


def get_users_followers(users):
    for u in users:
        get_followers(u)


def get_followers(user):
    conn = cl.ConnectionList(filepath="config/access.conf") 

    cursor = -1 #default cursor
        
    while cursor != 0:
        
        current_cursor = cursor

        try:
            response = conn.connection().get_followers_ids(screen_name = str(user),cursor = cursor)

            for follower_id in response['ids']:
                print(follower_id)
                cursor = response['next_cursor']


        except TwythonRateLimitError:
            time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min
            cursor = current_cursor


    
main()
