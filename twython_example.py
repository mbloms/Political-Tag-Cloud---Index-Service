# Using Twithon, install with sudo pip3 install twython
from twython import Twython,TwythonRateLimitError
import json
import time

def main():
    APP_KEY = 'PcVBQSI6dxa6FeVP8uuanEK0V'
    APP_SECRET = 'jt03KeTK1yivxfKXzK9CDxyKj7tGrd5VIcUF846dO0jwxBuqW8'
    OAUTH_TOKEN = "3221674156-AffFW5MZDq9NVcEPB7gIuqDsj5xDHZjNnoiunsE"
    OAUTH_TOKEN_SECRET = "Nl4SOOWr2aqeLgX9CrkeTRIrkfNO6vIsLBwoe3J6ozp6m"

    twitter = Twython(APP_KEY, APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    f = ["AndreasBrommund","HadarGreinsmark","Borslampan","dprintz3","benlandis",
         "ugglapuggla","anderseriksson","Thenilsdc","DavidSkeppstedt","JacobOljemark",
         "S0fiaPetterss0n","SweClockers","AlvinRisk","TonyKungsholmen","MrMadhawk",
         "R_Fredriksson"]
    
    get_all_followers(twitter,f[14])



def get_all_followers(twitter,user):
    cursor = -1 #default cursor
        
    while cursor != 0:
        response = twitter.get_followers_ids(screen_name = str(user),cursor = cursor)
        for follower_id in response['ids']:
            print(follower_id)
        cursor = response['next_cursor']


main()
