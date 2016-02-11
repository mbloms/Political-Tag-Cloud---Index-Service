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
    db = Database.Database()
    conn = CL.ConnectionList(filepath="config/access.conf") 
    db.cursor.execute("SELECT usr.userid FROM usr JOIN useringroup ON usr.userid = useringroup.userid JOIN grp ON useringroup.groupid = grp.groupid WHERE name = 'Kristdemokraterna'")
    i = 0
    for userid in db.cursor.fetchall():
        i += 1
        print(userid[0])
        print(i)
        start = time.time()
        getTweets(userid[0],db,conn)
        end = time.time()
        print("Time 1:"+str(end-start))
        print("---")

def jsonToTweet(userId,tweet):
    hashtags = []
    for hashtag in (tweet['entities']['hashtags']):
        hashtags.append(hashtag['text'])

    id = tweet['id']
    timestamp = tweet['created_at']
    content = tweet['text']

    return Tweet(id,userId,timestamp,content,hashtags)

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
            print("nop")
            #Add to blacklist
            break
            
        except TwythonRateLimitError as err:
            print(":(")
            print(err)
            print(datetime.datetime.now())
            time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min 
            print(":)")  
        except TwythonError as err: #Handel timeouts
            print("Timeout?")
            print(err)
main()
