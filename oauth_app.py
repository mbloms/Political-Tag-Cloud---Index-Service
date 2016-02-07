import base64
import requests
import json
def generateOAuthAccessToken():
    CONSUMER_KEY = "CF55V4vi3yZvpWCfYt38SMu1I"
    CONSUMER_SECRET = "0SW8HZ570dA5eO3YmF6ZssQCk1KqWZ3wFYrEvq2GWBHT91dQXk"
    bearer = CONSUMER_KEY + ":" + CONSUMER_SECRET
    bearer64 = stringToBase64(bearer) 

    #https://api.twitter.com/oauth2/token
    my_headers = {"Authorization":"Basic " + bearer64.decode("utf-8"),
            "Content-Type":"application/x-www-form-urlencoded;charset=UTF-8"} 
    r = requests.post("https://api.twitter.com/oauth2/token",data = "grant_type=client_credentials",headers = my_headers)

    response = r.json()
    token_type = response['token_type']
    access_token = response['access_token']

    return access_token


def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))
def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

def lookAtTimeline(token):
    #https://api.twitter.com/1.1/statuses/user_timeline.json
    my_headers = {"Authorization":"Bearer "+token}
    r = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?count=100&screen_name=twitterapi",headers = my_headers)
    print(r.text)


lookAtTimeline(generateOAuthAccessToken())
    
