import os
from pushbullet import PushBullet

access_token = os.getenv('PUSHBULLET_ACCESS_TOKEN')
pb = PushBullet(access_token)


while True:
    os.system('cd ./ftcdocs && git pull -f')

    status = os.subprocess.call('make', '-C docs/ linkcheck SPHINXOPTS="-W --keep-going -n"')

    if status != 0:
        pb.push_note('FTC Docs Link Check failed', 'The FTC Docs Link Check failed. Please check the build logs.')

        with open("ftcdocs/docs/build/linkcheck/output.txt", "rb") as log:
            log_data = pb.upload_file(log, "log.txt")

        pb.push_file(**log_data)

