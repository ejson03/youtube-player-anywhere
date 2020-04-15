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
    
        # vlc video frame
        self.video_panel = ttk.Frame(self.container_instance)
        self.canvas = tk.Canvas(self.video_panel, background='black')
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.video_panel.pack(fill=tk.BOTH, expand=1)

         # set search box
        self.search = tk.Entry(self.container_instance, width=80) 
        self.canvas.create_window(400, 20, window=self.search)    
        self.button = tk.Button(text='Find youtube', command=self.url)
        self.canvas.create_window(100, 20, window=self.button)

        # controls
        self.create_control_panel()


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

    def url (self):  
        name = self.search.get()
        query_string = urllib.parse.urlencode({"search_query" : name})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        print(len(search_results), search_results)
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
            self.vlc_media_player_instance.set_xwindow(self.get_handle())
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
        self.url = ""
        self.vlc_media_player_instance.stop()
      

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