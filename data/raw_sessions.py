from pymongo import MongoClient
import requests
import raw_lap
def fetch_lap_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("No data retrieved. Check session key.")


client = MongoClient("mongodb://admin:adminpassword@localhost:27017/")
session_url = "https://api.openf1.org/v1/sessions?year=2025"

db = client["F1_raw"]
collection = db["session"]


"""sessions_tld = fetch_lap_data(session_url)
for session in sessions_tld:
    session['laps'] = False
    session['car_data'] = False
"""


pipeline = [
    {
        "$group": {
            "_id": None,
            "maxValue": { "$max": "$date_end" }
        }
    }
]

result = list(collection.aggregate(pipeline))

if result:
    max_date = result[0]['maxValue']

    new_sessions = fetch_lap_data(session_url + "date_start>" + str(max_date))
    if new_sessions:
        collection.insert_many(new_sessions)


unprocessed_sessions = collection.find({"laps": False})
for session in unprocessed_sessions:
    raw_lap.lap_data(session['session_key'])




























