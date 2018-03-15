import requests
from bs4 import BeautifulSoup
import json
import sys
import re
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""



page = requests.get("https://www.beatport.com/")

soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

genreList = soup.find_all("li" , {"class" : "genre-drop-list__item"})

for hrefs in genreList:
	print "https://www.beatport.com/" + hrefs.a['href'].strip()
	page = requests.get("https://www.beatport.com/" + hrefs.a['href'].strip())
	soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")
	#BELOW FOR MAIN PAGE
	#topTens = soup.find("div" , {"class" : "bucket top-ten-tracks"})


	trackList = []
	tracksData = {}
	#BELOW FOR INTERIOR PAGE
	topTens = soup.find("div" , {"class" : "bucket top-ten-tracks interior-genre-top-ten-tracks"})
	topTenTracksData = topTens.find_all("li" , { "class":"bucket-item ec-item top-ten-track"})

	for tracks in topTenTracksData:
		rank = tracks.find("div" , {"class" : "top-ten-num top-ten-track-num"})
		rank = int(rank.text)
		trackName = tracks.find("span" ,{"class" : "top-ten-track-primary-title"}).text.strip()
		trackList.append(trackName)
		
		mix = tracks.find("span" ,{"class" : "top-ten-track-remixed"}).text.strip()
		artists = tracks.find("span" ,{"class" : "top-ten-track-artists"}).text.strip()
		artists = artists.replace("\n","")
		artists = re.sub(' +', ' ',artists)
		label = tracks.find("span" ,{"class" : "top-ten-track-label"}).text.strip()
		trackData = {
		"rank" : rank,
		"trackName" : trackName,
		"mix" : mix,
		"artists" : artists,
		"label" : label,
			    }
		tracksData.update({trackName : trackData})
		
	scriptData = soup.find("script" , {"id" : "data-objects"})
	#jsonDataText = find_between(scriptData.text,"Playables = ",";")
	jsonDataText = find_between(scriptData.text,"Playables = ","window.")
	jsonDataText = jsonDataText.replace(";","")
	jsonData = json.loads(jsonDataText)
	for index in jsonData["tracks"]:
		title =  index['name']
		url = index['preview']['mp3']['url']
		if title in trackList:
			tracksData[title].update({"url" : url})
	print tracksData
