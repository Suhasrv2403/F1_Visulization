🏎️ F1 Data Analysis & Visualization

🚀 Overview

Analyze and visualize Formula 1 race data using the OpenF1 API. This project includes:
✅ Lap Time Analysis – Visualize lap times and sector performance.
✅ Speed Trap Analysis – Track speed readings over laps.
✅ Throttle & Brake Analysis – Compare throttle and brake usage.

📌 Features

📊 Lap Time Analysis: Bar charts of sector times and lap duration.

⚡ Speed Trap Data: Line plots of speed trap readings per lap.

🎛 Throttle & Brake Overlap: Dual-line charts of driver inputs.

🔧 Setup

Install dependencies:

pip install requests pandas matplotlib seaborn pymongo termcolor

Set SESSION_KEY with a valid OpenF1 API session key.

Run:

lap_time_analysis.py 🏁 for lap insights

speed_trap_analysis.py 📈 for speed tracking

throttle_brake_analysis.py 🎚 for throttle/brake comparison

📊 How It Works

Fetch Data from OpenF1 API / MongoDB.

Process & Sort by driver, lap, timestamps.

Visualize with interactive charts.

🔍 Example Outputs

Lap Time Chart 🏎 – Bar chart of sector times.

Speed Trap Chart ⚡ – Line graph tracking speed over laps.

Throttle/Brake Chart 🎛 – Overlapping line graph for pedal inputs.

📌 Notes

Ensure SESSION_KEY is correct.

Adjust chart settings (plt.figure(figsize=...)) for customization.

MongoDB is optional but enhances performance.

📜 License

Open-source under MIT License. Happy analyzing! 🚀

