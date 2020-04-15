import os
import sys
import vlc, pafy
import urllib.request
import urllib.parse
import re
import tkinter as tk
from tkinter import ttk
from tkinter.font import Font


class PyPlayer(tk.Frame):
    def __init__(self, container, container_instance, title=None):
        tk.Frame.__init__(self, container_instance)
        self.container = container
        self.container_instance = container_instance
        self.default_font = Font(family="Times New Roman", size=16)
        # create vlc instance
        self.vlc_instance, self.vlc_media_player_instance = self.create_vlc_instance()
         # set search box
        self.create_search_box()
        # vlc video frame
        self.video_panel = ttk.Frame(self.container_instance)
        self.canvas = tk.Canvas(self.video_panel, background='black')
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.video_panel.pack(fill=tk.BOTH, expand=1)
        # controls
        self.create_control_panel()

    def create_search_box(self):
        search_panel = ttk.Frame(self.container_instance)
        self.search = tk.Entry(search_panel, width=80) 
        self.button = ttk.Button(search_panel, text='Find youtube', command=self.getURL)
        self.button.pack(side=tk.LEFT)
        self.search.pack(side=tk.LEFT)
        search_panel.pack(side=tk.TOP)

    def create_control_panel(self):
        """Add control panel."""
        control_panel = ttk.Frame(self.container_instance)
        pause = ttk.Button(control_panel, text="Pause", command=self.pause)
        play = ttk.Button(control_panel, text="Play", command=self.play)
        stop = ttk.Button(control_panel, text="Stop", command=self.stop)
        pause.pack(side=tk.LEFT)
        play.pack(side=tk.LEFT)
        stop.pack(side=tk.LEFT)
        control_panel.pack(side=tk.BOTTOM)

    def create_vlc_instance(self):
        vlc_instance = vlc.Instance()
        vlc_media_player_instance = vlc_instance.media_player_new()
        self.container_instance.update()
        return vlc_instance, vlc_media_player_instance

    def getURL (self):  
        name = self.search.get()
        query_string = urllib.parse.urlencode({"search_query" : name})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        url = "http://www.youtube.com/watch?v=" + search_results[0]
        video = pafy.new(url)
        best = video.getbest()
        self.url = best.url

    def get_handle(self):
        return self.video_panel.winfo_id()

    def play(self):
        if not self.vlc_media_player_instance.get_media():
            self.Media = self.vlc_instance.media_new(self.url)
            self.vlc_media_player_instance.set_media(self.Media)
            self.vlc_media_player_instance.set_hwnd(self.get_handle())
            self.play()
        else:
            if self.vlc_media_player_instance.play() == -1:
                pass

    def close(self):
        """Close the window."""
        self.container.delete_window()

    def pause(self):
        """Pause the player."""
        self.vlc_media_player_instance.pause()

    def stop(self):
        """Stop the player."""
        self.vlc_media_player_instance.stop()
        self.url = ""

      

class BaseTkContainer:
    def __init__(self):
        self.tk_instance = tk.Tk()
        self.tk_instance.title("py player")
        self.tk_instance.protocol("WM_DELETE_WINDOW", self.delete_window)
        self.tk_instance.geometry("720x480") # default to 1080p
        self.tk_instance.configure(background='black')
        self.theme = ttk.Style()
        self.theme.theme_use("alt")

    def delete_window(self):
        tk_instance = self.tk_instance
        tk_instance.quit()
        tk_instance.destroy()
        os._exit(1)
    
    def __repr__(self):
        return "Base tk Container"


root = BaseTkContainer()
player = PyPlayer(root, root.tk_instance, title="Youtube Player")
root.tk_instance.mainloop()