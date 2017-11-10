import urllib.request as url
import json
from tkinter import *
from PIL import Image, ImageTk
import requests
import nltk

data = None
resultIndex = 0
apiKey = "56Sj26QLjNDGnuwixUk16H4EVfzjpT4s"

class GIFPlayer(Label):
    def __init__(self, master, filename):
        im = Image.open(filename)
        seq =  []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, master, image=self.frames[0])

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.paused = False
        self.idx = 0

        self.cancel = self.after(self.delay, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        if (not self.paused):
            self.cancel = self.after(self.delay, self.play)

    def pause(self):
        self.paused = True 

    def newImage(self, master, filename):
        self.pause()
        self.idx = 0
        im = Image.open(filename)
        seq =  []
        try:
            while 1:
                seq.append(im.copy())
                im.seek(len(seq)) # skip to next frame
        except EOFError:
            pass # we're done

        try:
            self.delay = im.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame)) 

        self.paused = False
        self.cancel = self.after(self.delay, self.play)
        
def search(rawSearch, filename, root):
    gifURL = ""
    tokens = nltk.word_tokenize(rawSearch)
    search = tokens[-1]
    request = "http://api.giphy.com/v1/gifs/search?q=" + search + "&api_key=" + apiKey + "&limit=5"
    print (request)
    rawData = url.urlopen(request).read()
    dat = json.loads(rawData.decode("utf-8"))
    try:
        gifURL = dat["data"][resultIndex]["images"]["original"]["url"]
    except Exception:
        rawSearch = input("No search results found! Try another search:")   

    gif = requests.get(gifURL, allow_redirects=True)
    open(filename, 'wb').write(gif.content)    
    return GIFPlayer(root, filename)

def main() :
    global data
    rawSearch = ""
    gifURL = ""
    done = False

    while (not done):
        rawSearch = input("Please enter a search phrase (put spaces between words): ")
        search = rawSearch.replace(' ', '+')
        rawData = url.urlopen("http://api.giphy.com/v1/gifs/search?q=" + search + "&api_key=" + apiKey + "&limit=5").read()
        data = json.loads(rawData.decode("utf-8"))
        try:
            gifURL = data["data"][resultIndex]["images"]["original"]["url"]
            done = True
        except Exception:
            rawSearch = input("No search results found! Try another search:")   

    gif = requests.get(gifURL, allow_redirects=True)
    open('result.gif', 'wb').write(gif.content)


def nextResult() : 
    global resultIndex
    global data
    resultIndex = (resultIndex + 1) % 5
    gifURL = data["data"][resultIndex]["images"]["original"]["url"]
    gif = requests.get(gifURL, allow_redirects=True)
    open('result.gif', 'wb').write(gif.content)

# main()
# root = Tk()
# anim = GIFPlayer(root, 'result.gif')
# anim.pack()

# def stop_it():
#     anim.after(100, anim.pause)

# def play_it():
#     anim.paused = False
#     anim.after(100, anim.play)

# def next():
#     nextResult()
#     anim.newImage(root, 'result.gif')

# Button(root, text='pause', command=stop_it).pack()
# Button(root, text='play', command=play_it).pack()
# Button(root, text='next result', command=next).pack()

# s = StringVar()
# s.set("New GIF search here")
# searchBox = Entry(root, textvariable=s)
# searchBox.pack()

# def newSearch():
#     global data 
#     global resultIndex
#     resultIndex = -1
#     done = False
#     while (not done):
#         rawSearch = searchBox.get()
#         search = rawSearch.replace(' ', '+')
#         rawData = url.urlopen("http://api.giphy.com/v1/gifs/search?q=" + search + "&api_key=" + apiKey + "&limit=5").read()
#         data = json.loads(rawData.decode("utf-8"))
#         try:
#             gifURL = data["data"][resultIndex]["images"]["original"]["url"]
#             done = True
#         except Exception:
#             rawSearch = searchBox.get()

#     gif = requests.get(gifURL, allow_redirects=True)
#     open('result.gif', 'wb').write(gif.content)

#     anim.newImage(root, 'result.gif')
#     anim.after(100, anim.play)

# Button(root, text='search', command=newSearch).pack()

# root.mainloop()