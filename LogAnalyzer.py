import os
import zipfile
from datetime import datetime, timedelta
from drain3 import TemplateMiner
#from logparser import Drain  # Assuming LogPai's Drain parser is installed

def extract_zip(zip_path, extract_to):
    """Extracts the zip file to a specified directory."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

from drain3 import TemplateMiner  # Ensure this import is present

def parse_logs(log_dir):
    """Parses log files in the directory and stores only ERROR logs with the source file name."""
    log_files = [f for f in os.listdir(log_dir) if f.endswith('.txt')]
    error_logs = []

    for log_file in log_files:
        log_path = os.path.join(log_dir, log_file)
        with open(log_path, 'r') as file:
            for line in file:
                # Split the log line into parts based on the provided format
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    timestamp = parts[0].strip()  # Extract timestamp
                    log_level = parts[2].strip()  # Extract log level
                    message = parts[5].strip()   # Extract log message

                    # Store only ERROR logs and include the source file name
                    if log_level == "ERROR":
                        error_logs.append(f"{timestamp} | Source: {log_file} | {log_level} | {message}")

    return error_logs

def analyze_events(events):
    """Analyzes ERROR events and groups them into 60-second intervals, removing duplicates."""
    event_dict = {}
    for event in events:
        try:
            # Extract timestamp from the event
            timestamp_str = event.split('|')[0].strip()
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
            rounded_time = timestamp - timedelta(seconds=timestamp.second % 60, microseconds=timestamp.microsecond)
            
            if rounded_time not in event_dict:
                event_dict[rounded_time] = set()  # Use a set to store unique events
            
            event_dict[rounded_time].add(event)  # Add the event to the set (duplicates are ignored)
        except Exception as e:
            print(f"Skipping line due to error: {e}")

    # Convert sets back to lists for saving to file
    for time in event_dict:
        event_dict[time] = list(event_dict[time])

    return event_dict

def save_events_to_file(event_dict, output_file):
    """Saves events grouped by 60-second intervals to a file."""
    with open(output_file, 'w') as file:
        for time, events in sorted(event_dict.items()):
            file.write(f"\nEvents at {time}:\n")
            for event in events:
                file.write(f"  {event}\n")

if __name__ == "__main__":
    zip_path = "vpnlogs_Apr_9.zip"  # Path to the zip file
    extract_to = "extracted_logs"  # Directory to extract logs
    output_file = "error_logs.txt"  # File to save the error logs

    # Step 1: Extract logs from the zip file
    extract_zip(zip_path, extract_to)

    # Step 2: Parse the logs
    events = parse_logs(extract_to)

    # Step 3: Analyze and group events
    event_dict = analyze_events(events)

    # Step 4: Save events to a file
    save_events_to_file(event_dict, output_file)

    print(f"Error logs have been saved to {output_file}")
