import os 
import dotenv

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
SHARED_PATH = ROOT_PATH + "/share"
ENV_FILE_PATH = SHARED_PATH + "/worker.env"
TRACKER_ADDR = "https://staging.server.ainetwork.ai/tracker/"

ENVS = dotenv.dotenv_values(ROOT_PATH + "/.env.development")
IMAGE = ENVS["IMAGE"]
VERSION = ENVS["VERSION"]