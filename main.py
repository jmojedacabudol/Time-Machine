import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
import pprint

CLIENT_ID_SPOTIFY = "90c7b48ea27942328be69d429776a762"
CLIENT_SECRET_SPOTIFY = "12a75adc97d84e63b4f923a7e1e674f9"
URL_REDIRECT = "http://example.com"
USERNAME = "Hadadi Mithrandir"
song_uris = []
pp = pprint.PrettyPrinter(indent=4)

spotipy = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID_SPOTIFY,
                              client_secret=CLIENT_SECRET_SPOTIFY,
                              redirect_uri=URL_REDIRECT,
                              cache_path="token.txt",
                              show_dialog=True,
                              username=USERNAME,
                              scope="playlist-modify-private"))
user_id = spotipy.current_user()['id']
# print(user_id)

song_name = "Incomplete",
year = 2000

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
