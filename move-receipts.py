import argparse, logging
from logging import handlers
import os, errno
from os import listdir
from os.path import isfile, join
import datetime
import shutil

# logger init
#TODO Add README
logger = logging.getLogger('move-receipts')
logger.propagate = False
logger.setLevel(logging.DEBUG)
fh = handlers.RotatingFileHandler('move-receipts.log', maxBytes=1024000, backupCount=30)
fh.setLevel(logging.INFO)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

parser = argparse.ArgumentParser(description="")
parser.add_argument('dir', nargs='?', default=os.getcwd())
# subparsers = parser.add_subparsers()

# dirPathParser = subparsers.add_parser('fetch-IdpConnect')
# dirPathParser.add_argument('-id', required=True, help="The client id that you want retrieved from Ping")
# dirPathParser.set_defaults(func=fetchOidcPolicy)

# parse the args and call whatever function was selected
args = parser.parse_args()
# args.func(args)


#TODO: Make this an optional parameter and store dry run results
dryRun = True
myPath = args.dir
logger.info('Current directory: ' + myPath)
for f in listdir(myPath):
    currentFileHandle = f
    if isfile(currentFileHandle):
        logger.info('Examining ' + currentFileHandle)
        modifiedTime = datetime.datetime.fromtimestamp(os.path.getmtime(currentFileHandle))
        #if a folder for the year does not exist, create one
        yearDir = unicode(modifiedTime.year)
        if os.path.exists(yearDir) and os.path.isdir(monthDir):
            logger.debug('A directory for this year already exists')
        else:
            if not dryRun:
                os.makedirs(yearDir)
        #if a folder for that month in that year does not exist, create one
        monthDir = unicode(modifiedTime.strftime("%B"))
        if os.path.exists(monthDir) and os.path.isdir(monthDir):
            logger.debug('A directory for this month already exists')
        else:
            if not dryRun:
                os.makedirs(yearDir + os.path.sep + monthDir)
        #if not a dry run, move the file to the folder for the correct month and year
        finalDestination = join(myPath, yearDir, monthDir, currentFileHandle)
        print finalDestination
        if not dryRun:
            shutil.move(currentFileHandle, finalDestination)