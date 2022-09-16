import os
from pushbullet import PushBullet
import subprocess
import pickle

access_token = os.getenv('PUSHBULLET_ACCESS_TOKEN')
pb = PushBullet(access_token)
old_errors = []


while True:
    os.system('cd ./ftcdocs && git pull -f')
    
    env = os.environ.copy()
    env["SPHINXOPTS"] = "-W --keep-going -n"
    
    status = subprocess.call(['make', '-C', 'ftcdocs/docs/', 'linkcheck'], env=env)

    if status != 0:
        try:        
            with open('errors.pickle', 'rb') as f:
                old_errors = pickle.load(f)
        except:
            print("Could not load old errors")

        with open("ftcdocs/docs/build/linkcheck/output.txt", "rb") as log:
            errors = [(line.strip()).split() for line in log]

        if old_errors != errors:
            for error in errors:
                if error not in old_errors:
                    pb.push_note("New Error", str(error))
                    
            with open('errors.pickle', 'wb') as f:
                pickle.dump(error, f)

