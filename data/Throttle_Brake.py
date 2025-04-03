"""Visualization Type: Overlapping line charts

Metrics: Throttle (%) and Brake (%)


Raw data (session data )
1)





1) For every session all lap data are collected
sorted driver wise
we get timestamp of each lap
lap >= data_start timestamp of lap and lap < date_start timestamp of lap + 1
arrange data in this fashion

For a given lap find all car data between the two time stamps
sort them on time stamp, we get car data for each lap




"""

from termcolor import colored

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# OpenF1 API Configuration
BASE_URL = "https://api.openf1.org/v1/laps?"
SESSION_KEY = "9689"  # Replace with actual session key

LOCATION_URL = "https://api.openf1.org/v1/car_data?"
"driver_number=1&session_key=9689&date>%3D2025-03-15T05:04:18.324000+00:00&date<2025-03-15T05:05:55.056000+00:00"



# Fetch lap data for all drivers
def fetch_lap_data(session_key):
    url = f"{BASE_URL}session_key={session_key}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

def fetch_location_url(driver_number,session_key,start_timestamp,end_timestamp):
    final_url = LOCATION_URL+"driver_number="+str(driver_number)+"&session_key="+str(session_key)+"&date>"+str(start_timestamp) + "&date<" + str(end_timestamp)
    response = requests.get(final_url)
    return response.json() if response.status_code == 200 else []

def fetch_location_url2(driver_number,session_key,start_timestamp):
    final_url = LOCATION_URL+"driver_number="+str(driver_number)+"&session_key="+str(session_key)+"&date>"+str(start_timestamp)
    response = requests.get(final_url)
    return response.json() if response.status_code == 200 else []


# Retrieve data
data = fetch_lap_data(SESSION_KEY)

if not data:
    print("No data retrieved. Check session key.")
    exit()

# Convert to DataFrame
df = pd.DataFrame(data)
drivers = df["driver_number"].unique().tolist()
for driver in drivers:
    print("Driver number "+str(driver))
    driver_laps = df[df["driver_number"] == driver].copy()  # Ensure you are not modifying the original DataFrame
    sorted_laps = driver_laps.sort_values(["lap_number", "date_start"],ascending=[True, True])  # Returns a sorted DataFrame
    laps = sorted_laps[["lap_number","date_start"]].values.tolist()

    dn = requests.get(f'https://api.openf1.org/v1/drivers?driver_number={driver}&session_key={SESSION_KEY}')
    driver_name = dn.json()[0]["full_name"]

    for i in range(len(laps)-1):

        lap_stats = fetch_location_url(driver,SESSION_KEY,laps[i][1],laps[i+1][1])
        if lap_stats == []:
            continue
        lap_stats = pd.DataFrame(lap_stats)
        lap_stats.sort_values(by="date")
        x = [i for i in range(1,lap_stats.shape[0])]
        throttle = lap_stats["throttle"].values.tolist()
        brake = lap_stats["brake"].values.tolist()
        min_length = min(len(throttle), len(brake),len(x))
        x = x[:min_length]
        throttle = throttle[:min_length]
        brake = brake[:min_length]
        plt.plot(x, throttle, color='green',alpha=0.5 ,linestyle='-', label="Throttle")

        # Plot the second line (Blue)
        plt.plot(x, brake, color='red', alpha=0.5,linestyle='-', label="Brake")

        # Labels and Title
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Brake and Throttle over lap " + str(laps[i][0]) + " for " + driver_name)

        # Show legend
        plt.legend()

        # Show graph
        plt.show()




