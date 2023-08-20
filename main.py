import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import pprint
import os

song_uris = []
pp = pprint.PrettyPrinter(indent=4)

spotipy = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=os.environ['CLIENT_ID_SPOTIFY'],
                              client_secret=os.environ['CLIENT_SECRET_SPOTIFY'],
                              redirect_uri=os.environ['URL_REDIRECT'],
                              cache_path="token.txt",
                              show_dialog=True,
                              username=os.environ['USERNAME'],
                              scope="playlist-modify-private"))
user_id = spotipy.current_user()['id']
# print(user_id)

date = input("Which year do you want to time travel format YYYY-MM-DD:")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{date}/")
billboard_link = response.text

billboard_website = BeautifulSoup(billboard_link, "html.parser")

bilboard_titles = [title.getText().strip() for title in
                   billboard_website.select(selector="li .o-chart-results-list__item h3#title-of-a-story")]

# print(bilboard_titles)
year = date.split("-")[0]

for song_name in bilboard_titles:
    result = spotipy.search(q=f"track:{song_name} year:{year}", type="track")
    # pp.pprint(result)
    try:
        uri = result['tracks']['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"{song_name} doesn't exists in Spotify. Skipped.")

# pp.pprint(song_uris)

# CREATE PLAYLIST

current_playlist = spotipy.user_playlist_create(user=user_id, name=f"{date} Billboard 100",public=False, description="This is auto generate using Python created by JM POGI")
spotipy.playlist_add_items(playlist_id=current_playlist['id'],items=song_uris)
