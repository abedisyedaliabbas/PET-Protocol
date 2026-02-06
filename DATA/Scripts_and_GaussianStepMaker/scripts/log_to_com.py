"""
Syed Ali Abbas Abedi

"""
import os
import re

def extract_last_geometry(logfile_path):
    """
    Extract the last geometry block from the .log file.
    """
    geometry_blocks = []
    current_block = []

    # Regex to match lines that start with an optional space, then one or more word characters (atom symbol),
    # followed by one or more spaces, and then three floating-point numbers (coordinates).
    # Examples: " C    0.000000    0.000000    0.000000"
    #           "H  -1.234567  0.987654  -0.123456"
    atom_line_regex = re.compile(r'^\s*\w+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+')

    try:
        with open(logfile_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            if atom_line_regex.match(line):
                current_block.append(line)
            elif current_block: # If a line doesn't match the regex and we have a current block, it means the block ended
                geometry_blocks.append(current_block)
                current_block = [] # Reset for the next block

        # Add the last block if the file ends with a geometry block
        if current_block:
            geometry_blocks.append(current_block)

        if geometry_blocks:
            return geometry_blocks[-1] # Return the very last complete geometry block
        else:
            return [] # No geometry blocks found

    except FileNotFoundError:
        print(f"Error: The file '{logfile_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading '{logfile_path}': {e}")
        return []

def save_to_com(com_path, geometry_lines):
    """
    Save geometry block to a .com file at com_path.
    Includes standard Gaussian input header.
    """
    base_name = os.path.basename(os.path.splitext(com_path)[0])
    try:
        with open(com_path, 'w') as f:
            f.write(f'%chk={base_name}.chk\n')
            f.write('#p opt freq b3lyp/6-31g(d)\n\n')
            f.write('Title Card Required\n\n')
            f.write('0 1\n') # Charge and Multiplicity (e.g., 0 1 for neutral singlet)
            f.writelines(geometry_lines)
            f.write('\n') # Ensure a newline at the end of the geometry block for proper formatting
        print(f"Successfully saved: {com_path}")
    except IOError as e:
        print(f"Error: Could not write to file '{com_path}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred while saving '{com_path}': {e}")


if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Starting to process .log files in folder: {current_dir}")

    # Check if the directory exists
    if not os.path.isdir(current_dir):
        print(f"Error: The directory '{current_dir}' does not exist or is not accessible.")
    else:
        log_files_found = False
        for filename in os.listdir(current_dir):
            if filename.lower().endswith('.log'):
                log_files_found = True
                log_path = os.path.join(current_dir, filename)
                print(f"\nProcessing file: {log_path}")
                
                # Check if the log file actually exists before trying to process it
                if not os.path.exists(log_path):
                    print(f"Warning: File not found at expected path: {log_path}. Skipping.")
                    continue

                last_geometry = extract_last_geometry(log_path)
                if last_geometry:
                    # Save .com with same basename and same folder as .log file
                    base = os.path.splitext(filename)[0]
                    com_path = os.path.join(current_dir, base + '.com')
                    save_to_com(com_path, last_geometry)
                else:
                    print(f"No geometry found in {filename}. Skipping .com file creation.")
        
        if not log_files_found:
            print(f"No .log files found in the directory: {current_dir}")
        else:
            print("\nFinished processing all .log files.")

