import urllib.request as url
import json
from tkinter import *
from PIL import Image, ImageTk
import requests
import nltk
import test

data = None
resultIndex = 0
apiKey = "56Sj26QLjNDGnuwixUk16H4EVfzjpT4s"

class GIFPlayer(Label):
    def __init__(self, master, filename, url, i):
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

        Label.__init__(self, master, image=self.frames[0], cursor='heart')

        temp = seq[0]
        for image in seq[1:]:
            temp.paste(image)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.paused = False
        self.idx = 0
        self.url = url
        self.result_index = i
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
        
def search(rawSearch, filename, root, fdist):
    gifURL = ""
    message = rawSearch.split("]")[1]
    search = ""
    keywords = test.keywords(message, fdist)
    print('\nSearching for GIF with tags: ')
    print(keywords)
    for i, word in enumerate(keywords):
        if (i + 1 < len(keywords)):
            search += word + "+"
        else:
            search += word
    request = "http://api.giphy.com/v1/gifs/search?q=" + search + "&api_key=" + apiKey +"&limit=5"
    #print (request)
    rawData = url.urlopen(request).read()
    dat = json.loads(rawData.decode("utf-8"))
    gifs = []
    for i in [0,1,2]:
        try:
            #print(json.dumps(dat, sort_keys=True, indent=4, separators=(',',': ')))
            gifURL = dat["data"][i]["images"]["fixed_width"]["url"]
        except Exception as e:
            print(type(e))
            print(e)
            print(dat["meta"])

        gif = requests.get(gifURL, allow_redirects=True)
        open(str(i) + filename, 'wb').write(gif.content)    
        gifs.append(GIFPlayer(root, str(i) + filename, request, i))
    return gifs

def create_GIF_label(request, filename, root, i):
    rawData = url.urlopen(request).read()
    dat = json.loads(rawData.decode("utf-8"))
    gifURL = dat["data"][int(i)]["images"]["fixed_width"]["url"]
    gif = requests.get(gifURL, allow_redirects=True)
    open(filename, 'wb').write(gif.content)     
    return GIFPlayer(root, filename, request, i)    

# def main() :
#     global data
#     rawSearch = ""
#     gifURL = ""
#     done = False

#     while (not done):
#         rawSearch = input("Please enter a search phrase (put spaces between words): ")
#         search = rawSearch.replace(' ', '+')
#         rawData = url.urlopen("http://api.giphy.com/v1/gifs/translate?s=" + search + "&api_key=" + apiKey).read()
#         data = json.loads(rawData.decode("utf-8"))
#         try:
#             gifURL = data["data"]["images"]["fixed_height"]["url"]
#             done = True
#         except Exception:
#             print(data["meta"]) 

#     gif = requests.get(gifURL, allow_redirects=True)
#     open('result.gif', 'wb').write(gif.content)


# def nextResult() : 
#     global resultIndex
#     global data
#     resultIndex = (resultIndex + 1) % 5
#     gifURL = data["data"][resultIndex]["images"]["fixed_height"]["url"]
#     gif = requests.get(gifURL, allow_redirects=True)
#     open('result.gif', 'wb').write(gif.content)

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