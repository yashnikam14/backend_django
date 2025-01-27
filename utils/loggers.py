from pathlib import Path
from datetime import datetime

def log_into_file(logs):
    try:
        filename = "{}-logfile.log".format(datetime.now().strftime("%Y-%m-%d"))
        base_dir = Path.home() / 'users' / 'var'
        log_into_path = base_dir/filename

        base_dir.mkdir(parents=True, exist_ok=True)
        with open(log_into_path, 'a') as file:
            file.write("{}\n".format(logs))

    except Exception as e:
        print(str(e))
