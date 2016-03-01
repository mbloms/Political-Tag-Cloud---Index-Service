import ConnectionList as CL
import json
from twython import Twython,TwythonRateLimitError,TwythonError,TwythonAuthError
import sys
import datetime
import time

def readUserId(modMode):
    if not modMode:
        return input()

    userId = input()
    while (userId % sys.argv[1] != sys.argv[2]):
        userId = input()
    return userId

def main():
    TRIES = 10
    timeout = 1
    conn = CL.ConnectionList(filepath="config/access.conf")
    modMode = False
    if len(sys.argv) != 0 and sys.argv[0]=='%':
        modMode = True
    maxId = None
    userId = readUserId(modMode)
    printcount = 0
    first = 0
    start = time.time()
    while True:
        try:
            response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId)
            while response == []:
                end = time.time()
                last = printcount
                print("User Id: " +'\t'+ str(userId.strip()), file=sys.stderr)
                print("Tweets: " +'\t'+ str(last - first), file=sys.stderr)
                print("Duration: " +'\t'+ str(end - start)+'\n', file=sys.stderr)
                start = time.time()
                first = printcount
                userId = readUserId(modMode)
                maxId = None
                response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId)

            for stuff in response:
                print(stuff)
                printcount += 1

            maxId = response[-1]['id']-1

        except TwythonAuthError:
                    print("{'privateaccount':"+str(userId)+"}")
                    userId = readUserId(modMode)
                    maxId = None
                    
                    
        except TwythonRateLimitError as err:
            timeout += 1
            if timeout > TRIES:
                timeout = 1
                print(":(", file=sys.stderr)
                print(err, file=sys.stderr)
                print(datetime.datetime.now(), file=sys.stderr)
                time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min 
                print(":)", file=sys.stderr)
        except TwythonError as err: #Handel timeouts
            print("Error:", file=sys.stderr)
            print(err, file=sys.stderr)
        except EOFError:
            print(eof, file=sys.stderr)
        except Exception as other:
            print(other, file=sys.stderr)
            print("{'userId':"+str(userId)+",'maxId':"+str(maxId)+" 'error':'")
            print(other)
            print("'}")
            userId = readUserId(modMode)
            maxId = None

main()