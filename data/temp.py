import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# OpenF1 API Configuration
BASE_URL = "https://api.openf1.org/v1/laps?"
SESSION_KEY = "9689"  # Replace with actual session key

# Fetch lap data for all drivers
def fetch_lap_data(session_key):
    url = f"{BASE_URL}session_key={session_key}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else []

# Retrieve data
data = fetch_lap_data(SESSION_KEY)

if not data:
    print("No data retrieved. Check session key.")
    exit()

# Convert to DataFrame
df = pd.DataFrame(data)

# Convert data types
df["date_start"] = pd.to_datetime(df["date_start"])
df["driver_number"] = df["driver_number"].astype(str)  # Ensure driver number is string
df["lap_number"] = df["lap_number"].astype(int)
df["lap_duration"] = df["lap_duration"].astype(float)
df["i1_speed"] = df["i1_speed"].astype(float)
df["i2_speed"] = df["i2_speed"].astype(float)
df["st_speed"] = df["st_speed"].astype(float)

df = df.dropna(subset=["date_start", "st_speed"])


# Sort data by session start time, lap number, and driver number
df = df.sort_values(by=["date_start", "lap_number", "driver_number"])

sns.set(style="darkgrid")

# Create subplots: one per driver
unique_drivers = df["driver_number"].unique()


# Plot each driver's data in a separate plot
# Iterate over unique drivers
for driver in unique_drivers:
    driver_data = df[df["driver_number"] == driver]

    # Fetch driver name once
    dn = requests.get(f'https://api.openf1.org/v1/drivers?driver_number={driver}&session_key={SESSION_KEY}')
    driver_name = dn.json()[0]["full_name"]
    plt.figure(figsize=(10, 6))

    # Extract lap numbers and speeds
    laps = driver_data["lap_number"].unique()
    speeds_i1 = [driver_data[driver_data["lap_number"] == lap]["i1_speed"].values[0] for lap in laps]

    plt.plot(laps, speeds_i1, marker='o', linestyle='-', color='blue', label="Speed Trap 1")

    # Annotate the points with speed values
    for lap, speed in zip(laps, speeds_i1):
        plt.text(lap, speed, f"{speed:.1f} km/h", ha='center', va='bottom')

    plt.xlabel('Lap Number')
    plt.ylabel('Speed (km/h)')
    plt.title(f'Driver {driver_name} - Speed Trap 1 vs Lap Number')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Speed Trap 2
    plt.figure(figsize=(10, 6))

    # Extract lap numbers and speeds
    speeds_i2 = [driver_data[driver_data["lap_number"] == lap]["i2_speed"].values[0] for lap in laps]

    plt.plot(laps, speeds_i2, marker='o', linestyle='-', color='red', label="Speed Trap 2")

    # Annotate the points with speed values
    for lap, speed in zip(laps, speeds_i2):
        plt.text(lap, speed, f"{speed:.1f} km/h", ha='center', va='bottom')

    plt.xticks(laps)
    plt.xlabel('Lap Number')
    plt.ylabel('Speed (km/h)')
    plt.title(f'Driver {driver_name} - Speed Trap 2 vs Lap Number')
    plt.legend()
    plt.grid(True)
    plt.show()







