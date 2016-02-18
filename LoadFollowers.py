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
        #group[0] now contains name and [1] list of users
        for user in group[1]['users']:
            try:
                db.cursor.execute("INSERT INTO grp(groupid,name) VALUES (%s,%s)",(user,group[0],))
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
main()
