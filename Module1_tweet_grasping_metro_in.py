import argparse  #to parse the arguments in command line 
from urllib.parse import urlparse #urllib python module for opening URL , urlib.parse to break the url to components , 
import urllib
import csv
import tweepy 


# URL CLEANUP
def url_fix(s, charset='utf-8'): #UTF-8 is one of the most commonly used encodings. UTF stands for “Unicode Transformation Format”, and the '8' means that 8-bit numbers are used in the encoding.
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%') #for delimeter
    qs = urllib.quote_plus(qs, ':&=') #python data structures key-value pairs
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))


def tw_parser():
    global qw, ge, l, t, c, d


    parser = argparse.ArgumentParser(description='Twitter Search') #The argparse module makes it easy to write user-friendly command-line interfaces and issues errors when gives ivalid arguments
    parser.add_argument(action='store', dest='query', help='Search term string')
    parser.add_argument('-g', action='store', dest='loca', help='Location (mum, ndl, kol, ch, bang, srt, hbd)')
    parser.add_argument('-l', action='store', dest='l', help='Language (en = English, fr = French, etc...)')
    parser.add_argument('-t', action='store', dest='t', help='Search type: mixed, recent, or popular')
    parser.add_argument('-c', action='store', dest='c', help='Tweet count (must be <50)')
    args = parser.parse_args()

    qw = args.query     # Actual query word(s)
    ge = ''

    # Location
    loca = args.loca
    if (not(loca in ('mum', 'ndl', 'kol', 'ch', 'bang', 'srt', 'hbd')) and (loca)):
        print ("WARNING: Location must be one of these: mum,ndl,kol,ch,bang,srt,hbd")
        exit()
    if loca:
        ge = locords[loca]

    # Language
    l = args.l
    if (not l):
        l = "en"
    if (not(l in ('en'))):
        print ("WARNING: Languages currently supported are: en (English)")
        exit()

    # Tweet type
    t = args.t
    if (not t):
        t = "recent"
    if (not(t in ('mixed','recent','popular'))):
        print ("WARNING: Search type must be one of: (m)ixed, (r)ecent, or (p)opular")
        exit()

    # Tweet count
    if args.c:
        c = int(args.c)
        if (c > cmax):
            print ("Resetting count to ",cmax," (maximum allowed)")
            c = cmax
        if (not (c) or (c < 1)):
            c = 1
    if not(args.c):
        c = 1

    print ("Query: %s, Location: %s, Language: %s, Search type: %s, Count: %s" %(qw,ge,l,t,c))

# AUTHENTICATION (OAuth)
def tw_oauth(authfile):
    with open(authfile, "r") as f:
        ak = f.readlines() #to read until EOF 
    f.close()
    auth1 = tweepy.auth.OAuthHandler(ak[0].replace("\n",""), ak[1].replace("\n",""))
    auth1.set_access_token(ak[2].replace("\n",""), ak[3].replace("\n",""))
    return tweepy.API(auth1) #wrapper class of twitter API

def tw_search_json(query, cnt=5):
    authfile = './auth.k'
    api = tw_oauth(authfile)
    results = {}
    meta = {
        'username': 'text',
        'usersince': 'date',
        'followers': 'numeric',
        'friends': 'numeric',
        'authorid': 'text',
        'authorloc': 'geo',
        'geoenable': 'boolean',
        'source': 'text'
    }
    data = []
    for tweet in tweepy.Cursor(api.search, q=query, count=cnt).items():
        dTwt = {}
        dTwt['username'] = tweet.author.name
        dTwt['usersince'] = tweet.author.created_at      #author/user profile creation date
        dTwt['followers'] = tweet.author.followers_count #number of author/user followers (inlink)
        dTwt['friends']   = tweet.author.friends_count   #number of author/user friends (outlink)
        dTwt['authorid']  = tweet.author.id              #author/user ID#
        dTwt['authorloc'] = tweet.author.location        #author/user location
        dTwt['geoenable'] = tweet.author.geo_enabled     #is author/user account geo enabled?
        dTwt['source']    = tweet.source                 #platform source for tweet
        data.append(dTwt)
    results['meta'] = meta
    results['data'] = data
    return results


# TWEEPY SEARCH FUNCTION
def tw_search(api):
    counter = 0
    # Open/Create a file to append data
    csvFile = open('result_16march.csv','w')
    #Use csv Writer
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["created", "text", "retwc", "hashtag", "followers", "friends"])
	
    for tweet in tweepy.Cursor(api.search,
                                q = qw,
                                g = ge,
                                lang = l,
                                result_type = t,
                                count = c).items():

        #TWEET INFO
        created = tweet.created_at   #tweet created
        text    = tweet.text         #tweet text
        tweet_id = tweet.id          #tweet ID# (not author ID#)
        cords   = tweet.coordinates  #geographic co-ordinates
        retwc   = tweet.retweet_count #re-tweet count
        try:
            hashtag = tweet.entities[u'hashtags'][0][u'text'] #hashtags used
        except:
            hashtag = "None"
        try:
            rawurl = tweet.entities[u'urls'][0][u'url'] #URLs used
            urls = url_fix(rawurl)
        except:
            urls    = "None"
        #AUTHOR INFO
        username  = tweet.author.name            #author/user name
        usersince = tweet.author.created_at      #author/user profile creation date
        followers = tweet.author.followers_count #number of author/user followers (inlink)
        friends   = tweet.author.friends_count   #number of author/user friends (outlink)
        authorid  = tweet.author.id              #author/user ID#
        authorloc = tweet.author.location        #author/user location
        #TECHNOLOGY INFO
        geoenable = tweet.author.geo_enabled     #is author/user account geo enabled?
        source    = tweet.source                 #platform source for tweet
		# Dongho 03/28/16
        csvWriter.writerow([created, str(text).encode("utf-8"), retwc, hashtag, followers, friends])
        counter = counter +1
        if (counter == c):
            break

    csvFile.close()

# MAIN ROUTINE
def main():

    global api, cmax, locords  # Global keyword is a keyword that allows a user to modify a variable outside of the current scope. It is used to create global variables from a non-global scope i.e inside a function

    # Geo-coordinates of five metropolitan areas in india #A geographic coordinate system is a coordinate system that enables every location on Earth to be specified by a set of numbers, letters or symbols
    # Mumbai,newdelhi,kolkata,chennai,banglore,hyderabed,surat 
    locords =  {'mum': '19.0728302, 72.8826065, 20km',
                'ndl': '28.6139391, 77.2090212, 2mi',
                'kol': '22.5626297, 88.3630371, 2mi',
                'ch': '13.0878401, 80.2784729, 2mi',
                'bang': '12.972442,77.580643, 2mi',
                'hbd': '17.3840504, 78.4563599, 5km',
                'srt': '21.1702401, 72.8310607, 2mi'}
    # Maximum allowed tweet count (note: Twitter sets this to ~180 per 15 minutes)
    cmax = 50
    # OAuth key file
    authfile = './auth.k'

    tw_parser()
    api = tw_oauth(authfile)
    tw_search(api)

if __name__ == "__main__":  #“__main__” is the part of the program that runs when the script is run from the command line using a command like python File1.py.
    main()