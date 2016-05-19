'''
    Skript för att hämta en eller flera användares tweets. 
    idn på konton läses från stdin och tweets skrivs ut till stdout.
'''

from requests.packages.urllib3 import response

#Jag gjorde ett försök med mys options och skit. Funkade inte. Importer behöver rensas.

import ConnectionList as CL
import json
from twython import Twython,TwythonRateLimitError,TwythonError,TwythonAuthError
import sys
import getopt
import datetime
import time
import io


sinceId = None

def readUserId():
    global sinceId
    userId = input().strip()
    if not userId[:1] == "(":
        sinceId = None
        return userId
    else:
        (a,b) = userId.split(",")
        userId = int(a[1:])
        sinceId = int(b[:-1])-1
        return userId

def main():
    if not len(sys.argv)>1:
        mess = ""
    else:
        mess = "Process: \t"+str(sys.argv[1])
    maxId = None
    global sinceId
    #variabel som används för att kolla hur många connections som testats innan skriptet sover.
    timeout = 1
    conn = CL.ConnectionList(filepath="config/access.conf")
    #Läs första idt från stdin.
    userId = readUserId()
    #Variabel som räknar antalet nedladdade tweets.
    printcount = 0
    #variabler för att skriva ut tidsstämplar.
    first = 0
    start = time.time()

    while True:
        try:
            #Hämta nästa respons
            response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId, since_id = sinceId)
            while response == []:
                #Om tom respons skriv ut info till loggen (stderr)
                end = time.time()
                last = printcount
                print("User Id: " +'\t'+ str(userId), file=sys.stderr)
                print("Tweets: " +'\t'+ str(last - first), file=sys.stderr)
                print("Duration: " +'\t'+ str(end - start), file=sys.stderr)
                print("Total Fetched: " +'\t'+ str(last), file=sys.stderr)
                print("Timestamp: " +'\t'+ str(datetime.datetime.now()), file=sys.stderr)
                print(mess+'\n', file=sys.stderr)

                start = time.time()
                first = printcount
                #Läs nästa id, nollställ maxId och hämta ny respons.
                maxId = None
                userId = readUserId()
                response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId, since_id = sinceId)

            for stuff in response:
                #skriv ut tweeten (och allt annat stuff som hör till) som ren json som man fick den från twitter. 
                print(json.dumps(stuff))
                #incrementera antalet nedladdade tweets.
                printcount += 1

            #Hämta bara tweets som ligger efter de sista tweetsen.
            maxId = response[-1]['id']-1

        except TwythonAuthError:
                    #Skriv ut dummy json vid privat konto. på det sättet får inte en jsonparser spasmer, men vi har fortfarande info om de kontona.
                    print('{"text": "privateaccount", "entities": {"symbols": [], "urls": [], "hashtags": [], "user_mentions": []}, "id": null, "user": {"id_str": "'+str(userId)+'", "id": null}, "created_at": null, "is_quote_status": false, "in_reply_to_user_id_str": null, "id_str": null, "lang": null, "place": null, "in_reply_to_user_id": null, "source": null, "in_reply_to_status_id_str": null}')
                    #Läs nästa
                    maxId = None
                    userId = readUserId()
                    
                    
        except TwythonRateLimitError as err:
            timeout += 1
            print("access "+str(conn.position())+" timed out.", file=sys.stderr)
            if timeout > conn.size():
                timeout = 1
                print(":(", file=sys.stderr)
                print(err, file=sys.stderr)
                print(datetime.datetime.now(), file=sys.stderr)
                time.sleep(60*15+60) #In sec. 60*15 = 15 min + 1min 
                print(":)", file=sys.stderr)
        except TwythonError as err: #Handel timeouts
            print("Error:", file=sys.stderr)
            print(err, file=sys.stderr)
            print(err.error_code, file=sys.stderr)
            print("User Id: " +'\t'+ str(userId), file=sys.stderr)
            if err.error_code == 404:
                maxId = None
                userId = readUserId()

        except EOFError as eof:
            print(eof, file=sys.stderr)
            break
        except Exception as other:
            #Vid annat felmeddelande skriv ut felmeddelandet som json så att det går att se i efterhand.
            #Meddelandet skrivs ut på en rad genom att alla newlines byts ut till '\\n'
            print(other, file=sys.stderr)
            print("{\"userId\":"+str(userId)+",\"maxId\":"+str(maxId)+" \"error\":\"")
            print(str(other).replace('\n',"\\n"))
            print("\"}")
            #Läs nästa
            maxId = None
            userId = readUserId()

main()
