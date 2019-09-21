"""
tkinter_ydl
-----------------

A simple youtube downloader and converter built with python tkinter
"""

import datetime
import gettext
import sys
import time
import os
import tkinter
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter import *
import youtube_dl
from tkinter import filedialog

# All translations provided for illustrative purposes only.
# english
_ = lambda s: s


class MainFrame(ttk.Frame):
    "Main area of user interface content."

    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        paddings = {'padx': 6, 'pady': 6}
        self.download_location = '/'.join(os.getcwd().split('/')[:3]) + '/Downloads'
        ttk.Label(parent, text="Youtube Url").pack(side='top', anchor='w', **paddings)
        self.entry = ttk.Entry(parent, )
        self.entry.pack(side='top', fill='x', **paddings)

        # todo delete this line
        self.entry.insert(0, 'https://www.youtube.com/watch?v=nXait2wHOQc')

        self.button = ttk.Button(parent, text="Download", command=self.do_download)
        self.button.pack(side='top', **paddings, anchor='w')

        # style = ttk.Style()
        # style.configure('TButton', foreground="red")
        # self.button.config(style='Alarm.TButton')

        self.location_button = ttk.Button(parent, text="Location", command=self.browse_button)
        self.location_button.pack(side='top', **paddings, anchor='w')

        self.statusStringVar = StringVar()
        self.statusStringVar.set('status here')
        self.status = ttk.Label(parent, textvariable=self.statusStringVar, text='status', )
        self.status.pack(side='top', anchor='w', fill='x', **paddings)

        self.locStringVar = StringVar()
        self.locStringVar.set(f"Location: {self.download_location}")
        self.locationLabel = ttk.Label(parent, textvariable=self.locStringVar, )
        self.locationLabel.pack(side='top', anchor='w', fill='x', **paddings)

        self.progressIntVar = IntVar()
        self.progressIntVar.set(0)
        self.mpb = ttk.Progressbar(parent, orient="horizontal", length=200, mode="determinate")
        self.mpb['variable'] = self.progressIntVar
        self.mpb.pack(side='top', anchor='w', fill='x', **paddings)
        self.mpb["maximum"] = 100
        # self.mpb["value"] = 0

    def do_download(self):
        print('started')
        # download_location = '~/'

        ydl_opts = {
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'noplaylists': True,
            'progress_hooks': [self.progress_hook],
            'quiet': True,
            'outtmpl': self.download_location + '/%(title)s.%(ext)s',
        }

        # todo: do validations on this
        target = self.entry.get()

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # ydl.add_progress_hook()
            ydl.download([target, ])

    def progress_hook(self, d):
        if d['status'] == 'finished':
            file_tuple = os.path.split(os.path.abspath(d['filename']))
            print("Done downloading {}".format(file_tuple[1]))
        if d['status'] == 'downloading':
            # print(d['filename'], d['_percent_str'], d['_eta_str'])
            # print('***', d['_percent_str'])
            # self.status.config(text=d['_percent_str'])
            self.statusStringVar.set(d['_percent_str'])
            progress_int = int(float((d['_percent_str']).split('%')[0].strip()))
            self.progressIntVar.set(progress_int)
            self.parent.update_idletasks()
            # self.mpb["value"] = int(float((d['_percent_str']).split('%')[0].strip()))

    def browse_button(self):
        filename = filedialog.askdirectory()
        print(filename)
        self.download_location = filename
        self.locStringVar.set(f"Location: {self.download_location}")


class Application(tkinter.Tk):
    "Create top-level Tkinter widget containing all other widgets."

    def __init__(self):
        tkinter.Tk.__init__(self)

        self.wm_title('Tkinter YDL')
        self.wm_geometry('640x480')

        self.mainframe = MainFrame(self)
        self.mainframe.pack(side='right', fill='y')


if __name__ == '__main__':
    APPLICATION_GUI = Application()
    APPLICATION_GUI.mainloop()
