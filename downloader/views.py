from django.shortcuts import render,redirect
from django.conf import settings
import requests
from isodate import parse_duration
from pytube import YouTube
from pytube import Playlist
import os


def home(request):

    videos =[]
    flag = 0
    

    if request.method =='POST':
        try:
            search_url ='https://www.googleapis.com/youtube/v3/search'
            video_url = 'https://www.googleapis.com/youtube/v3/videos'

            searchParameter = {
                'part' : 'snippet',
                'q' :request.POST['searchField'],
                'key' : settings.YOUTUBE_API_KEY,
                'maxResults' : 6,
                'type' : 'video'
            }
            idList = []
            req = requests.get(search_url, params =searchParameter)

            items = req.json()['items']

            for item in items:
                idList.append(item['id']['videoId'])

            #Search end , now times to videos

            videoParameter = {
                'part' : 'snippet, contentDetails',
                'key' : settings.YOUTUBE_API_KEY,
                'id' :','.join(idList),
                'maxResults':6
            }

            req = requests.get(video_url, params = videoParameter)

            items = req.json()['items'] # ['contentDetails']
            

            for item in items:

                title = item['snippet']['title']

                if len(title) > 65:
                    title = title[:65] + '....'
                
                urll = f'https://www.youtube.com/watch?v={item["id"]}'
                try:
                    obj = YouTube(urll)
                    allItem = obj.streams.filter(file_extension='mp4').all()
                except:
                    pass 

                itag = []
                vformat = []
                for Item in allItem:
                    try:
                        if Item.resolution and int(Item.resolution[:-1]) not in vformat:
                            itag.append(Item.itag)
                            vformat.append(int(Item.resolution[:-1]))
                    except:
                        pass


                vformat.sort(reverse=True) 

                mylist = zip(itag, vformat)
                video = {
                    'title' : title,
                    'id' : item['id'],
                    'url': f'https://www.youtube.com/watch?v={item["id"]}',
                    'duration' : int(parse_duration(item['contentDetails']['duration']).total_seconds() // 60),
                    'thumbnail' : item['snippet']['thumbnails']['high']['url'],
                    'mylist': mylist

                }
                videos.append(video)
        except:
             flag = 1
    
    context = {'videos':videos,'flag':flag}

    return render(request,'downloader/home.html',context)


def download(request,id):

    if request.method == 'POST':

        choice = request.POST['choice']
        urll  = f'https://www.youtube.com/watch?v={id}'
        obj = YouTube(urll).streams.get_by_itag(choice).download('../../../../')
        
    return redirect('home')

def playlist(request):

    return render(request, 'downloader/playlist.html', context={})

def playlistDownload(request):
    if request.method =='POST':
        url = request.POST['searchField']
        playlistr = Playlist(url)
        for video in playlistr:
        	video.streams.get_highest_resolution().download('')
    return redirect('playlistt')
    

    
