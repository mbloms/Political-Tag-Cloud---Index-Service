import ConnectionList as CL
import json
from twython import Twython,TwythonRateLimitError,TwythonError,TwythonAuthError
import sys
import datetime
import time


def main():
    conn = CL.ConnectionList(filepath="config/access.conf")
    userId = input()
    #if len(sys.argv) != 0:
    #    while(sys.argv[0]!=userId):
    #            userId = input()
    maxId = None
    printcount = 0
    first = 0
    start = time.time()
    while True:
        try:
            response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId)
            while response == []:
                end = time.time()
                last = printcount
                print("Duration: " + str(end - start), file=sys.stderr)
                print("Tweets: " + str(last - first), file=sys.stderr)
                start = time.time()
                first = printcount
                userId = input()
                maxId = None
                response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId)

            for stuff in response:
                print(stuff)
                printcount += 1
                #if(printcount%1000==0):
                #    print(printcount, file=sys.stderr)



            maxId = response[-1]['id']-1

        except TwythonAuthError:
                    print("{'privateaccount':"+str(userId)+"}")
                    userId = input()
                    maxId = None
                    
                    
        except TwythonRateLimitError as err:
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
            userId = input()
            maxId = None

main()