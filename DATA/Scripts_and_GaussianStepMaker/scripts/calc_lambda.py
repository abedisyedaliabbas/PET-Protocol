import os
import subprocess
import glob
import csv
import matplotlib.pyplot as plt

# ================= USER CONFIGURATION =================
# CRITICAL: Replace the path below with the actual location of Multiwfn.exe
# Double check this path! It must end in .exe
MULTIWFN_PATH = r"C:\Users\Admin\Downloads\Multiwfn_3.8_dev_bin_Win64\Multiwfn_3.8_dev_bin_Win64\Multiwfn.exe"
# ======================================================

def run_calculation():
    # 1. Find and SORT files
    fchk_files = sorted(glob.glob("*.fchk"))
    
    if not fchk_files:
        print("No .fchk files found!")
        return

    print(f"Found {len(fchk_files)} files.")
    print("NOTE: Ensure your .log/.out files are in the same folder!")
    print("-" * 60)

    # 2. ASK USER FOR THE EXCITED STATE
    # The script pauses here and waits for you to type a number
    state_input = input(">> Enter the Excited State index you want to analyze (e.g. 1): ").strip()
    
    # Default to 1 if you just hit Enter
    if not state_input:
        state_idx = "1"
        print("No input detected. Defaulting to State 1.")
    else:
        state_idx = state_input
        print(f"Okay, calculating Lambda for State {state_idx}...")

    print("\n" + "="*80)
    print(f"{'Filename':<45} | {'Lambda':<10} | {'Status'}")
    print("="*80)

    results_data = []

    # 3. Loop through all files
    for file in fchk_files:
        # Check for corresponding .log or .out file
        base_name = os.path.splitext(file)[0]
        if os.path.exists(base_name + ".log"):
            log_exists = True
        elif os.path.exists(base_name + ".out"):
            log_exists = True
        else:
            print(f"{file:<45} | {'---':<10} | FAIL: No .log/.out file")
            continue

        # Prepare Multiwfn commands
        input_commands = [
            "18",           # Electron excitation analysis
            "14",           # Calculate lambda index
            "",             # Press ENTER to load the matching .log file
            state_idx,      # <--- Uses the state YOU typed (e.g. 1)
            "n",            # Print contributions? -> No
            "n",            # Do analysis again? -> No
            "0",            # Return
            "q"             # Quit
        ]
        
        input_str = "\n".join(input_commands)

        try:
            # Run Multiwfn
            process = subprocess.run(
                [MULTIWFN_PATH, file],
                input=input_str, text=True, capture_output=True,
                encoding='utf-8', errors='ignore'
            )

            # Extract Lambda Value
            lambda_val = None
            output_lines = process.stdout.splitlines()
            
            # Look for line: "Excited state 1: lambda = 0.683489"
            for line in output_lines:
                if "lambda =" in line:
                    parts = line.split("=")
                    lambda_val = float(parts[-1].strip())
                    break
            
            if lambda_val is not None:
                print(f"{file:<45} | {lambda_val:<10.4f} | OK")
                results_data.append([file, state_idx, lambda_val])
            else:
                print(f"{file:<45} | {'---':<10} | FAIL: Value not found")

        except Exception as e:
            print(f"{file:<45} | {'Error':<10} | {e}")

    # 4. Save to CSV
    csv_filename = "results_lambda.csv"
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Filename", "State", "Lambda"]) 
        writer.writerows(results_data)
    
    print("-" * 80)
    print(f"Data saved to: {csv_filename}")

    # 5. Plot Results
    if results_data:
        lambdas = [row[2] for row in results_data]
        x_axis = range(1, len(lambdas) + 1)

        plt.figure(figsize=(10, 6))
        plt.plot(x_axis, lambdas, marker='s', linestyle='-', color='g') 
        plt.title(f"Lambda Index (State {state_idx}) vs Scan Step")
        plt.xlabel("Scan Step")
        plt.ylabel("Lambda Index")
        plt.grid(True)
        
        plt.savefig("lambda_plot.png")
        plt.show()

if __name__ == "__main__":
    run_calculation()
