from .fantasypros import FantasyPros

class PlayerFactory:
    @staticmethod
    def create_players(merged_data):
        position_player_dict = {}
        player_list = []
        for position in FantasyPros.positions:
            players_at_positions = merged_data[position]
            for player in players_at_positions:
                player_list.append(Player(player))
            position_player_dict[position] = player_list
            player_list = []
        return position_player_dict
    

class Player:
    def __init__(self, player):
        self.name = player['player_name']
        self.position = player['player_position_id']
        self.page_url = player['player_page_url']
        self.opponent_id = player.get('player_opponent_id', "")
        self.yahoo_id = player['player_yahoo_id']
        self.bye_week = player['player_bye_week']
        self.rank_average = player['rank_ave']
        self.rank_std = player['rank_std']
        self.cbs_id = player['cbs_player_id']
        self.team = player['player_team_id']
        self.team_name = player['team']['teamName']
        self.is_home = player['game']['homeTeam']['abbr'] == self.team
        self.salary = player['salary']
        self.player_owned_avg = player['player_owned_avg']
        self.projected_base_yahoo = player['projectedPoints']
        self.ppg = player['fantasyPointsPerGame']
        self.ppg_std = player['fantasyPointsStdDev']
        self.points_history = player['fantasyPointsHistory']
        self.projected_base_fpros = player['r2p_pts']
        self.grade = player['start_sit_grade']
        self.position_rank = player['pos_rank']
        