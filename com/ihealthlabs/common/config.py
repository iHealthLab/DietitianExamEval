import os

from environs import Env

env = Env()
env.read_env(path=os.environ.get('ENV', '.env'))
