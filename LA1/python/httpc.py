#!/usr/bin/python

import sys
import argparse
from httpl import GET, POST

def main(kb):
    method = kb[0]
    url = kb[-1]
    del kb[0], kb[-1]
    arguments = " ".join(kb)
    #print kb
    #print arguments


    if method == "get":
        if " -d " not in arguments and " -f " not in arguments:
            print "\nUsing the get method\n"
            GET(url, arguments)
        else:
            print "\nCannot us -d or -f as an option"
    elif method == "post":
        if ((" -d" in arguments) is not (" -f" in arguments)):
            print "\nUsing the post method\n"
            POST(url, arguments)
        else:
            print "\nCannot use both -d and -f at the same time"
            #POST(url, arguments)
    else:
        print "error: http method must be specified"




if __name__ == "__main__":
   main(sys.argv[1:])
