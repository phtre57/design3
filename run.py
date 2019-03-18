import argparse
import subprocess

parser = argparse.ArgumentParser(description='Process some integers.')
optional = parser._action_groups.pop()
optional.add_argument('--cov')
optional.add_argument('--test')
optional.add_argument('--install')
args = parser.parse_args()

# Emergency pip uninstall -y (pip freeze)

def main():
    if (args.install):
        print("Press any key to continue, pip install functions will be executed.")
        print("You will suffer, not me.")
        print("Over.")
        input()
        subprocess.call('pip install --upgrade pyzbar', shell=True)
        subprocess.call('pip install --upgrade opencv-python', shell=True)
        subprocess.call('pip install --upgrade coverage', shell=True)
        subprocess.call('pip install --upgrade python-socketio[client]', shell=True)
        subprocess.call('pip install --upgrade imutils', shell=True)
        subprocess.call('pip install --upgrade requests', shell=True)
    elif (args.cov):
        subprocess.call('coverage run -m unittest discover . "*Test.py"', shell=True)
        subprocess.call('coverage report -m', shell=True)
    elif (args.test):
        subprocess.call('python -m unittest discover . "*Test.py"', shell=True)
    else:
        subprocess.call('start cmd /k yarn main', shell=True)
        subprocess.call('start cmd /k yarn start', shell=True)
        subprocess.call('start cmd /k yarn client', shell=True)

main()