from flask import Flask, render_template, request
import urllib.request
import urllib.parse
import re
from pyfladesk import init_gui
import os, sys
base_dir = '.'
if hasattr(sys, '_MEIPASS'):
    base_dir = os.path.join(sys._MEIPASS)

app = Flask(__name__,
        static_folder=os.path.join(base_dir, 'static'),
        template_folder=os.path.join(base_dir, 'templates'))

def get_url(query):
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    print("https://www.youtube.com/embed/" + search_results[0])
    url = "https://www.youtube.com/embed/" + search_results[0]
    return url

@app.route('/')
def index():
    return render_template('index.html', url="exit")

@app.route('/get_video', methods=['POST'])
def video():
    query = request.form.get("song")
    url = get_url(query)
    return render_template('index.html', url=url)


if __name__ == '__main__':
    # app.run(debug=True)
    init_gui(app)