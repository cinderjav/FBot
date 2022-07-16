import json
import pathlib

class Config:
    _config = None
    
    @classmethod
    def get_config(cls):
        if cls._config is not None:
            print("config Cached")
            return cls._config      
        filepath = pathlib.Path(__file__).resolve().parent.parent  
        try:
            f = open(f"{filepath}/config/requestinfo.json", 'r')
            return json.loads(f.read())
        except Exception as e:
            print(f'Exception Thrown! {e}')
            raise e
        finally:
            f.close()