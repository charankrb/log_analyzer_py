import os
import json

def extract_success_samples(log_dir, output_file):
    """
    Extracts success samples (e.g., logs with 'EVENT' or 'INFO') from logs and stores them in a JSON file.
    """
    log_files = [f for f in os.listdir(log_dir) if f.endswith('.txt')]
    success_samples = []

    for log_file in log_files:
        log_path = os.path.join(log_dir, log_file)
        with open(log_path, 'r') as file:
            for line in file:
                # Split the log line into parts based on the provided format
                parts = line.strip().split('|')
                if len(parts) >= 6:
                    log_level = parts[2].strip()  # Extract log level
                    message = parts[5].strip()   # Extract log message

                    # Collect logs with 'EVENT' or 'INFO' as success samples
                    if log_level in ["EVENT", "INFO"]:
                        success_samples.append(f"{line.strip()} | Source: {log_file}")

    # Remove duplicates
    success_samples = list(set(success_samples))

    # Save success samples to a JSON file
    with open(output_file, 'w') as file:
        json.dump(success_samples, file, indent=4)

    print(f"Success samples have been saved to {output_file}")

if __name__ == "__main__":
    log_dir = "extracted_logs"  # Directory containing extracted logs
    output_file = "success_samples.json"  # File to store success samples

    # Extract success samples and save them
    extract_success_samples(log_dir, output_file)