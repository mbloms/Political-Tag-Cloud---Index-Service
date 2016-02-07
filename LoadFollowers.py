from twython import Twython,TwythonRateLimitError
import time
import ConnectionList as CL
import Database

def main():
    
    f = ["socialdemokrat",
         "vansterpartiet",
         "miljopartiet",
         "sdriks",
         "nya_moderaterna",
         "liberalerna",
         "kdriks",
         "Centerpartiet"]
   
    db = Database.Database()

    getUsersFollowers(f,db)    
  
    db.close()

def getUsersFollowers(users,db):
    for u in users:
        try:
            db.cursor.execute("INSERT INTO grp(name) VALUES (%s)",(u,))
        except:
            pass 
        finally:
            db.commit()
        getFollowers(u,db)

def getFollowers(user,db):
    conn = CL.ConnectionList(filepath="config/access.conf") 

    cursor = -1 #default cursor
        
    while cursor != 0:
        
        try:
            response = conn.connection().get_followers_ids(screen_name = str(user),cursor = cursor)
            
            for followerId in response['ids']:
                try:
                    db.cursor.execute("INSERT INTO usr(userid) VALUES (%s)",(followerId,))
                except:
                    pass
                finally:
                    db.commit()
                cursor = response['next_cursor']
        except TwythonRateLimitError:
            print(":(")
            time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min 
            print(":)")
        except TwythonError as err:
            print(err)
            
main()
