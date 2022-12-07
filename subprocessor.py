import os
import subprocess

os.system("pip install -r requirements.txt -q")

dir_path = os.path.dirname(os.path.realpath(__file__))

subprocess.Popen(['python', dir_path+'\\interactions\clapDetect.py'])
subprocess.call(['python', dir_path+'\\main.py'])
