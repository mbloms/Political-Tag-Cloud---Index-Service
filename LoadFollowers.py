from twython import TwythonRateLimitError,TwythonError
import time
import ConnectionList as CL
import TwitterUsers as TU
import Database
import datetime

def main():

    conn = CL.ConnectionList(filepath="config/access.conf") 
    db = Database.Database()
 
    getUsersFollowers(db,conn)

    db.close()

def getUsersFollowers(db,conn):
    users = TU.TwitterUsers()
    
    for group in users.getGroups():
        # group[0] now contains name and [1] list of users
        # First, add the group to the database
        try:
            db.cursor.execute("INSERT INTO grp(name) VALUES (%s)",(group[0],))
        except:
            pass
        finally:
            db.commit()
        # Fetch groupId from DB
        db.cursor.execute("SELECT groupId FROM grp WHERE name = %s", (group[0],))
        groupId = db.cursor.fetchone()[0]

        # Now, for each user, add it to the database along with the group relation
        for user in group[1]['users']:
            try:
                db.cursor.execute("INSERT INTO usr(userId) VALUES (%s)",(user,))
            except:
                pass 
            finally:
                db.commit()
            # Now store data that this user follows the group
            try:
                db.cursor.execute("INSERT INTO userInGroup(groupId, userId) VALUES (%s, %s)",(groupId, user,))
            except:
                pass
            finally:
                db.commit()

            getFollowers(user,db,conn)

"""Get all followers from a specifik twitter user and and the follower to the database"""
def getFollowers(followedId,db,conn):

    cursor = -1 #default cursor
        
    while cursor != 0: #No more pages
        
        try:
            response = conn.connection().get_followers_ids(user_id = followedId,cursor = cursor)
            
            for followerId in response['ids']:
                try:
                    db.cursor.execute("INSERT INTO usr(userid) VALUES (%s)",(followerId,))
                except: 
                    pass
                finally:
                    db.commit()
                    
                try:
                    db.cursor.execute("INSERT INTO following(followedId,followerId) VALUES (%s,%s)",(followedId,followerId))
                except:
                    pass
                finally:
                    db.commit()
                    
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

def calculateFollowingDiffAndClean(tempTableName):
    """
        A method that caluclates which users that have stopped following and started following 
        each other and puts this information in corresonding relations as well as deleting the 
        temporary table after these calculations are done
    """
    # Caluclate new followers
    db.cursor.execute("(SELECT followedId, followerId FROM " + tempTableName + ") DIVIDE (SELECT followedId, followerId FROM following)")
    for follows in db.cursor.fetchall():
        db.cursor.execute("INSERT INTO startfollow(followedId, followerId) VALUES (%s, %s)", (unfollows[0], unfollows[1]))
    db.commit()

    # Caluclate unfollows
    db.cursor.execute("(SELECT followedId, followerId FROM following) DIVIDE (SELECT followedId, followerId FROM " + tempTableName + ")")
    for unfollows in db.cursor.fetchall():
        db.cursor.execute("INSERT INTO unfollow(followedId, followerId) VALUES (%s, %s)", (unfollows[0], unfollows[1]))
    db.commit()
    # Delete temporary table by deleting the old one and renaming the temporary one
    db.cursor.execute("DROP TABLE following")
    db.commit()
    db.cursor.execute("ALTER TABLE " + tempTableName + " RENAME TO following")
    db.commit()
main()
