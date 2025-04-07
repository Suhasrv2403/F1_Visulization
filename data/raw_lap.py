from pymongo import MongoClient
import requests
import pandas as pd
client = MongoClient("mongodb://admin:adminpassword@localhost:27017/")
db = client["F1_raw"]





BASE_LAP_URL = "https://api.openf1.org/v1/laps?"
SESSION_KEY = "9689"  # Replace with actual session key

# Fetch lap data for all drivers
def fetch_lap_data(session_key):
    url = f"{BASE_LAP_URL}session_key={session_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("No data retrieved. Check session key.")
        exit()



def lap_data(session_key):

    session_data = fetch_lap_data(session_key)
    collection = db['laps']
    df = pd.DataFrame(session_data)
    df.sort_values(by=['driver_number','lap_number'], ascending=True, inplace=True)
    values = df.to_dict(orient='records')
    collection.insert_many(values)
    db['session'].update_one({"session_key": session_key}, {"$set": {"laps": True}})













