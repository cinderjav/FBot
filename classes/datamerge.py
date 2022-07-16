from .position import Position
from .fantasypros import FantasyPros

class DataMerge:
    
    @staticmethod
    def merge_data(pro, yahoo):
        new_merged_dict = {}
        player_list = []
        for position in FantasyPros.positions:
            players = pro[position]
            for player in players:
                pro_yahoo_id = player['player_yahoo_id']
                for yp in yahoo:
                    if pro_yahoo_id == yp['code']: # yahoo ids match
                        merged_player = player | yp
                        player_list.append(merged_player)
            new_merged_dict[position] = player_list
            player_list = []
                    
        return new_merged_dict