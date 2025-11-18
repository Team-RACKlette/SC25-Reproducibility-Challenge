import os
import re
import csv

# Directory containing the log files
log_dir = "results"

# Output CSV file
output_file = "results_eps_parsed.csv"

# Initialize the CSV file with headers
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # UPDATED HEADERS: Only including algorithm, epsilon, and total time
    writer.writerow(["algorithm", "eps", "total time"])

    # Loop through the files in the results folder
    try:
        filenames = os.listdir(log_dir)
    except FileNotFoundError:
        print(f"Error: Directory '{log_dir}' not found. Please ensure your log files are in a folder named 'results'.")
        filenames = []

    for filename in filenames:
        # Only process files that start with 'log_k' and end with '.txt'.
        if filename.startswith("log_k") and filename.endswith(".txt"):

            # Extract algorithm (1D or 2D), epsilon, and repetition from the filename
            match = re.match(r'log_k(\d+)_(\d)D_e([0-9.]+)_r(\d+)\.txt', filename)
            if match:
                k_value = int(match.group(1))
                algorithm = f"{match.group(2)}D"
                eps = float(match.group(3))
                repetition = int(match.group(4))
            else:
                # Skip files that don't match the expected pattern
                print(f"Skipping file due to unexpected name pattern: {filename}")
                continue

            # Parse the log file to extract relevant time data
            file_path = os.path.join(log_dir, filename)
            try:
                with open(file_path, 'r') as log_file:
                    log_content = log_file.read()

                    # Extract only the Total Time using regex
                    total_time_match = re.search(r'Total Time:\s+([0-9.]+)\s+seconds', log_content)

                    if total_time_match:
                        total_time = total_time_match.group(1)

                        # Write the extracted data to the CSV
                        writer.writerow([algorithm, eps, total_time])
                    else:
                         print(f"Warning: Could not find 'Total Time' metric in {filename}. Skipping.")

            except FileNotFoundError:
                print(f"Error: File not found at {file_path}. Skipping.")
            except Exception as e:
                print(f"Error processing file {filename}: {e}. Skipping.")

print("Results have been saved to", output_file)

