from twython import TwythonRateLimitError,TwythonError
import time
import ConnectionList as CL
import TwitterUsers as TU
import Database
import datetime

def main():

    conn = CL.ConnectionList(filepath="config/access.conf") 
    db = Database.Database()
    tempTableName = "followingTemp"

    #Need the weird syntax
    #Link: http://stackoverflow.com/questions/9354392/psycopg2-cursor-execute-with-sql-query-parameter-causes-syntax-error
    try:
        db.cursor.execute("CREATE TABLE %s(followedId BIGINT REFERENCES usr(userId),followerId BIGINT REFERENCES usr(userId),PRIMARY KEY(followedId, followerId))"  % (tempTableName))
    except:
        pass
    finally:
        db.commit()

    getUsersFollowers(db,conn,tempTableName)
    db.close()

def getUsersFollowers(db,conn,tempTableName):


    #Create the new tempdatabse
    try:
        db.cursor.execute("CREATE TABLE a",(tempTableName))
    except:
        pass
    finally:
        db.commit()

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

            getFollowers(user,db,conn,tempTableName)

"""Get all followers from a specifik twitter user and and the follower to the database"""
def getFollowers(followedId,db,conn,tempTableName):

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
                    #Need the weird syntax
                    #Link: http://stackoverflow.com/questions/9354392/psycopg2-cursor-execute-with-sql-query-parameter-causes-syntax-error
                    db.cursor.execute("INSERT INTO %s(followedId,followerId) VALUES (%s,%s)" % (tempTableName, "%s", "%s"),(followedId,followerId,))
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
main()
