import subprocess

clap_process = subprocess.Popen(["python clapProgram.py"])
main_process = subprocess.call(["python main.py"])

