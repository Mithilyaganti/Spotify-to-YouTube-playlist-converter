from requests import post
from requests import get

import json
import base64
import os

from googleapiclient.discovery import build
from dotenv import load_dotenv


load_dotenv()
client_id=os.getenv("client_id")
client_secret=os.getenv("client_secret")
def get_token():
    auth_string=client_id+":"+client_secret
    auth_byte=auth_string.encode('utf-8')
    auth_base64=str(base64.b64encode(auth_byte),"utf-8")

    url="https://accounts.spotify.com/api/token"
    headers= {
        "Authorization":"Basic "+auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data={"grant_type":"client_credentials"}
    result=post(url,headers=headers,data=data)
    json_result=json.loads(result.content)
    token=json_result['access_token']

    return token

def get_header(token):
    return {"Authorization": "Bearer "+token}


def get_tracks(playlist_url,token):
    playlist_id=playlist_url.split('/')[-1]
    url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers=get_header(token)
    result=get(url,headers=headers)
    json_result=result.json()
    if len(json_result)==0:
        print("no playlist exists with that url")
        return None
    names=[x['track']['name'] for x in json_result['tracks']['items']]
    return names

token=get_token()
playlist_url=input("Enter the url of the playlist: ")
song_names=get_tracks(playlist_url,token)
print(song_names)

youtube_apiKey=os.getenv("youtube_api")
youtube=build('youtube','v3',developerKey=youtube_apiKey)
def video_id(query):
    req=youtube.search().list(
        part='snippet',
        maxResults=1,
        order="relevance",
        q=query,
        type='video'
    )
    output=req.execute()
    return output['items'][0]['id']['videoId']


def video_link(vid_id):
    return f"https://www.youtube.com/watch?v={vid_id}"


song_links=[]
for i in song_names:
    vid_id=video_id(i)
    song_links.append(video_link(vid_id))

print(song_links)