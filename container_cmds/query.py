#!/usr/bin/python  
import sys  
import os


os.system('peer chaincode query -C $CHANNEL_NAME -n mycc -c \'{"Args":["query","%s"]}\'' %sys.argv[1])
