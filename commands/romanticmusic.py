import sys
import spotipy
import spotipy.util as util
import logging

class RomanticMusic:
    AUTH_TOKEN = 'ADD_YOUR_TOKEN_HERE'
    SONG_ID = 'spotify:track:39l1UORIhuHvUWfxG53tRZ' # Marvin Gaye - Get It On

    def __init__(self, logger):
        self.logger = logger
        self.spotify_client = spotipy.Spotify(auth=RomanticMusic.AUTH_TOKEN)

    def respond_to(self, command_text):
        if command_text not in ('romantic music', 'romantic mood'):
            return

        devices = self.spotify_client.devices()
        devices = devices['devices']
        for device in devices:
            if device['name'] != u"My Device Name": # Replace device name here
                self.logger.info('Skipping Spotify device ' + device['name'])
                continue

            self.spotify_client.volume(30, device_id=device['id'])
            self.spotify_client.start_playback(device_id=device['id'], uris=[RomanticMusic.SONG_ID])

            track_info = self.spotify_client.track(RomanticMusic.SONG_ID)

            self.logger.info('Playing ' + track_info['name'] + ' by ' + track_info['artists'][0]['name'] + ' on ' + device['name'])


# Initial setup
if __name__ == "__main__":
    """
    Don't forget:

    export SPOTIPY_CLIENT_ID='your-spotify-client-id'
    export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
    export SPOTIPY_REDIRECT_URI='https://localhost/'

    """

    scope = 'user-read-playback-state,user-read-currently-playing,user-modify-playback-state,app-remote-control,streaming'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print "Usage: %s username" % (sys.argv[0],)
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        print "Token: " + token
    else:
        print "Can't get token for", username
