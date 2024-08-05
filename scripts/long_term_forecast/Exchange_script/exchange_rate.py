import os
import subprocess
from datetime import datetime

# Path to the directory containing the .sh files
scripts_dir = 'scripts/long_term_forecast/Exchange_script'

# Path to the logs directory
logs_dir = os.path.join(scripts_dir, 'logs')

# Create the logs directory if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)

# Get a list of all .sh files in the scripts directory
sh_files = [f for f in os.listdir(scripts_dir) if f.endswith('.sh')]

# Get the full paths and modification times of the .sh files
sh_files_with_time = [(f, os.path.getmtime(os.path.join(scripts_dir, f))) for f in sh_files]

# Sort the files by modification time
sh_files_sorted = sorted(sh_files_with_time, key=lambda x: x[1])

# Execute each .sh file in sorted order and log the output
for sh_file, _ in sh_files_sorted:
    sh_file_path = os.path.join(scripts_dir, sh_file)
    log_file_path = os.path.join(logs_dir, f'{sh_file}.log')
    
    try:
        # Change the permission to make the file executable
        subprocess.run(['chmod', '+x', sh_file_path], check=True)
        
        # Run the shell script and capture the output
        print(f'Executing {sh_file}...')
        result = subprocess.run(['bash', sh_file_path], capture_output=True, text=True)
        
        # Write the output to a log file
        with open(log_file_path, 'w') as log_file:
            log_file.write(f'Execution Date: {datetime.now()}\n\n')
            log_file.write('STDOUT:\n')
            log_file.write(result.stdout)
            log_file.write('\n\nSTDERR:\n')
            log_file.write(result.stderr)
        
        print(f'Output for {sh_file} logged to {log_file_path}')
    
    except subprocess.CalledProcessError as e:
        print(f'Error executing {sh_file}: {e}')

    except Exception as e:
        print(f'Unexpected error occurred while executing {sh_file}: {e}')
