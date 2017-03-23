#!/usr/bin/python

import httplib
import urllib
import urlparse
import ast
import json


def GET(url, str, port):
    #process the url
    url = urlparse.urlparse(url)
    HOST = url.netloc
    PATH = url.path
    if PATH == "":
        PATH = "/"
    QUERY = url.query
    PORT = port

    #process the string
    str = str.split(" ")

    HEADER = ""
    start = 0
    for x in str:
        start += 1
        if (x == "-h"):
            HEADER += str[start]+ " "

    con = httplib.HTTPConnection(HOST, PORT)
    con.request("GET", PATH, HEADER)
    res = con.getresponse()

    print "GET", PATH, "HTTP /",(res.version / 10.)
    print "Host: ", HOST, "\n"
    print res.reason, res.status

    if ("-v" in str):
        print res.msg
        print res.read()
    else:
        print res.getheaders()

    #print res.read()

    res.close()


#GET("http://httpbin.org/status/418?var=2", "GET -v -h Content-Type:application -h Accept:text/plain")

def POST(url, args):
    #process the url
    url = urlparse.urlparse(url)
    HOST = url.netloc
    PATH = url.path
    if PATH == "":
        PATH = "/"
    QUERRY = url.query
    if QUERRY != "":
        QUERRY = "?"+QUERRY 

    #process the string
    args = args.split(" ")

    HEADER = {}
    start = 0
    for x in args:
        start += 1
        if (x == "-h"):
            temp = args[start].split(":")
            HEADER[temp[0]] = temp[1]
    
    body = {} 
    if ("-d" in args):
        #print args[args.index("-d")+1]
        body = ast.literal_eval(args[args.index("-d")+1])

    if ("-f" in args):
        file = open(args[args.index("-f")+1],"r")
        body = ast.literal_eval(file.read())

    BODY = urllib.urlencode(body)
    
    con = httplib.HTTPConnection(HOST, 80)
    con.request("POST", PATH + QUERRY, BODY, HEADER)
    res = con.getresponse()

    print "POST", PATH, "HTTP /", (res.version / 10.)
    print "Host: ", HOST, "\n"
    print res.reason, res.status

    if ("-v" in args):
        print res.msg
        print res.read()
    else:
        print res.getheaders()
    
    #print res.read()


    #print QUERRY

    res.close()

#POST("http://httpbin.org/post?var=1","POST -h Content-Type:application/json -h Accept:text/plain -d {'spam':5,'eggs':2,'bacon':0}")




