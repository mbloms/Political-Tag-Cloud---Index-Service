from twython import TwythonRateLimitError,TwythonError
import time
import ConnectionList as CL
import TwitterUsers as TU
import Database
import datetime

class LoadFollowers():
    def __init__(self):
        self.conn = CL.ConnectionList(filepath="config/access.conf") 
        self.db = Database.Database()
     
        getUsersFollowers()

        self.db.close()

    def getUsersFollowers(self):
        users = TU.TwitterUsers()
        
        for group in users.getGroups():
            # group[0] now contains name and [1] list of users
            # First, add the group to the database
            try:
                self.db.cursor.execute("INSERT INTO grp(name) VALUES (%s)",(group[0],))
            except:
                pass
            finally:
                self.db.commit()
            # Fetch groupId from DB
            self.db.cursor.execute("SELECT groupId FROM grp WHERE name = %s", (group[0],))
            groupId = self.db.cursor.fetchone()[0]

            # Now, for each user, add it to the database along with the group relation
            for user in group[1]['users']:
                try:
                    self.db.cursor.execute("INSERT INTO usr(userId) VALUES (%s)",(user,))
                    self.db.cursor.execute("INSERT INTO userInGroup(groupId, userId) VALUES (%s, %s)",(groupId, user,))
                except:
                    pass 
                finally:
                    self.db.commit()

                self.getFollowers(user)

    """Get all followers from a specifik twitter user and and the follower to the database"""
    def getFollowers(self,followedId):

        cursor = -1 #default cursor
            
        while cursor != 0: #No more pages
            
            try:
                response = self.conn.connection().get_followers_ids(user_id = followedId,cursor = cursor)
                
                for followerId in response['ids']:
                    try:
                        self.db.cursor.execute("INSERT INTO usr(userid) VALUES (%s)",(followerId,))
                    except: 
                        pass
                    finally:
                        self.db.commit()
                        
                    try:
                        self.db.cursor.execute("INSERT INTO following(followedId,followerId) VALUES (%s,%s)",(followedId,followerId))
                    except:
                        pass
                    finally:
                        self.db.commit()
                        
                    cursor = response['next_cursor'] 
            except TwythonRateLimitError as err:
                print(":(")
                print(err)
                print(datetime.datetime.now())
                time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min 
                print(":)")  
            except TwythonError as err: #Handel timeouts
                print("Timeout?")
                print(err)
