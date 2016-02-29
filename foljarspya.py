import ConnectionList as CL
import json
from twython import Twython,TwythonRateLimitError,TwythonError,TwythonAuthError
import sys
import datetime
import time


def main():
    conn = CL.ConnectionList(filepath="config/access.conf")
    userId = input()
    cursor = -1
    while True:
        try:
            response = conn.connection().get_followers_ids(user_id = userId,cursor = cursor)
            print("userId="+str(userId)+", cursor="+str(cursor), file=sys.stderr)

            for followerId in response['ids']:
                print(followerId)

            cursor = response['next_cursor']

            while response['next_cursor'] == 0:
                userId = input()
                cursor = -1
                response = conn.connection().get_followers_ids(user_id = userId,cursor = cursor)

        except TwythonAuthError:
                    print("Private account", file=sys.stderr)
                    #Add to blacklist
                    break
                    
        except TwythonRateLimitError as err:
            print(":(", file=sys.stderr)
            print(err, file=sys.stderr)
            print(datetime.datetime.now(), file=sys.stderr)
            time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min 
            print(":)", file=sys.stderr)
        except TwythonError as err: #Handel timeouts
            print("Error:", file=sys.stderr)
            print(err, file=sys.stderr)
        except EOFError as eof:
            print(eof, file=sys.stderr)
            break
        except Exception as other:
            print("Error.. userId="+userid+", cursor="+cursor, file=sys.stderr)
            print(other, file=sys.stderr)


main()