import ConnectionList as CL
import json
from twython import Twython,TwythonRateLimitError,TwythonError,TwythonAuthError
import sys
import datetime
import time


def main():
    conn = CL.ConnectionList(filepath="config/access.conf")
    #Läs userid från stdin
    userId = input()
    cursor = -1
    while True:
        try:
            #Hämta respons
            response = conn.connection().get_followers_ids(user_id = userId,cursor = cursor)
            #Skriv ut info till stderr
            print("userId="+str(userId)+", cursor="+str(cursor), file=sys.stderr)

            #Skriv ut alla id till stdout
            for followerId in response['ids']:
                print(followerId)

            #Ställ in cursorn
            cursor = response['next_cursor']

            #När det inte finns mer att hämta.
            while response['next_cursor'] == 0:
                #Läs
                userId = input()
                #Nollställ cursor
                cursor = -1
                #hämta nästa respons
                response = conn.connection().get_followers_ids(user_id = userId,cursor = cursor)


        except TwythonAuthError:
                    print("Private account: userId", file=sys.stderr)
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
        #När End Of File: bryt ur while-loopen och avsluta.
        except EOFError as eof:
            print(eof, file=sys.stderr)
            break
        #Skriv ut andra fel till terminalen
        except Exception as other:
            print("Error.. userId="+userid+", cursor="+cursor, file=sys.stderr)
            print(other, file=sys.stderr)


main()