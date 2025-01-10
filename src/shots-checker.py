import json
import time
from datetime import datetime, timedelta
import os

# A dictionary to track performed shots for the current day
performed_shots = {}

# Path to the status file for sharing data with Flask
status_file_path = os.path.join(os.path.dirname(__file__), "status.json")

# Function to perform the shot
def perform_shot(shot):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ✅ Performing shot: Start Time = {shot['startTime']}, Duration = {shot['duration']} seconds")
    # Add your actual irrigation logic here

# Function to update the status file
def update_status_file(current_time, shots_status):
    try:
        status_data = {
            "current_time": current_time.strftime('%Y-%m-%d %H:%M:%S'),
            "shots": shots_status,
        }
        with open(status_file_path, "w") as status_file:
            json.dump(status_data, status_file, indent=4)
    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Failed to update status file: {e}")

# Main loop to check and perform shots
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🌟 Starting irrigation system monitoring...")
while True:
    try:
        config_path = os.path.join(os.path.dirname(__file__), "../config.json")
        with open(config_path, 'r') as file:
            config = json.load(file)

        current_time = datetime.now()

        # Log current time
        # print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] ⏰ Checking for scheduled shots...")

        # Reset performed_shots at midnight
        if len(performed_shots) > 0 and current_time.time() == datetime.min.time():
            print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] 🔄 New day detected. Resetting performed shots.")
            performed_shots.clear()

        # Track status of each shot
        shots_status = []
        for shot in config["shots"]:
            start_time_str = shot["startTime"]
            start_time_today = datetime.strptime(start_time_str, "%H:%M").time()
            start_datetime_today = datetime.combine(current_time.date(), start_time_today)

            if start_datetime_today <= current_time < start_datetime_today + timedelta(seconds=shot["duration"]):
                if start_time_today not in performed_shots:
                    perform_shot(shot)
                    performed_shots[start_time_today] = True
                    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📝 Shot recorded as performed: Start Time = {start_time_str}")
                status = "Active"
            elif current_time < start_datetime_today and start_time_today not in performed_shots:
                status = "Upcoming"
            else:
                status = "Completed" if start_time_today in performed_shots else "Missed"

            shots_status.append({"time": start_time_str, "status": status})

        # Update status file for Flask app
        update_status_file(current_time, shots_status)

        time.sleep(1)  # Sleep for 1 second before checking again

    except KeyboardInterrupt:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Script interrupted by user. Exiting.")
        break

    except Exception as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ❌ Error occurred: {e}")
