from twython import Twython,TwythonRateLimitError
import time
import ConnectionList as cl
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
        getFollowers(u,db)


def getFollowers(user,db):
    conn = cl.ConnectionList(filepath="config/access.conf") 

    cursor = -1 #default cursor
        
    while cursor != 0:
        
        currentCursor = cursor

        try:
            response = conn.connection().get_followers_ids(screen_name = str(user),cursor = cursor)
            
            for followerId in response['ids']:
                try:
                    db.cursor().execute("INSERT INTO usr VALUES (%s)",(followerId,))
                    db.commit()
                except:
                    print("dup")
                    
                cursor = response['next_cursor']


        except TwythonRateLimitError:
            time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min
            cursor = currentCursor


    
main()
