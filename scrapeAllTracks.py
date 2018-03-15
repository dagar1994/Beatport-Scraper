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

def printDict(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s{' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)
        print >> output, '%s}' % (nested_level * spacing)
    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)


artistList = {}
genreList = {}

page = requests.get("https://www.beatport.com/tracks/all")
#page = requests.get("https://www.beatport.com/artist/astrix/7873/releases")
soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

pageNumbers = soup.find_all("a" , {"class" : "pag-number"})
print pageNumbers
availablePages = pageNumbers[-1].text

print availablePages




for pageNumber in range(1,int(availablePages)):
	#page = requests.get("https://www.beatport.com/artist/astrix/7873/releases?page=" + str(pageNumber))
	page = requests.get("https://www.beatport.com/tracks/all?page=" + str(pageNumber))
	print "https://www.beatport.com/tracks/all?page=" + str(pageNumber)
	soup = BeautifulSoup(page.content, 'html.parser',from_encoding="ascii")

	scriptData = soup.find("script" , {"id" : "data-objects"})

	jsonDataText = find_between(scriptData.text,"Playables = ","window.")
	jsonDataText = jsonDataText.replace(";","")
	jsonData = json.loads(jsonDataText)
	for index in jsonData["tracks"]:
		title =  index['name']
		url = index['preview']['mp3']['url']
		artists = index['artists']
		genres = index['genres']
		for artist in artists:
			print artist['name'].strip()
			try:
				print artistList[artist['name'].strip()]
				print "FOUND"
			except:
				artistUrl =  "https://www.beatport.com/artist/" + str(artist['slug']) + "/" + str(artist['id'])
				print artistUrl
				artistList.update({artist['name'].strip() : artistUrl})
				print "ADDED"
		
		for genre in genres:
			print genre['name'].strip()
			try:
				print genreList[genre['name'].strip()]
				print "FOUND"
			except:
				genreUrl =  "https://www.beatport.com/genre/" + str(genre['slug']) + "/" + str(genre['id'])
				print genreUrl
				genreList.update({genre['name'].strip() : genreUrl})
				print "ADDED"
	
	
		print title
		print url
		
print artistList
print genreList
		




