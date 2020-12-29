from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from pprint import pprint
from random import randint
import config

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(config.client_id, config.client_secret))

playlist_id = config.playlist_id
offset = 0
tracks = []
while True:
    response = sp.playlist_items(playlist_id,
                                 offset=offset,
                                 fields='items.track.id,total',
                                 additional_types=['track'])
    if len(response['items']) == 0:
        break
    for i in response['items']:

        track = sp.track(i['track']['id'])
        name = track['name']
        artist = track['artists'][0]['name']
        tracks.append([[i['track']['id']], name, artist, 0])
    offset = offset + len(response['items'])

while True:
    track1 = randint(0, len(tracks)-1)
    track2 = randint(0, len(tracks)-1)
    while track1 == track2:
        track2 = randint(0, len(tracks) - 1)

    pprint("Choose between: ")
    pprint("Track 1: " + tracks[track1][1] + " by " + tracks[track1][2])
    pprint("Track 2: " + tracks[track2][1] + " by " + tracks[track2][2])
    track = input("Enter trackID or \"Done\" to finish ranking:")

    if track == "1":
        tracks[track1][3] = tracks[track1][3] + 1
        tracks[track2][3] = tracks[track2][3] - 1
        track_won = track1
        track_lost = track2
    elif track == "2":
        tracks[track2][3] = tracks[track2][3] + 1
        tracks[track1][3] = tracks[track1][3] - 1
        track_won = track2
        track_lost = track1
    elif track == "done":
        break
    else:
        pprint("Invalid input!")
        continue

    track_won_new = track_won - 1 if track_won > 0 else 0

    while track_won_new > 0 and tracks[track_won_new][3] < tracks[track_won][3]:
        track_won_new = track_won_new - 1 if track_won_new > 0 else 0
    tracks.insert(track_won_new, tracks.pop(track_won))

    if track_won_new < track_lost < track_won:
        track_lost = track_lost + 1

    track_lost_new = track_lost + 1 if track_lost < len(tracks) else len(tracks)

    while track_lost_new < len(tracks) and tracks[track_lost_new][3] > tracks[track_lost][3]:
        track_lost_new = track_lost_new + 1 if track_lost_new < len(tracks) else len(tracks)
    tracks.insert(track_lost_new, tracks.pop(track_lost))
pprint(tracks)