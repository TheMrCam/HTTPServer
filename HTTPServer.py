from netTools import *
import threading
from threading import *
import time
import random

binaryFiles = ["jpg","bmp","gif","png","ico"]
asciiFiles = ["html","txt","ss235"]
TypeExpand = {"html" :"text/html",
              "txt"  :"text/text",
              "ss235":"text/html",
              "jpg"  :"image/jpeg",
              "bmp"  :"image/bitmap",
              "gif"  :"image/GIF",
              "png"  :"image/PNG",
              "ico"  :"image/ICO"}

def processRequest(s, addr, l):
    request = getMessage(s)
    print("#"*25)
    print(request)
    print("#"*25)
###########################################
    if request[:3] == "GET":
        request = request[4:]
        spaceLoc = request.find(" ")
        resource = request[:spaceLoc]
        resource = resource.strip("/")
        endLoc = resource.rfind("?")
        data = ""
        if(endLoc == -1):
            mediaType = resource[resource.rfind(".")+1:]
        else:
            mediaType = resource[resource.rfind(".")+1:endLoc]
            data = resource[endLoc+1:]
            resource = resource[:endLoc]
        #print("DEBUG:",mediaType)
        #print("DEBUG:",data)

        #ascii files
        #if resource[-4:].lower() == "html":
        if mediaType in asciiFiles:
            try:
                inFile = open(resource, "r")
            except:
                response = "HTTP/1.0 404 Not Found\n\n"
                response += "Resource not found\n"
                s.send(response.encode("ascii"))
            else:
                response = "HTTP/1.0 200 OK\n"
                response += "Content-Type: "+TypeExpand[mediaType]+"\n"
                response += "\n"
                response += inFile.read()
                if mediaType == "ss235":
                    try:
                        replaces = {}
                        info = data.split("&")
                        for pair in info:
                            k, v = pair.split("=",1)
                            replaces[k] = v
                        #####
                        if resource == "vote.ss235":
                            print("HERE!")
                            f = open("votes.txt", "r")
                            votetotals = f.readlines()
                            f.close()
                            print("votetotals = "+votetotals)
                            replaces["$SWVotes"] = votetotals[0]
                            replaces["$STVotes"] = votetotals[1]
                            if "StarWars" in replaces.values():
                                replaces["$SWVotes"] = replaces["$SWVotes"] + 1
                            elif "StarTrek" in replaces.values():
                                replaces["$STVotes"] = replaces["$STVotes"] + 1
                            f = open("votes.txt", "w")
                            f.write(replaces["$SWVotes"]+"\n")
                            f.write(replaces["$STVotes"])
                            f.close()
                        #####
                        #print(replaces)
                        for key in replaces.keys():
                            response = response.replace(key, replaces[key])
                    except:
                        print("Error with replacements")
                    finally:
                        pass
                s.send(response.encode("ascii"))

        #binary files
        #elif resource[-3:].lower() == "jpg":
        elif mediaType in binaryFiles:
            try:
                inFile = open(resource, "rb")
            except:
                response = "HTTP/1.0 404 Not Found\n\n"
                response += "Resource not found\n"
                s.send(response.encode("ascii"))
            else:
                response = "HTTP/1.0 200 OK\n"
                response += "Content-Type: "+TypeExpand[mediaType]+"\n"
                response += "\n"
                s.send(response.encode("ascii"))
                #infile = open(resource, "rb")
                s.send(inFile.read())
        else:
            response = "HTTP/1.0 403 Forbidden\n\n"
            response += "Resource type not allowed\nCheck URL spelling\n"
            s.send(response.encode("ascii"))

###########################################

    elif request[:4] == "POST":
        request = request[5:]
        resource = request[:request.find(" ")].strip("/")
        mediaType = resource[resource.rfind(".")+1:]
        data = request[request.find("\r\n\r\n")+4:]

        try:
            inFile = open(resource, "r")
        except:
            response = "HTTP/1.0 404 Not Found\n\n"
            response += "Resource not found\n"
            s.send(response.encode("ascii"))
        else:
            #print(f"{'='*25}\nRequest:{request}\nResource:{resource}\nInfo:{data}\n{'='*25}")
            response = "HTTP/1.0 200 OK\n"
            response += "Content-Type: "+TypeExpand[mediaType]+"\n"
            response += "\n"

            inFile = open(resource, "r")
            response += inFile.read()
            inFile.close()
            #if mediaType == "ss235":
            #replaces = {}
            #info = data.split("&")
            #for pair in info:
            #    k, v = pair.split("=",1)
            #    replaces[k] = v
            #print(replaces)
            #for key in replaces.keys():
            #    response = response.replace(key, replaces[key])
            #s.send(response.encode("ascii"))
            #try:
            replaces = {}
            info = data.split("&")
            print("Data:", data)
            print("Info:", info)
            for pair in info:
                k, v = pair.split("=",1)
                replaces[k] = v
            print(resource)
            print("1",replaces)
            if resource == "vote.ss235":
                print("HERE 1")
                #f = open("votes.txt", "r")
                #votetotals = f.readlines()
                #f.close()
                with open("votes.txt", 'r') as f:
                    for line in f:
                        votetotals = line.strip().split(" ",1)
                print("HERE 2\nVote totals:",votetotals)
                replaces["$SWVotes"] = int(votetotals[0])
                replaces["$STVotes"] = int(votetotals[1])
                print("2",replaces)
                if replaces["spaceshow"] == "StarWars":
                    replaces["$SWVotes"] = replaces["$SWVotes"] + 1
                elif replaces["spaceshow"] == "StarTrek":
                    replaces["$STVotes"] = replaces["$STVotes"] + 1
                print("3",replaces)
                #f = open("votes.txt", "w")
                #f.write(replaces["$SWVotes"]+" "+replaces["$STVotes"])
                #f.close()
                #print("HERE 1")
                try:
                    l.acquire()
                    with open("votes.txt", 'w') as f:
                        f.write(str(replaces["$SWVotes"])+' '+str(replaces["$STVotes"])+"\n")
                    l.release()
                except:
                    print("Error writing to file")
                #print("HERE 2")

                #print("4",replaces)
                print("Pre-Response:\n"+response)
                temp = response;
                for key in replaces.keys():
                    print(f"Replacing {key} with {replaces[key]}.", end=" ")
                    try:
                        temp = response.replace(key, str(replaces[key]))
                        print("Success!")
                    except:
                        print("Failed.")
                    response = temp
            #except:
            #    print("Error with replacements")
            #finally:
            print("Sending response:\n"+response)
            s.send(response.encode("ascii"))

            #if mediaType == "ss235":


    else:
        response = "HTTP/1.0 501 Not Implemented\n"
        response += "\n"
        response += "I'm sorry Dave, I can't do that\n"
        response += "\n"
        s.send(response.encode("ascii"))
    s.close()


def HTTPServer():
    serversocket = socket()

    host = getIPAddress()
    print("Listening on: "+host+":2009")
    serversocket.bind((host, 2009))

    serversocket.listen()

    myLock = Lock()
    while True:
        print("Waiting for connection....")
        clientsocket, addr = serversocket.accept()
        print("Connnection from", addr)

        threading.Thread(target=processRequest, args=(clientsocket, addr, myLock)).start()

    serversocket.close()

if __name__ == "__main__":
    HTTPServer()
