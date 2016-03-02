from requests.packages.urllib3 import response

import ConnectionList as CL
import json
from twython import Twython,TwythonRateLimitError,TwythonError,TwythonAuthError
import sys
import getopt
import datetime
import time
import io

inputfile = sys.stdin
outputfile = sys.stdout

def readUserId(flags):
    if not ('-m' in flags and '-r' in flags):
        return readHelper(flags)
    userId = inputfile.readline()
    while (userId % flags['-m'] != flags['-r']) or (userId < flags['-s']):
        userId = inputfile.readline()
    return userId.strip()

def badUserId(flags, userId):
    '''mer för läsbarhet än något annat, används inte just nu...'''
    return (userId % flags['-m'] != flags['-r']) or (userId < flags['-s'])

def main():
    try:
        opts, args = getopt.getopt(sys.argv,"s:m:r:i:o:d:T")
    except getopt.GetoptError:
        print('-s <minimum userId> -m <modulo> -r <rest>; -i <inputfile> -o <outputfile> -d <dump hashtags to file> -T (Trunctate file)', file=sys.stderr) #(-w <väntetid vid limit>) -t <försök vid limit>
    flags = {}
    for opt, arg in opts:
        flags[opt] = arg
    timeout = 1
    conn = CL.ConnectionList(filepath="config/access.conf")
    if '-t' in flags:
        TRIES = flags['-t']
    else:
        TRIES = conn.size()
    if '-i' in flags:
        inputfile=open(flags['-i'])
    if '-T' in flags:
        writeMode = 'w'
    else:
        writeMode = 'a'
    if '-o' in flags:
        outputfile=open(flags['-o'], 'a')
    print(flags)
    maxId = None
    userId = readUserId(flags)
    printcount = 0
    first = 0
    start = time.time()
    while True:
        try:
            response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId)
            while response == []:
                end = time.time()
                last = printcount
                print("User Id: " +'\t'+ str(userId.strip())+'\n', file=sys.stderr)
                print("Tweets: " +'\t'+ str(last - first), file=sys.stderr)
                print("Duration: " +'\t'+ str(end - start), file=sys.stderr)
                print("Total Fetched: " +'\t'+ str(last), file=sys.stderr)
                print("Timestamp: " +'\t'+ str(datetime.datetime.now()), file=sys.stderr)
                start = time.time()
                first = printcount
                userId = readUserId(flags)
                maxId = None
                response = conn.connection().get_user_timeline(user_id = userId,count=200,include_rts = True, trim_user = True, max_id = maxId)

            for stuff in response:
                print(json.dumps(stuff), file=outputfile)
                if '-d' in flags:
                    dumpfile = open(flags['-d'], 'a')
                    for hashtag in stuff['entities']['hashtags']
                        print(hashtag, file=dumpfile)
                    dumpfile.close()
                printcount += 1


            maxId = response[-1]['id']-1

        except TwythonAuthError:
                    print('{"text": "privateaccount", "entities": {"symbols": [], "urls": [], "hashtags": [], "user_mentions": []}, "id": null, "user": {"id_str": "'+str(userId)+'", "id": '+str(userId)+'}, "created_at": null, "is_quote_status": false, "in_reply_to_user_id_str": null, "id_str": null, "lang": null, "place": null, "in_reply_to_user_id": null, "source": null, "in_reply_to_status_id_str": null}')
                    userId = readUserId(flags)
                    maxId = None
                    
                    
        except TwythonRateLimitError as err:
            timeout += 1
            print("access "+str(conn.position())+" timed out.", file=sys.stderr)
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
            break
        except Exception as other:
            print(other, file=sys.stderr)
            print("{\"userId\":"+str(userId)+",\"maxId\":"+str(maxId)+" \"error\":\"")
            print(str(other).replace('\n',"\\n"))
            print("\"}")
            userId = readUserId(modMode)
            maxId = None

main()