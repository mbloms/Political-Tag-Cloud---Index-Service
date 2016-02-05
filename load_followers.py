# Using Twithon, install with sudo pip3 install twython
from twython import Twython,TwythonRateLimitError
import json
import time

def main():
    
    APP_KEY = 'Gqw3LVScCY4rZ3wfA1Gbe8FIN'
    APP_SECRET = 'HYuHv5h6OlUqmKp9D5yfX0hNnNWlvrSFIq05Mq1hUE2E1Y6Enh'
    OAUTH_TOKEN = "4877768477-iygFnDTiDCTQG8Gve9s2tKc0GNuTvApHkOYxbaz"
    OAUTH_TOKEN_SECRET = "l1rCfP1lZSiHK6I82PZRhIJdSjIujD2w0S64LXZNlhpwE"

    twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    f = ["AndreasBrommund","HadarGreinsmark","Borslampan","dprintz3","benlandis",
         "ugglapuggla","anderseriksson","Thenilsdc","DavidSkeppstedt","JacobOljemark",
         "S0fiaPetterss0n","SweClockers","AlvinRisk","TonyKungsholmen","Aftonbladet","MrMadhawk",
         "R_Fredriksson"]
    
    get_all_followers(twitter,f[14]) #14
    

def get_all_followers(conn,user):
    cursor = -1 #default cursor
        
    while cursor != 0:
        
        current_cursor = cursor

        try:
            response = conn.get_followers_ids(screen_name = str(user),cursor = cursor)

            for follower_id in response['ids']:
                print(follower_id)
                cursor = response['next_cursor']


        except TwythonRateLimitError:
            time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min
            cursor = current_cursor


    
main()
