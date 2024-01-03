"""import os

try:
  import requests
except ImportError:
  print("Trying to Install required module: requests\n")
  os.system('python -m pip install requests')

try:
  import pycountry
except ImportError:
  print("Trying to Install required module: pycountry\n")
  os.system('python -m pip install pycountry')"""
import subprocess
import sys


def install1(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def install2(package):
    command = "yes | " + sys.executable + " -m pip install " + package
    subprocess.run(command, shell=True, check=True)


def install_all():
    try:
        package = "django-request"
        install2(package)
        packages = ["pycountry", "pycountry_convert", "requests"]
        for package in packages:
            try:
                install1(package)
            except:
                pass
        print("Required packages installed successfully")
    except subprocess.CalledProcessError as e:
        pass
