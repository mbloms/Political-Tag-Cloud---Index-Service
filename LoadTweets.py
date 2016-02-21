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

    def __str__(self):
        output = "ID: " + str(self.id) + " | userID: " + str(self.userId) + " | timestamp: " + str(self.timestamp) + \
                 " | content: " + str(self.content) + " | Hashtags: " + ' '.join(self.hashtags)
        return output

class LoadTweets:
    def __init__(self):
        self.db = Database.Database()
        self.conn = CL.ConnectionList(filepath="config/access.conf") 

    def jsonToTweet(self, userId,tweet):
        hashtags = []
        for hashtag in (tweet['entities']['hashtags']):
            hashtags.append(hashtag['text'])

        id = tweet['id']
        timestamp = tweet['created_at']
        content = tweet['text']

        return Tweet(id,userId,timestamp,content,hashtags)

    def getLastTweetId(self, userid):
        """Returns the latest twitter id,if the user does not exists or have not tweeted we return None"""
        self.db.cursor.execute("SELECT coalesce(tweetid,-1)AS tweetid FROM usr" +
                             " NATURAL LEFT JOIN tweet WHERE userid = %s ORDER BY TIMESTAMP DESC LIMIT 1"
                               ,(userid,))
        id = self.db.cursor.fetchone()
        if id == None:
            return None
        return id[0] if id[0] != -1 else None


    def getTweets(self,userId):

        maxId = None
        sinceId = self.getLastTweetId(userId)

        tweets = []

        while True:

            
            try:
                response = self.conn.connection().get_user_timeline(user_id = userId,
                                    count=200,include_rts = False, trim_user = True, max_id = maxId, since_id = sinceId)

                if response == []:
                    break

                for jsontw in response:
                    data = self.jsonToTweet(userId,jsontw)
                    try:
                        self.db.cursor.execute("INSERT INTO tweet(tweetId,userId,timestamp,content) VALUES (%s,%s,%s,%s)",
                                               (data.id,data.userId,data.timestamp,data.content,))
                    except: 
                        pass
                    finally:
                        self.db.commit()

                    for tag in data.hashtags:
                        print("Handling tag " + tag)
                        try:
                            self.db.cursor.execute("INSERT INTO tag(tag) VALUES (%s)",(tag,))
                        except:
                            pass
                        finally:
                            self.db.commit()

                        try:
                            self.db.cursor.execute("SELECT tagId FROM tag WHERE tag=%s",(tag,))
                        except:
                            pass

                        try:
                            self.db.cursor.execute("INSERT INTO tweettag(tweetId,tagId) VALUES (%s,%s)",
                                                   (data.id,self.db.cursor.fetchone()[0],))
                        except:
                            pass
                        finally:
                            self.db.commit()


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