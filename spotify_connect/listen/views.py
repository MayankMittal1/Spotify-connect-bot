from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
import os
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_sameorigin
import os
from os.path import join, dirname
import environ
# Initialise environment variables
environ.Env.read_env()
env = environ.Env()

def refreshToken():
  respons = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={
                "Authorization": f"Basic {env('CLIENT_ID')}"
            },
            data={
              'grant_type':f"refresh_token",
              'refresh_token':f"{env('REFRESH_TOKEN')}"
            }
        )
  return respons.json()["access_token"]

def request_addSong(url,data):
    respons = requests.post(url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {refreshToken()}"
        }
    )
    print(respons.json())
    return respons

@csrf_exempt
def addSong(request):
  if request.method=="POST":
    text=request.POST.get('text')
    texts=text.split(" ")
    for text in texts:
      if 'open.spotify.com' in text:
        song_id=(text.split('/')[-1]).split('?')[0]
        data= 'spotify:track:'+song_id
        url = f"https://api.spotify.com/v1/playlists/7ku1XAdsOMc1uKz7SAcGEx/tracks?uris={data}"
        respons = request_addSong(url,data)
        return HttpResponse('Done')
  else:
    return HttpResponse('Welcome To Spotify Api')


def accessToken(request):
    code=request.GET.get('code')
    state=request.GET.get('state')
    print(code,state)
    return HttpResponse('Welcome To Spotify Api')
  

