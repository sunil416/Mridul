from setuptools import setup, find_packages
import os
from pathlib import Path

setup(name="eshopchatbot",
        version="0.0.1",
        author="Mridul ",
        author_email="abc@softsuave.org",
        packages=find_packages(),
        install_requires=['fastapi', 'uvicorn','pydantic','transformers','torch','sentence-transformers','pinecone-client'],
        )   