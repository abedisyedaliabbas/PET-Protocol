import os
import pandas as pd

# Create an empty list to store dictionaries of results
results = []

# Iterate over all files in the current directory
for filename in os.listdir("."):
    if filename.endswith(".log"):
        with open(filename, "r") as file:
            content = file.readlines()

        # Check for job completion
        if "Normal termination of Gaussian" in content[-1]:
            job_completion = "Job finished"
            error_details = ""
        else:
            job_completion = "Job error"
            error_details = "".join(content[-5:])  # Last 5 lines of the file

        # Check for the presence of imaginary frequencies
        if any("imaginary frequencies (negative Signs)" in line for line in content):
            freq_status = "Negative frequency"
        else:
            # Find the index of the keyword
            try:
                start_index = content.index(" Full mass-weighted force constant matrix:\n") + 1
                freq_lines = [line for line in content[start_index:] if "Low frequencies ---" in line]

                if len(freq_lines) > 1:
                    # Extract frequencies from the second line
                    second_freqs = [float(x) for x in freq_lines[1].split()[3:]]
                    if second_freqs[0] < 0:
                        freq_status = "Negative frequency"
                    else:
                        freq_status = "OK"
                else:
                    freq_status = "Incomplete data"
            except ValueError:
                freq_status = "Keyword not found"

        # Append results to list
        results.append({
            "Filename": filename,
            "Status": freq_status,
            "Job Completion": job_completion,
            "Error Details": error_details
        })

# Convert list of dictionaries to DataFrame
results_df = pd.DataFrame(results)

# Write the DataFrame to an Excel file
results_df.to_excel("frequency_check_results.xlsx", index=False)
