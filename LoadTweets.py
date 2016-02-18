from twython import Twython,TwythonRateLimitError,TwythonError,TwythonAuthError
import time
import ConnectionList as CL
import TwitterUsers as TU
import Database
import datetime
import json
 
class Tweet:
    def __init__(self,id,userId,timestamp,content,hashtags):
        self.id = id
        self.userId = userId
        self.timestamp = timestamp
        self.content = content
        self.hashtags = hashtags

def main():
    print("Started at:"+str(datetime.datetime.now()))
    db = Database.Database()
    conn = CL.ConnectionList(filepath="config/access.conf") 
    db.cursor.execute("SELECT usr.userid FROM usr JOIN useringroup ON usr.userid = useringroup.userid JOIN grp ON useringroup.groupid = grp.groupid WHERE name = 'Kristdemokraterna'")
    i = 0
    for userid in db.cursor.fetchall():
        i += 1
        print("User nr:"+str(i))
        start = time.time()
        getTweets(userid[0],db,conn)
        end = time.time()
        print("Duration:"+str(end-start))
        print("---")

def jsonToTweet(userId,tweet):
    hashtags = []
    for hashtag in (tweet['entities']['hashtags']):
        hashtags.append(hashtag['text'])

    id = tweet['id']
    timestamp = tweet['created_at']
    content = tweet['text']

    return Tweet(id,userId,timestamp,content,hashtags)

def getLastTweetId(userid,db):
    """Returns the latest twitter id,if the user does not exists or have not tweeted we return None"""
    db.cursor.execute("SELECT coalesce(tweetid,-1)AS tweetid FROM usr" +
                                         " NATURAL LEFT JOIN tweet WHERE userid = %s ORDER BY TIMESTAMP DESC LIMIT 1",(userid,))
    id = db.cursor.fetchone()
    if id == None:
        return None
    return id[0] if id[0] != -1 else None

def getTweets(userId,db,conn):

    maxId = None
    tweets = []

    while True:

        
        try:
            response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = False, trim_user = True, max_id = maxId)

            if response == []:
                break

            for jsontw in response:
                data = jsonToTweet(userId,jsontw)

                try:
                    db.cursor.execute("INSERT INTO tweet(tweetId,userId,timestamp,content) VALUES (%s,%s,%s,%s)",(data.id,data.userId,data.timestamp,data.content,))
                except: 
                    pass
                finally:
                    db.commit()


                try:
                    for tag in data.hashtags:
                        db.cursor.execute("INSERT INTO tweettag(tweetId,tag) VALUES (%s,%s)",(data.id,tag,))
                except: 
                    pass
                finally:
                    db.commit()


                maxId = data.id-1
    
                        
        except TwythonAuthError:
            print("Private account")
            #Add to blacklist
            break
            
        except TwythonRateLimitError as err:
            print(":(")
            print(err)
            print(datetime.datetime.now())
            time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min 
            print(":)")  
        except TwythonError as err: #Handel timeouts
            print("Error:")
            print(err)
main()
