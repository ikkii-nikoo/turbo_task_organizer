# NOTE : I COPIED THESE CODES FROM CHATGPT

import os
import time
import subprocess
import signal

file_path = "/home/biscuit/Documents/New_World/Fantasy/Python/Turbo_Task_Manager/turbo_task_manager_0/1/0/main.py"

command = ["python3", "-m", "turbo_task_manager_0.1.0.main"]

def get_last_modified_time(filepath):
    return os.path.getmtime(filepath)

if __name__ == "__main__":
    print(f"Watching for changes in {file_path} with a 100ms polling interval...")

    last_modified_time = get_last_modified_time(file_path)
    process = None

    try:
        while True:
            current_modified_time = get_last_modified_time(file_path)
            if current_modified_time != last_modified_time:
                print("Change detected. Restarting...")
                if process:
                    process.send_signal(signal.SIGINT)
                    process.wait()
                process = subprocess.Popen(command)
                last_modified_time = current_modified_time
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopped watching.")
    finally:
        if process:
            process.terminate()
            process.wait()
