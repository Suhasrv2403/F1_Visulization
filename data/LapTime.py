"""
3. Lap Time Comparison
Visualization Type: Bar chart

Metrics: Lap time per lap
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D


# OpenF1 API Configuration
BASE_URL = "https://api.openf1.org/v1/laps?"
SESSION_KEY = "9689"  # Replace with actual session key

LOCATION_URL = "https://api.openf1.org/v1/car_data?"
"driver_number=1&session_key=9689&date>%3D2025-03-15T05:04:18.324000+00:00&date<2025-03-15T05:05:55.056000+00:00"

def split_value(value, segments):
    base_value = value // segments
    remainder = value % segments
    return [base_value + (1 if i < remainder else 0) for i in range(segments)]


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
def convert_to_color(sector_segment):
    result = []
    for sector_color in sector_segment:

        if sector_color == 2049:
            result.append("green")
        if sector_color == 2050:
            result.append("green")
        if sector_color == 2051:
            result.append("purple")
        if sector_color == 2064:
            result.append("blue")
        else:
            if len(result) > 0:
                result.append(result[-1])
            else:
                result.append("grey")

    return result
# Retrieve data
data = fetch_lap_data(SESSION_KEY)

if not data:
    print("No data retrieved. Check session key.")
    exit()

# Convert to DataFrame
df = pd.DataFrame()
drivers = df["driver_number"].unique().tolist()
for driver in drivers:
    dn = requests.get(f'https://api.openf1.org/v1/drivers?driver_number={driver}&session_key={SESSION_KEY}')
    driver_name = dn.json()[0]["full_name"]
    print("Driver number "+str(driver))
    driver_laps = df[df["driver_number"] == driver].copy()  # Ensure you are not modifying the original DataFrame
    sorted_laps = driver_laps.sort_values(["lap_number", "date_start"],ascending=[True, True])  # Returns a sorted DataFrame
    sector_one = sorted_laps["duration_sector_1"].values.tolist()
    sector_two = sorted_laps["duration_sector_2"].values.tolist()
    sector_three = sorted_laps["duration_sector_2"].values.tolist()
    sector_one_segment = sorted_laps["segments_sector_1"].values.tolist()
    sector_two_segment = sorted_laps["segments_sector_2"].values.tolist()
    sector_three_segment = sorted_laps["segments_sector_2"].values.tolist()
    lap_number = sorted_laps["lap_number"].values.tolist()
    lap_time = sorted_laps["lap_duration"].values.tolist()
    minimum_all = min(len(sector_one),len(sector_two),len(sector_three),len(sector_one_segment),len(sector_two_segment),len(sector_three_segment),len(lap_number),len(lap_time))
    sector_one = sector_one[:minimum_all]
    sector_two = sector_two[:minimum_all]
    sector_three = sector_three[:minimum_all]
    sector_one_segment = sector_one_segment[:minimum_all]
    sector_two_segment = sector_two_segment[:minimum_all]
    sector_three_segment = sector_three_segment[:minimum_all]
    lap_number = lap_number[:minimum_all]
    lap_time = lap_time[:minimum_all]
    import matplotlib.pyplot as plt

    # Set the size of the figure (in inches)
    plt.figure(figsize=(12, 8))  # Width=12 inches, Height=8 inches

    # Your plotting code follows
    for i in range(len(lap_number)):
        # Split the sectors into parts
        sector_one_splits = split_value(sector_one[i], len(sector_one_segment[i]))
        sector_one_color = convert_to_color(sector_one_segment[i])
        sector_two_splits = split_value(sector_two[i], len(sector_two_segment[i]))
        sector_two_color = convert_to_color(sector_two_segment[i])
        sector_three_splits = split_value(sector_three[i], len(sector_three_segment[i]))
        sector_three_color = convert_to_color(sector_three_segment[i])

        # Plot each sector's parts
        bottom = 0
        for j in range(len(sector_one_splits)):
            plt.bar(lap_number[i], sector_one_splits[j], color=sector_one_color[j], bottom=bottom)
            bottom += sector_one_splits[j]
        plt.bar(lap_number[i], 0.5, color='gold',bottom=sector_one[i])
        for j in range(len(sector_two_splits)):
            plt.bar(lap_number[i], sector_two_splits[j], color=sector_two_color[j], bottom=bottom)
            bottom += sector_two_splits[j]
        plt.bar(lap_number[i], 0.5, color='gold', bottom=(sector_one[i]+sector_two[i]))
        for j in range(len(sector_three_splits)):
            plt.bar(lap_number[i], sector_three_splits[j], color=sector_three_color[j], bottom=bottom)
            bottom += sector_three_splits[j]
        plt.bar(lap_number[i], 0.5, color='gold', bottom=(sector_one[i]+sector_two[i]+sector_three[i]))

        # Get current y-axis limits
        y_min, y_max = plt.ylim()

        # Calculate an offset that ensures the text stays within bounds
        offset = 0.5  # Default offset
        if lap_time[i] + offset > y_max:
            offset = y_max - lap_time[i] - 0.1  # Adjust offset if it exceeds y_max

        # Add the text slightly above the bar
        plt.text(lap_number[i], lap_time[i] + offset, str(lap_time[i]) + "sec", rotation=90, ha='center', va='bottom', color='black')
    plt.bar(lap_number[-1]+1,160, color='white')
    # Set x-axis ticks and labels
    plt.xticks(lap_number, lap_number)

    # Labels and Title
    plt.xlabel('Lap number')
    plt.ylabel('Lap Time in seconds')
    plt.title('Lap Time for '+ driver_name)
    legend_elements = [Line2D([0], [0], color='blue', lw=1, label='pitlane'),
                       Line2D([0], [0], color='green', lw=1, label='green sector'),
                       Line2D([0], [0], color='yellow', lw=1, label='sector end'),
                       Line2D([0], [0], color='purple', lw=1, label='purple sector'),
                       Line2D([0], [0], color='grey', lw=1, label='no data'),
                        ]
    # Show plot
    plt.legend(handles=legend_elements)
    plt.show()










