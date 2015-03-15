from bs4 import BeautifulSoup
import mechanize
import time
import urllib
import string
import os

def getHtml (url):
    browser = mechanize.Browser()
    try:
        openedBrowser = browser.open( url )
    except mechanize.HTTPError as e:
        print "mechanize HTTP Error: ", e.code
        print "\tURL: ", url
        return None
    except mechanize.URLError as e:
        print "mechanize URL Error: ", e.args
        print "\tURL: ", url
        return None

    return openedBrowser.read()

def downloadProcess (html, base, filetype, linkList):
    soup = BeautifulSoup( html )
    for link in soup.find_all( 'a' ):
        linkText = str( link.get('href') )

        if filetype in linkText:
            # extract directory name
            slashList = [i for i, ind in enumerate(linkText) if ind == '/']
            directoryName = linkText[(slashList[0]+1) : slashList[1]]
            # create directory
            if not os.path.exists( directoryName ):
                os.makedirs( directoryName )

            linkGet = base + linkText
            filesave = linkText.lstrip('/')
            # download file
            try:
                urllib.urlretrieve( linkGet, filesave )
            except urllib.URLError as e:
                print "urllib URL Error: ", e.code
        elif "htm" in linkText: # covers both ".htm" and ".html" files
            linkList.append( link )

#start = "http://" + raw_input( "Where would you like to start searching?\n" )
start = "http://www.irrelevantcheetah.com/browserimages.html"
filetype = raw_input( "What file type are you looking for?\n" )

# create a list of slash indices
numSlash = start.count( '/' )
slashList = [i for i, ind in enumerate(start) if ind == '/']

# extract base address
if len(slashList) >= 3:
    third = slashList[2]
    base = start[:third]
else:
    base = start

linkList = []

html = getHtml( start )
if html != None:
    print "Parsing " + start
    downloadProcess( html, base, filetype, linkList )

for leftover in linkList:
    time.sleep( 0.1 )
    linkText = str( leftover.get('href') )
    html = getHtml( base + linkText )
    if html != None:
        print "Parsing " + base + linkText
        downloadProcess( html, base, filetype, linkList )

print "link list: ", linkList
