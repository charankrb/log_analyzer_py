import os
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_success_samples(file_path):
    """
    Loads pre-stored success samples from a JSON file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Success samples file not found: {file_path}")
    
    with open(file_path, 'r') as file:
        success_samples = json.load(file)
    return success_samples

def parse_logs_from_dir(log_dir):
    """
    Reads all logs from the extracted_logs directory and returns them as a list of events.
    """
    log_files = [f for f in os.listdir(log_dir) if f.endswith('.txt')]
    logs = []

    for log_file in log_files:
        log_path = os.path.join(log_dir, log_file)
        with open(log_path, 'r') as file:
            logs.extend([line.strip() for line in file if line.strip()])
    return logs

def validate_logs_with_success_samples(logs, success_samples):
    """
    Validates logs against success samples using cosine similarity.
    """
    vectorizer = CountVectorizer().fit(success_samples + logs)
    success_vectors = vectorizer.transform(success_samples)
    log_vectors = vectorizer.transform(logs)

    results = []
    for i, log_vector in enumerate(log_vectors):
        similarities = cosine_similarity(log_vector, success_vectors).flatten()
        max_similarity = max(similarities)
        if max_similarity >= 0.8:  # Threshold for considering a match
            results.append((logs[i], "MATCH"))
        else:
            results.append((logs[i], "NO MATCH"))
    return results

def save_success_logs(results, output_file):
    """
    Saves logs with messages containing 'success' to a file.
    """
    with open(output_file, 'w') as file:
        for log, status in results:
            if "success" in log.lower():  # Check if 'success' is in the log message
                file.write(f"{log} | {status}\n")

if __name__ == "__main__":
    # File paths
    success_samples_file = "success_samples.json"  # Pre-stored success samples
    log_dir = "extracted_logs"                    # Directory containing extracted logs
    output_file = "success_logs.txt"              # Output file for logs with 'success'

    # Step 1: Load success samples
    success_samples = load_success_samples(success_samples_file)

    # Step 2: Parse logs from the directory
    logs = parse_logs_from_dir(log_dir)

    # Step 3: Validate logs with success samples
    validation_results = validate_logs_with_success_samples(logs, success_samples)

    # Step 4: Save logs with 'success' in the message
    save_success_logs(validation_results, output_file)

    print(f"Logs with 'success' have been saved to {output_file}")