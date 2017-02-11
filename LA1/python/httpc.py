#!/usr/bin/python

import sys
import argparse
from httpl import GET, POST

def main(kb):
    method = kb[1]
    del kb[1]
    arguments = " ".join(kb)

    if method == "get":
        print "Using the get method"
        GET(kb[0], arguments)
    elif method == "post":
        print "Using the post method"
    else:
        print "error: http method must be specified"




if __name__ == "__main__":
   main(sys.argv)
