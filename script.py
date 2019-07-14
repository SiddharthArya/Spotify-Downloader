# shows a user's playlists (need to be authenticated via oauth)

import sys
import spotipy
import spotipy.util as util
import urllib
import urllib2
from bs4 import BeautifulSoup
import re
import youtube_dl

scope = 'user-library-read'

def download( str ):
	textToSearch = str
	query = urllib.quote(textToSearch)
	url = "https://www.youtube.com/results?search_query=" + query
	response = urllib2.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)
	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		link = 'https://www.youtube.com' + vid['href']
		break

	ydl_opts = {
    	'format': 'bestaudio/best',
    	'postprocessors': [{
        	'key': 'FFmpegExtractAudio',
        	'preferredcodec': 'mp3',
        	'preferredquality': '192',
    	}],
	}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([link])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
        # print(username)
    else:
        print ("Whoops, need your username!")
        sys.exit()

    token = util.prompt_for_user_token(username,scope,'c9bcc06139074886b1a143f24b30e7fb','1b3bcd8203404419ad8f96925f399d13','http://localhost:8888/callback')

    if token:
    	sp = spotipy.Spotify(auth=token)
    	flag=1
    	b=0
    	i=0
    	while (1):
    		results = sp.current_user_saved_tracks(limit=50,offset=b)
    		for item in results['items']:
        		track = item['track']
        		i+=1
        		a = repr(track['artists'][0]['name'])
        		print " %d %32.32s | %s" %(i,track['name'],a[2:len(a)-1])
        		dwn_name = a[2:len(a)-1]+" - "+track['name']
        		# download(dwn_name)    			
        	b = int(b)
        	b+=50
        	b = str(b)
        	if(i%50!=0):
        		break
        print "Enter indices that you want to download"
        start = input("Start From :")
        end = input("End Here :")
        i=0
        b=0
        while (1):
    		results = sp.current_user_saved_tracks(limit=50,offset=b)
    		for item in results['items']:
        		track = item['track']
        		if(track == ""):
        			break
        		i+=1
        		a = repr(track['artists'][0]['name'])
        		dwn_name = a[2:len(a)-1]+" - "+track['name']
        		if ((i<=end)and(i>=start)):
        			print "Downloading " + dwn_name
        			download(dwn_name)    			
        	b = int(b)
        	b+=50
        	b = str(b)	
    else:
        print "Can't get token for", username