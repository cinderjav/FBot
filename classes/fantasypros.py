import string
import requests
import json
from .position import Position
from concurrent import futures

class FantasyPros:
    _headers = {'x-api-key': 'zjxN52G3lP4fORpHRftGI2mTU8cTwxVNvkjByM3j'}
    _pros_week_header = "fantasyproweek"
    _pros_year_header = "fantasyproyear"
    positions = [Position.RB.name, Position.WR.name, Position.DST.name, Position.QB.name, Position.TE.name]
    
    @classmethod
    def get_fpros_data(cls, config):
        assert config != None, "Error Reading Config"
        
        response = cls._make_requests(config)
        cls._sanitize_data(response)
        return response
    
    @classmethod
    def _get_player_data(cls, response):
        data = json.loads(response.content)        
        return data['players']
    
    @classmethod
    def _get_url(cls, position : string, config):
        return f'https://api.fantasypros.com/v2/json/nfl/{config[cls._pros_year_header]}/consensus-rankings?type=weekly&scoring=HALF&position={position}&week={config[cls._pros_week_header]}'
    
    @classmethod
    def _make_requests(cls, config):
        result_dict = {}
        with futures.ProcessPoolExecutor() as executor:
            qb_process = executor.submit(cls._get_fpros_position_data, Position.QB.name, config)
            rb_process = executor.submit(cls._get_fpros_position_data, Position.RB.name, config)
            wr_process = executor.submit(cls._get_fpros_position_data, Position.WR.name, config)
            te_process = executor.submit(cls._get_fpros_position_data, Position.TE.name, config)
            dst_process = executor.submit(cls._get_fpros_position_data, Position.DST.name, config)
            
            result_dict[Position.QB.name] = qb_process.result()
            result_dict[Position.RB.name] = rb_process.result()
            result_dict[Position.WR.name] = wr_process.result()
            result_dict[Position.TE.name] = te_process.result()
            result_dict[Position.DST.name] = dst_process.result()
            
            assert len(result_dict.keys()) == len(cls.positions), "Need to fix position data"
            
        return result_dict
    
    @classmethod
    def _get_fpros_position_data(cls, pos, config):
        request_url = cls._get_url(pos, config)
        response = requests.get(request_url, headers = cls._headers)
        return cls._get_player_data(response)
    
    @classmethod
    def _sanitize_data(cls, data_dict):
        filtered = set()
        def _allow_player_filter(player):
            result = player['player_yahoo_id'] != '' and player['player_yahoo_id'] != None and player['player_yahoo_id'] != "1000"
            if not result:
                filtered.add(player["player_name"])
            return result
        
        def _clean(player):
            pts = player.get('r2p_pts', 0)
            player['r2p_pts'] = int(pts)
            player['player_yahoo_id'] = int(player['player_yahoo_id'].replace("1000", ""))
            rank_ave = player.get('rank_ave', 0)
            rank_std = player.get('rank_std', 0)
            player['rank_ave'] = float(rank_ave)
            player[rank_std] = float(rank_std)
                    
        for positions in data_dict:
            players = data_dict[positions]
            new_filtered_players = []
            for player in players:                     
                if _allow_player_filter(player):
                    new_filtered_players.append(player)
                    _clean(player)
            data_dict[positions] = new_filtered_players
        print("Filtered Players", filtered)