import os 

SHARED_PATH = os.path.dirname(os.path.abspath(__file__)) + "/share"
ENV_FILE_PATH = SHARED_PATH + "/worker.env"
IMAGE = "ainblockchain/ain-worker-staging:latest"
VERSION="1.4.31"
TRACKER_ADDR = "http://52.79.226.211:3031/tracker"