from fastapi import FastAPI
from classes.fantasypros import FantasyPros
import time
from classes.config import Config
from classes.yahoo import Yahoo
from classes.datamerge import DataMerge
from classes.playerfactory import PlayerFactory

    
    
app = FastAPI()
@app.get("/")
def get_data():
    start = time.perf_counter()
    config = Config.get_config()
    fpros_data = FantasyPros.get_fpros_data(config)
    yahoo_data = Yahoo.get_yahoo_data(config)
    merged_data_result = DataMerge.merge_data(fpros_data, yahoo_data)
    players_dict = PlayerFactory.create_players(merged_data_result)
    end = time.perf_counter()
    print(f'Finished in {round(end-start, 2)} second(s)')
    return players_dict