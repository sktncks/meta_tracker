import os, sys

# 1. env directory create
env_dir_gen = "virtualenv env"
# 2. activate virtual env
activate_env = "source env/bin/activate"
# 3. install lib in requriements.txt
requriements_install = "pip install -r root/requriements.txt"
os.system(env_dir_gen)
os.system(activate_env)
os.system(requriements_install)