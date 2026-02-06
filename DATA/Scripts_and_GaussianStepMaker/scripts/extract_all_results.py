import os
import pandas as pd
import re

def extract_gaussian_data(file_path):
    filename = os.path.basename(file_path)
    
    # Initialize data dictionary
    data = {
        "Step": "Unknown",
        "Filename": filename,
        "Termination": "Error",
        "Freq_Status": "N/A",
        "Energy_Type": "None",
        "Root": 1,  # Default to Root 1 if not specified
        "Energy_Hartree": None,
        "Oscillator_Strength": None
    }

    # Detect Step from filename
    match = re.match(r"^(\d+)", filename)
    if match:
        data["Step"] = match.group(1)

    # Temporary storage variables
    current_root_idx = 0
    current_root_f = 0.0
    
    # Variables to store the last found values
    last_scf = None
    last_tddft = None
    last_clr = None

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        # -------------------------------------------------------
        # 1. PRE-SCAN: Check Route Card for "Root=N"
        # -------------------------------------------------------
        # Sets a default target root based on user input keywords
        for line in lines[:50]: 
            if line.strip().startswith("#"):
                root_match = re.search(r"root=(\d+)", line, re.IGNORECASE)
                if root_match:
                    data["Root"] = int(root_match.group(1))
                    break

        # -------------------------------------------------------
        # 2. PARSE FILE LINE-BY-LINE
        # -------------------------------------------------------
        for i, line in enumerate(lines):
            
            # --- Capture Energies ---
            if "SCF Done:" in line:
                try:
                    match_scf = re.search(r"SCF Done:.*=\s*([-+]?\d+\.\d+)", line)
                    if match_scf: last_scf = float(match_scf.group(1))
                except: pass

            if "Total Energy, E(TD-HF/TD-DFT)" in line:
                try:
                    match_td = re.search(r"=\s*([-+]?\d+\.\d+)", line)
                    if match_td: last_tddft = float(match_td.group(1))
                except: pass

            if "Total energy after correction" in line:
                try:
                    match_clr = re.search(r"correction\s*=?\s*([-+]?\d+\.\d+)", line)
                    if match_clr: last_clr = float(match_clr.group(1))
                except: pass

            # --- Capture Excited State Info ---
            # Format: " Excited State   3:      Singlet-A      2.2103 eV ... f=1.2340 "
            if "Excited State" in line and "f=" in line:
                try:
                    # Extract Root Number
                    root_match = re.search(r"Excited State\s+(\d+):", line)
                    if root_match:
                        current_root_idx = int(root_match.group(1))
                    
                    # Extract Oscillator Strength
                    f_match = re.search(r"f=\s*(\d+\.\d+)", line)
                    if f_match:
                        current_root_f = float(f_match.group(1))

                    # If this matches our expected Root, grab the 'f' value temporarily.
                    # (This will be confirmed or overwritten if the 'Optimization' flag appears below)
                    if current_root_idx == data["Root"]:
                        data["Oscillator_Strength"] = current_root_f
                        
                except: pass

            # --- CHECK FOR OPTIMIZATION FLAG ---
            # This line confirms exactly which state Gaussian is tracking.
            if "This state for optimization" in line:
                data["Root"] = current_root_idx
                data["Oscillator_Strength"] = current_root_f

        # -------------------------------------------------------
        # 3. CHECK TERMINATION & FREQUENCIES
        # -------------------------------------------------------
        if len(lines) > 0:
            full_text = "".join(lines[-5:])
            if "Normal termination" in full_text:
                data["Termination"] = "Normal"
        
        # Frequency Check
        negative_flag = any("imaginary frequencies (negative Signs)" in l for l in lines)
        freq_table_found = False
        min_freq = 9999
        
        for line in lines:
            if "Low frequencies ---" in line:
                freq_table_found = True
                try:
                    freqs = [float(x) for x in line.split()[3:]]
                    if freqs: min_freq = min(min_freq, min(freqs))
                except: pass

        if negative_flag or (freq_table_found and min_freq < 0):
            data["Freq_Status"] = "NEGATIVE FREQ"
        elif freq_table_found:
            data["Freq_Status"] = "OK"
        else:
            data["Freq_Status"] = "No Freq Calc"

        # -------------------------------------------------------
        # 4. FINALIZE ENERGY ASSIGNMENT
        # -------------------------------------------------------
        step = data["Step"]

        if step in ["01", "05", "07", "11", "15"]:
            data["Energy_Type"] = "SCF Done"
            data["Energy_Hartree"] = last_scf
            data["Root"] = "Ground" 
            data["Oscillator_Strength"] = None 

        elif step in ["02", "04", "08", "12", "13"]:
            data["Energy_Type"] = "TD-DFT Total"
            data["Energy_Hartree"] = last_tddft

        elif step in ["03", "06", "10", "14"]:
            data["Energy_Type"] = "cLR Corrected"
            data["Energy_Hartree"] = last_clr

        # Fallbacks for unknown steps
        if data["Energy_Hartree"] is None:
            if last_tddft is not None:
                data["Energy_Hartree"] = last_tddft
                data["Energy_Type"] = "TD-DFT (Fallback)"
            elif last_scf is not None:
                data["Energy_Hartree"] = last_scf
                data["Energy_Type"] = "SCF (Fallback)"

    except Exception as e:
        print(f"Error parsing {filename}: {e}")

    return data

def main():
    target_dir = os.getcwd()
    print(f"Scanning directory: {target_dir}")

    files = sorted([f for f in os.listdir(target_dir) if f.endswith(".log")])
    if not files:
        print("No .log files found!")
        return

    all_results = []
    print(f"Found {len(files)} log files. Processing...")

    for f in files:
        result = extract_gaussian_data(os.path.join(target_dir, f))
        all_results.append(result)

    # Create DataFrame
    df = pd.DataFrame(all_results)
    
    # Order Columns
    cols = ["Step", "Filename", "Termination", "Freq_Status", "Energy_Type", "Root", "Energy_Hartree", "Oscillator_Strength"]
    for c in cols:
        if c not in df.columns: df[c] = None
    df = df[cols]

    # Save
    output_xlsx = "Summary_Data.xlsx"
    df.to_excel(output_xlsx, index=False)
    print(f"\nSuccess! Data saved to {output_xlsx}")

if __name__ == "__main__":
    main()

