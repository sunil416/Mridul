import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]:  %(message)s: ')

lsit_of_files = ["src/__init__.py",
                 "src/helper.py",
                 ".env",
                 "requirements.txt",
                 "setup.py",
                 "app.py",
                 "research/trials.ipynb"]
for filepath in lsit_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory: {filedir} for file: {filename}")
    with open(filepath, "w") as f:
        pass
        logging.info(f"Creating empty file: {filename} in directory: {filedir}")
    