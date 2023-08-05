from setuptools import setup, find_packages

# prod: 1.9 , staging 1.2
NAME = "ain-worker-staging"
VERSION = "1.4.32"

packages = [
  "setuptools",
  "wheel",
  "python-dotenv==0.10.1",
  "docker==3.7.0",
  "requests-unixsocket==0.1.5",
  "requests",
  "click==7.0"
]

setup(
  package_data = {
    '': ['share/*.env','share/log/*.env'],
    'share/log': ['*.env'],
    'share': ['*.env'],
  },
  name = NAME,
  version = VERSION,
  python_requires='>=3',
  description = "CLI of " + NAME + " a Python script",
  license = "BSD",
  url = "https://bitbucket.org/comcomai/ain-v1-worker",
  packages=find_packages(),
  install_requires=packages,
  entry_points = {
    'console_scripts' : ['ain = ain.ain:call']
  },
  classifiers=[
    "License :: OSI Approved :: BSD License"
  ]
)
