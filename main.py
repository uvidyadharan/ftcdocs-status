import os
from pushbullet import PushBullet
import subprocess
import pickle

access_token = os.getenv('PUSHBULLET_ACCESS_TOKEN')
pb = PushBullet(access_token)
old_errors = []


while True:
    os.system('cd ./ftcdocs && git pull -f')

    status = subprocess.call(['make', '-C ftcdocs/docs/ linkcheck SPHINXOPTS="-W --keep-going -n"'])

    if status != 0:
        try:        
            with open('errors.pickle', 'rb') as f:
                old_errors = pickle.load(f)
        except:
            print("Could not load old errors")
            
        pb.push_note('FTC Docs Link Check failed', 'The FTC Docs Link Check failed. Please check the build logs.')

        with open("ftcdocs/docs/build/linkcheck/output.txt", "rb") as log:
            errors = [(line.strip()).split() for line in log]

        if old_errors != errors:
            for error in errors:
                if error not in old_errors:
                    pb.push_link("New Error", error)
                    
            with open('errors.pickle', 'wb') as f:
                pickle.dump(error, f)

