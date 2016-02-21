from twython import Twython,TwythonRateLimitError,TwythonError,TwythonAuthError
import time
import ConnectionList as CL
import TwitterUsers as TU
import Database
import datetime
import json
 
class Tweet:
    def __init__(self,id,userId,timestamp,content,hashtags,mentions,retweet):
        self.id = id
        self.userId = userId
        self.timestamp = timestamp
        self.content = content
        self.hashtags = hashtags
        self.mentions = mentions
        self.retweet = retweet

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

        retweet = None
        if(tweet['retweeted']): # This is a retweeted tweet, store info about original
            retweet = []
            retweet['creatorId'] = tweet['retweeted_status']['user']['id']
            retweeet['originalTweetId'] = tweet['retweeted_status']['id']
           
        mentions = [] 
        for mention in (tweet['entities']['user_mentions']):
            mentions.append(mention['id'])

        id = tweet['id']
        timestamp = tweet['created_at']
        content = tweet['text']

        return Tweet(id,userId,timestamp,content,hashtags,mentions,retweet)

    def getLastTweetId(self, userid):
        """Returns the latest twitter id,if the user does not exists or have not tweeted we return None"""
        self.db.cursor.execute("SELECT coalesce(MAX(tweetid),-1)AS tweetid FROM usr NATURAL LEFT JOIN tweet "+
                               "WHERE userid = 341958765",(userid))
        id = self.db.cursor.fetchone()
        if id == None:
            return None
        return id[0] if id[0] != -1 else None

    def hashtagHelper(self, data):
        """ Fetch hashtags from data and add the sufficient relations """
        for tag in data.hashtags:
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
                tagId = self.db.cursor.fetchone()[0]
                self.db.cursor.execute("INSERT INTO tweettag(tweetId,tagId) VALUES (%s,%s)",(data.id,tagId,))
            except:
                pass
            finally:
                self.db.commit()

    def mentionHelper(self, data):
        """ Fetch mentions from data and add the sufficient relations """
        for mention in data.mentions:
            try:
                self.db.cursor.execute("INSERT INTO tweetMention(tweetId,userId) VALUES (%s,%s)",(data.id,mention,))
            except:
                pass
            finally:
                self.db.commit()

    def retweetHelper(self, data):
        """ Fetch retweet info from data and add the sufficient relations """
        retweet = data.retweet
        if retweet != None:
            print("This is a retweeted tweet")
            try:
                self.db.cursor.execute("INSERT INTO retweet(tweetId,creatorId,originalTweetId) VALUES (%s,%s)",(data.id,retweet.creatorId, retweet.originalTweetId,))
            except:
                pass
            finally:
                self.db.commit()


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
                    self.hashtagHelper(data)
                    self.mentionHelper(data)
                    self.retweetHelper(data)

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