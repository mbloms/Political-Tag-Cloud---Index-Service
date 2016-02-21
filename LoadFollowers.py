from twython import TwythonRateLimitError,TwythonError
import time
import ConnectionList as CL
import TwitterUsers as TU
import Database
import datetime
import sys

class LoadFollowers():
    def __init__(self, tempTableName = "followingTemp"):
        print("Initializing LoadFollowers with temporary table " + tempTableName)
        self.conn = CL.ConnectionList(filepath="config/access.conf") 
        self.db = Database.Database()
        self.tempTableName = tempTableName

        # Create temp table for follows
        try:
            self.db.cursor.execute("CREATE TABLE %s(followedId BIGINT REFERENCES usr(userId),followerId BIGINT REFERENCES usr(userId),PRIMARY KEY(followedId, followerId))"  % (tempTableName))
        except:
            pass
        finally:
            self.db.commit()

    def close(self):
        self.db.close()

    def getUsersFollowers(self):
        print("Start fetching users")
        users = TU.TwitterUsers()
        
        for group in users.getGroups():
            print("Working with group " + group[0])
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
            
            try:
                for user in group[1]['users']:
                    try:
                        self.db.cursor.execute("INSERT INTO usr(userId) VALUES (%s)",(user,))
                    except:
                        pass
                    finally:
                        self.db.commit()
                    # Fetch groupId from DB
                    self.db.cursor.execute("SELECT groupId FROM grp WHERE name = %s", (group[0],))
                    groupId = self.db.cursor.fetchone()[0]

                    try:
                        self.db.cursor.execute("INSERT INTO userInGroup(groupId, userId) VALUES (%s, %s)",(groupId, user,))
                    except:
                        pass
                    finally:
                        self.db.commit()
                    self.getFollowers(user)
            except KeyboardInterrupt:
                print("KeyboardInterrupt catched, running the calculateFollowingDiffAndClean method before shutdown")
                self.calculateFollowingDiffAndClean()
                sys.exit(0)
        self.calculateFollowingDiffAndClean()


    """Get all followers from a specifik twitter user and and the follower to the database"""
    def getFollowers(self, followedId):

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
                        #Need the weird syntax
                        #Link: http://stackoverflow.com/questions/9354392/psycopg2-cursor-execute-with-sql-query-parameter-causes-syntax-error
                        self.db.cursor.execute("INSERT INTO %s(followedId,followerId) VALUES (%s,%s)" % (self.tempTableName, "%s", "%s"),(followedId,followerId,))

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

    def calculateFollowingDiffAndClean(self):
        """
            A method that caluclates which users that have stopped following and started following 
            each other and puts this information in corresonding relations as well as deleting the 
            temporary table after these calculations are done
        """
        print("Calculating new followers...")
        # Caluclate new followers
        self.db.cursor.execute("(SELECT followedId, followerId FROM " + self.tempTableName + ") EXCEPT (SELECT followedId, followerId FROM following)")
        for follows in self.db.cursor.fetchall():
            self.db.cursor.execute("INSERT INTO startfollow(followedId, followerId) VALUES (%s, %s)", (follows[0], follows[1]))
        self.db.commit()
        print("Calculating unfollows...")
        # Caluclate unfollows
        self.db.cursor.execute("(SELECT followedId, followerId FROM following) EXCEPT (SELECT followedId, followerId FROM " + self.tempTableName + ")")
        for unfollows in self.db.cursor.fetchall():
            self.db.cursor.execute("INSERT INTO unfollow(followedId, followerId) VALUES (%s, %s)", (unfollows[0], unfollows[1]))
        self.db.commit()
        print("Deleting and renaming table")
        # Delete temporary table by deleting the old one and renaming the temporary one
        self.db.cursor.execute("DROP TABLE following")
        self.db.commit()
        self.db.cursor.execute("ALTER TABLE " + self.tempTableName + " RENAME TO following")
        self.db.commit()
        print("It is almost as clean as my bedroom, thank you!")
