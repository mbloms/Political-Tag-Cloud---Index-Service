from twython import Twython,TwythonAuthError
import sys

def newTwython(app_key,app_secret):
    """Creates a new instance of a twython object. Authorized with 
    Application-only authentication oauth2"""
    twitter = Twython(app_key,app_secret,oauth_version=2)
    try:
        twitterAccess = Twython(app_key,access_token=twitter.obtain_access_token())
    except TwythonAuthError:
        print("Something went wrong when trying to obtain the acces token", file=sys.stderr)
        return False
    return twitterAccess 

