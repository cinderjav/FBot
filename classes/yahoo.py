import requests
import json

class Yahoo:
    _contest_id_header = "contestid"
    
    @classmethod
    def get_yahoo_data(cls, config):
        result = requests.get(f'https://dfyql-ro.sports.yahoo.com/v2/contestPlayers?lang=en-US&region=US&device=desktop&contestId={config[cls._contest_id_header]}')
        return cls._get_player_results(result)
    
    @classmethod
    def _get_player_results(cls, result):
        jData = json.loads(result.content)
        return cls._sanitize_data(jData['players']['result'])
    
    def _sanitize_data(yah_data):
        for player in yah_data:          
            yahoo_id_string = player['code']
            yahoo_id = yahoo_id_string.split(".")[-1]
            player['code'] = int(yahoo_id)
        return yah_data