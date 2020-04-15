import vlc, pafy
import urllib.request
import urllib.parse
import re


query_string = urllib.parse.urlencode({"search_query" : input()})
html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
print("http://www.youtube.com/watch?v=" + search_results[0])

url = "http://www.youtube.com/watch?v=" + search_results[0]
video = pafy.new(url)


best = video.getbest()
media = vlc.MediaPlayer(best.url)

media.play()

from time import sleep,time
timeout = time() + 120 
sleep(5) 
while media.is_playing():
    if time() > timeout:
        media.stop()
     


