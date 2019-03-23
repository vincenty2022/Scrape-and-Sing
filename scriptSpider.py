import scrapy
from scrapy.crawler import CrawlerProcess
import sys
import atexit
import json
import pyttsx3
import os

# initializes spider
class lyrics_Spider(scrapy.Spider):
    name = 'lyrics'

    def __init__(self, start_url):
        self.start_urls = [start_url]

    # parse function set up to work only with lyrics.com sites
    def parse(self, response):
        for i in range(len(response.xpath("//pre/text()"))):
            if not i == len(response.xpath("//pre/text()")) -1 :
                yield {
                    'lyric': response.xpath("//pre/text()")[i].get() + response.xpath("//pre/a/text()")[i].get()
                }
            else:
                yield {
                    'lyric': response.xpath("//pre/text()")[i].get()
                }

# formats start of json file
def fileinit(): 
    try: 
        file = open(jsonDir, 'r')
        file.close()
        file = open(jsonDir, 'w')
        file.truncate(0)
    except FileNotFoundError:
        file = open(jsonDir, 'w')
        
    file.write('{ \n "song":')
    file.close()

# formats end of json file
def fileend(): 
    file = open(jsonDir, 'a')
    file.write("\n}")
    file.close()

# sets json file type as output and starts spider
def spiderStart(arg):
    process = CrawlerProcess({
        'USER_AGENT' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT' : 'json',
        'FEED_URI' : 'lyrics.json'
    })

    process.crawl(lyrics_Spider, arg)
    process.start()

# returns json file dir based on script path
def jsonDir():
    scriptPath = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(scriptPath, "lyrics.json")
    return dir


if __name__ == "__main__" :  
    jsonDir = jsonDir()

    # scrapes and write quotes.json
    fileinit()
    spiderStart(sys.argv[1])
    fileend()

    # initialize voice engine
    engine = pyttsx3.init()
    engine.setProperty('voice',  r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

    with open(jsonDir) as f:
        data = json.load(f)

    # talk and stuff
    for line in data["song"]:
        engine.say(line["lyric"])
        engine.runAndWait()
