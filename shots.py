import json
from datetime import datetime, timedelta
from prettytable import PrettyTable

# Load the configuration file
file_path = "config.json"
with open(file_path, 'r') as file:
    config = json.load(file)

# Get the current time
current_time = datetime.now()

# Prepare the table
table = PrettyTable()
table.field_names = ["Shot Start Time", "Shot End Time", "Status"]

# Add the current time as the first row
table.add_row(["Current Time", current_time.strftime("%Y-%m-%d %H:%M:%S"), "Now"])

# Process each shot
for shot in config["shots"]:
    # Convert startTime to today's datetime
    start_time_str = shot["startTime"]
    start_time_today = datetime.strptime(start_time_str, "%H:%M").time()
    start_datetime_today = datetime.combine(current_time.date(), start_time_today)
    
    # Add the duration to calculate the end time
    duration_minutes = shot["duration"]
    end_datetime_today = start_datetime_today + timedelta(seconds=duration_minutes)
    
    # Determine status
    if start_datetime_today <= current_time < end_datetime_today:
        status = "Active"
    elif current_time < start_datetime_today:
        status = "Upcoming"
    else:
        status = "Passed"
    
    # Add row to the table
    table.add_row([start_datetime_today, end_datetime_today, status])

# Print the table
print(table)
