#from pyechonest import * 
#config.ECHO_NEST_API_KEY="QUJH6KNWA7UGZHYDU"
import urllib2
import json
import numpy
import time

api_key="YOUR_API_KEY"

def getBPM(song):
	try:
		return json.load(urllib2.urlopen("http://developer.echonest.com/api/v4/song/profile?api_key="+api_key+"&id="+song+"&bucket=audio_summary"))['response']['songs'][0]['audio_summary']['tempo']
	except:
		time.sleep(3)
		getBPM(song)	
def getSongs(artist):
	try:
		return json.load(urllib2.urlopen("http://developer.echonest.com/api/v4/artist/songs?api_key="+api_key+"&id="+artist+"&format=json&results=100"))['response']['songs']
	except:
		time.sleep(3)
		getSongs(artist)

def getArtists(genre):
	try:
		return json.load(urllib2.urlopen("http://developer.echonest.com/api/v4/genre/artists?api_key="+api_key+"&format=json&name=" + genre))['response']['artists']
	except:
		time.sleep(3)
		getArtists(genre)


genres=["hip+hop", "jazz", "r%26b", "reggae", "disco"]

f = open('RESULTS.dump', 'w')

for genre in genres:
	list_O_BPMs = []
	f.write("---------------\n")
	f.write(genre + '\n')
	f.write("---------------\n")

	print("---------------")
	print(genre)
	print("---------------")

	for artist in getArtists(genre):
		print('\t' + artist['name'])
		artist_BPMs = []
		f.write('\t' + str(artist['name'].encode('utf8')) + " : \n")
		songs = getSongs(artist['id'])
		if(songs is None):
			continue
		for song in songs: 
			BPM = getBPM(song['id'])
			if(BPM is not None):
				list_O_BPMs.append(BPM)
				artist_BPMs.append(BPM)
				f.write("\t\t" + str(song['title'].encode('utf8')) + " - " + str(getBPM(song['id'])) + " BPM \n")
				print("\t\t" + str(song['title'].encode('utf8')) + " - " + str(getBPM(song['id'])) + " BPM")
		f.write('\t' + str(artist['name'].encode('utf8')) + " mean BPM : " + str(numpy.average(artist_BPMs)) + ", std. deviation : " + str(numpy.std(numpy.array(artist_BPMs))) + ", num songs sampled : " + str(len(artist_BPMs)) + '\n')
		print('\t' + str(artist['name'].encode('utf8')) + " mean BPM : " + str(numpy.average(artist_BPMs)) + ", std. deviation : " + str(numpy.std(numpy.array(artist_BPMs))) + ", num songs sampled : " + str(len(artist_BPMs)) + '\n')

	f.write(genre + " - total number of songs : " + str(len(list_O_BPMs)) + '\n')
	f.write(genre + " - average BPM : " + str(numpy.average(list_O_BPMs)) + '\n')
	f.write(genre + " - BPM std. deviation : " + str(numpy.std(numpy.array(list_O_BPMs))) + '\n')
	
	print("FINAL AVERAGE : " + str(numpy.average(list_O_BPMs)))
f.close()
