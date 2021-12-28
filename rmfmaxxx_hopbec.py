import requests
import json
import bs4 as bs
import urllib.parse
import time
from dotenv import load_dotenv
from os import getenv

load_dotenv()

PLAYLIST_ID = getenv("PLAYLIST_ID")
CLIENT_ID = getenv("CLIENT_ID")
CLIENT_SECRET = getenv("CLIENT_SECRET")
ACCESS_TOKEN = getenv("ACCESS_TOKEN")
REFRESH_TOKEN = getenv("REFRESH_TOKEN")

headers = {}


def main():
    global headers
    ACCESS_TOKEN = refreshOAuth2()
    headers = {
        'Authorization': 'Bearer '+ACCESS_TOKEN+'',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }
    ClearList()
    r = requests.get("https://www.rmfmaxxx.pl/hopbec")

    soup = bs.BeautifulSoup(r.text, 'lxml')
    title = soup.find('div', attrs={'class': 'content-page'}).find('h2')
    nr = title.find_all('b')[1].text
    full_title = title.text

    print(full_title)
    print(nr)

    UpdatePlaylist("RMFMAXXX Lista Hop Bęc (Bot Update)",
                   "RMFMAXXX Lista Hop Bęc, notowanie numer "+str(nr))

    lista = soup.find('div', attrs={
                      'class': 'list-songs'}).find_all('div', attrs={'class': 'item-song'})
    i = 0
    for item in lista:
        i = i+1
        artist = item.find('div', attrs={'class': 'is-artist'}).text
        title = item.find('a', attrs={'class': 'is-title tov'}).text
        link = "https://www.rmfmaxxx.pl" + \
            item.find('a', attrs={'class': 'is-cover'})['href']
        ytlink = getYoutubeLink(link)
        if (ytlink == ""):
            ytlink = SearchForVideo(artist+" "+title)

        print(f"HopBec: {i}.\t {artist}\t {title}\t {ytlink}")
        if(ytlink != ""):
            InsertToPlaylist(ytlink.replace(
                "https://www.youtube.com/watch?v=", ""), i-1)

    return


def getYoutubeLink(link):
    r = requests.get(link)
    soup = bs.BeautifulSoup(r.text, 'lxml')
    try:
        url = soup.find('iframe', attrs={
                        'class': 'embed-responsive-item'})['src']
        code = url.split("embed/")[1].split("?")[0]
        return "https://www.youtube.com/watch?v="+code
    except:
        return ""


def UpdatePlaylist(name, desc):
    data = {"id": PLAYLIST_ID, "snippet": {"title": name,
                                           "description": desc}, "status": {"privacyStatus": "public"}}
    data = json.dumps(data)

    r = requests.put('https://www.googleapis.com/youtube/v3/playlists?part=snippet%2Cstatus&key=' +
                     CLIENT_SECRET, headers=headers, data=data)
    if(r.status_code == 200):
        print(f"Changed playlist:\n title:\t{name}\n description:\t{desc}")
    else:
        print(r.text)
        print("UpdatePlaylist FAIL")


def InsertToPlaylist(videoId, position=0):
    data = {"snippet": {"playlistId": PLAYLIST_ID, "resourceId": {
        "kind": "youtube#video", "videoId": videoId}, "position": position}}
    data = json.dumps(data)
    r = requests.post('https://www.googleapis.com/youtube/v3/playlistItems?part=snippet%2Cstatus&key=' +
                      CLIENT_SECRET, headers=headers, data=data)
    if(r.status_code == 200):
        print(f"[+] position: {position}\t videoId: {videoId}")
    else:
        print(r.text)
        print("InsertToPlaylist FAIL", videoId, position)
    time.sleep(5)


def SearchForVideo(search):
    search = urllib.parse.quote(search)
    r = requests.get('https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q=' +
                     search+'&key='+CLIENT_SECRET, headers=headers)
    if(r.status_code == 200):
        vid = r.json()["items"][0]
        code = vid['id']['videoId']
        print(f"Searching for `{search}` and found video {code}")
        return "https://www.youtube.com/watch?v="+code
    else:
        print(r.text)
        print("SearchForVideo FAIL", search)
    return ""


def ClearList():
    print("Usuwam Playliste")
    for _ in range(3):
        lis = requests.get('https://www.googleapis.com/youtube/v3/playlistItems?part=id&maxResults=100&playlistId=' +
                           PLAYLIST_ID+'&key='+CLIENT_SECRET, headers=headers)
        if(lis.status_code != 200):
            print(lis.text)
            print("Nie udalo sie pobrac playlisty")
            raise Exception("Nie udalo sie pobrac playlisty")

        video_list = lis.json()["items"]
        for vid in video_list:
            vid_id = vid["id"]
            r = requests.delete('https://www.googleapis.com/youtube/v3/playlistItems?id=' +
                                vid_id+'&key='+CLIENT_SECRET, headers=headers)
            if(r.status_code != 204):
                print(r.text)
                print("Nie udalo sie usunac pozycji z playlisty")
                continue
            print(f"Delete {vid_id}")
        if len(video_list) == 0:
            break

    print("Zakończono czyszczenie playlisty")
    time.sleep(10)


def refreshOAuth2():
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    }

    r = requests.post('https://accounts.google.com/o/oauth2/token', data=data)
    try:
        return r.json()["access_token"]
    except Exception as e:
        print(r.text)
        raise e

if __name__ == '__main__':
    main()
