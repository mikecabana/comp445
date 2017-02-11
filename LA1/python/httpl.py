import httplib
import urllib
import urlparse
import ast
import json


def GET(url, str):
    #process the url
    url = urlparse.urlparse(url)
    HOST = url.netloc
    PATH = url.path
    if PATH == "":
        PATH = "/"
    QUERY = url.query

    #process the string
    str = str.split(" ")

    HEADER = ""
    start = 0
    for x in str:
        start += 1
        if (x == "-h"):
            HEADER += str[start]+ " "
            

    con = httplib.HTTPConnection(HOST,80)
    con.request("GET", PATH, HEADER)
    res = con.getresponse()

    print "GET", PATH, "HTTP /",(res.version / 10.)
    print "Host: ", HOST, "\n"

    if ("-v" in str):
        print res.msg
    else:
        print res.getheaders()

    print res.read()

    res.close()


#GET("http://httpbin.org/status/418?var=2", "GET -v -h Content-Type:application -h Accept:text/plain")

def POST(url, str):
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
    str = str.split(" ")

    HEADER = {}
    start = 0
    for x in str:
        start += 1
        if (x == "-h"):
            temp = str[start].split(":")
            HEADER[temp[0]] = temp[1]
    
    body = {} 
    if ("-d" in str):
        body = ast.literal_eval(str[str.index("-d")+1])

    BODY = urllib.urlencode(body)
    
    con = httplib.HTTPConnection(HOST, 80)
    con.request("POST", PATH + QUERRY, BODY, HEADER)
    res = con.getresponse()

    print "POST", PATH, "HTTP /", (res.version / 10.)
    print "Host: ", HOST

    if ("-v" in str):
        print res.msg
    else:
        print res.getheaders()
    
    print res.read()


    #print QUERRY

    res.close()

#POST("http://httpbin.org/post?var=1","POST -h Content-Type:application/json -h Accept:text/plain -d {'spam':5,'eggs':2,'bacon':0}")




