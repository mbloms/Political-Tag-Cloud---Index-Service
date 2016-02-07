from twython import Twython

def newTwython(app_key,app_secret):
    """Creates a new instance of a twython object. Authorized with 
    Application-only authentication oauth2"""
    twitter = Twython(app_key,app_secret,oauth_version=2)
    twitter_access = Twython(app_key,access_token=twitter.obtain_access_token())
    return twitter_access 

