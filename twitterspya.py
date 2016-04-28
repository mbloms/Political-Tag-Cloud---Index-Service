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


def readUserId():
    '''Läser argumenten från terminalen. "% a b" kommer bara behandla de userIds där (userId % a == b) dvs userId delat med a ska ge rest b.
    Om det inte getts några argument läser den bara allt, men strippar strängarna på whitespace.'''
    if not len(sys.argv)>1:
        return input()
    userId = input()
    while (userId % sys.argv[1] != sys.argv[2]):
        userId = input()
    return userId.strip()

def main():
    #variabel som används för att kolla hur många connections som testats innan skriptet sover.
    timeout = 1
    conn = CL.ConnectionList(filepath="config/access.conf")
    maxId = None
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
            response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId)
            while response == []:
                #Om tom respons skriv ut info till loggen (stderr)
                end = time.time()
                last = printcount
                print("User Id: " +'\t'+ str(userId.strip())+'\n', file=sys.stderr)
                print("Tweets: " +'\t'+ str(last - first), file=sys.stderr)
                print("Duration: " +'\t'+ str(end - start), file=sys.stderr)
                print("Total Fetched: " +'\t'+ str(last), file=sys.stderr)
                print("Timestamp: " +'\t'+ str(datetime.datetime.now()), file=sys.stderr)
                start = time.time()
                first = printcount
                #Läs nästa id, nollställ maxId och hämta ny respons.
                userId = readUserId()
                maxId = None
                response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId)

            for stuff in response:
                #skriv ut tweeten (och allt annat stuff som hör till) som ren json som man fick den från twitter. 
                print(json.dumps(stuff))
                #incrementera antalet nedladdade tweets.
                printcount += 1

            #Hämta bara tweets som ligger efter de sista tweetsen.
            maxId = response[-1]['id']-1

        except TwythonAuthError:
                    #Skriv ut dummy json vid privat konto. på det sättet får inte en jsonparser spasmer, men vi har fortfarande info om de kontona.
                    print('{"text": "privateaccount", "entities": {"symbols": [], "urls": [], "hashtags": [], "user_mentions": []}, "id": null, "user": {"id_str": "'+str(userId)+'", "id": '+str(userId)+'}, "created_at": null, "is_quote_status": false, "in_reply_to_user_id_str": null, "id_str": null, "lang": null, "place": null, "in_reply_to_user_id": null, "source": null, "in_reply_to_status_id_str": null}')
                    #Läs nästa
                    userId = readUserId()
                    maxId = None
                    
                    
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
        except EOFError:
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
            userId = readUserId()
            maxId = None

main()
