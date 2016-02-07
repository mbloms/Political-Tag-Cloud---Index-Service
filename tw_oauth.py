from twython import Twython

def generateAccessToken(app_key,app_secret):
    """Generates access token for a twhython object."""
    twitter = Twython(app_key,app_secret,oauth_version=2)
    return twitter.obtain_access_token()

def newTwython(app_key,access_token):
    """Creates a instance of an Twhython object authed with a access token"""
    return Twython(app_key,access_token=access_token)
