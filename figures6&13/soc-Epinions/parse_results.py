import os
import re
import csv

# Directory containing the log files
log_dir = "results"

# Output CSV file
output_file = "results.csv"

# Initialize the CSV file with headers
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["nodes", "cores", "repetition", "algorithm", "total time", "generateRR time", "selectseeds time"])

    # Loop through the files in the results folder
    for filename in os.listdir(log_dir):
        # Only process files that are log files and skip time files
        if filename.endswith(".txt") and "time" not in filename:
            # Extract the algorithm type (1D or 2D) from the file name
            if "1D" in filename:
                algorithm = "1D"
            elif "2D" in filename:
                algorithm = "2D"
            else:
                continue  # Skip files that don't match the expected pattern

            # Extract the nodes, cores, and repetition from the filename
            match = re.match(r'log_(\d+)n_(\d+)c_(\d)D_r(\d+)\.txt', filename)
            if match:
                nodes = int(match.group(1))
                cores = int(match.group(2))
                repetition = int(match.group(4))
            else:
                continue  # Skip files that don't match the expected pattern

            # Parse the log file to extract relevant time data
            with open(os.path.join(log_dir, filename), 'r') as log_file:
                log_content = log_file.read()

                # Extract the relevant times using regex
                total_time_match = re.search(r'Total Time:\s+([0-9.]+)\s+seconds', log_content)
                generateRR_time_match = re.search(r'Total Time\(generateRR\):\s+([0-9.]+)\s+seconds', log_content)
                selectseeds_time_match = re.search(r'Total Time\(selectseeds\):\s+([0-9.]+)\s+seconds', log_content)

                if total_time_match and generateRR_time_match and selectseeds_time_match:
                    total_time = total_time_match.group(1)
                    generateRR_time = generateRR_time_match.group(1)
                    selectseeds_time = selectseeds_time_match.group(1)

                    # Write the extracted data to the CSV
                    writer.writerow([nodes, cores, repetition, algorithm, total_time, generateRR_time, selectseeds_time])

print("Results have been saved to", output_file)

