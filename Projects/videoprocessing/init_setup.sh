#!/bin/bash

echo [$(date)]: "START"

ENV_NAME="myenv310"
PYTHON_VERSION="3.10"

# Check if the environment already exists
if conda info --envs | grep -q "$ENV_NAME"; then
    echo [$(date)]: "Environment '$ENV_NAME' already exists. Skipping creation."
else
    echo [$(date)]: "Creating conda env '$ENV_NAME' with Python $PYTHON_VERSION"
    conda create -n $ENV_NAME python=$PYTHON_VERSION -y
fi

# Initialize conda (ensure conda activate works inside scripts)
eval "$(conda shell.bash hook)"

echo [$(date)]: "Activating environment '$ENV_NAME'"
conda activate $ENV_NAME

echo [$(date)]: "Installing requirements"
pip install -r requirements.txt

echo [$(date)]: "END"
