# ANPR TUMO
Experimental project with TUMO students to build automatic number-plate recognition system

# Setup
If you are doing this first time, then please go over all following steps.
Please remember you should do this just once

## Creating the environment

After cloning go to anpr_tumo directory and create python virtual environment

## For Ubuntu

```Bash
    cd anpr_tumo
    mkdir env
    sudo apt update
    sudo apt install python3-venv
    python3 -m venv env
```

# Activating the environment

Call the following command in your terminal in order to activate the environment.

```Bash
    source env/bin/activate
```
You can make the alias of the activating command

# Usage


```Bash
    export PYTHONPATH=${PYTHONPATH}:$(pwd)/src
    python3 src/bin/anpr.py --config <config_name> --image <image_path>
```

for example
```Bash
    python3 src/bin/anpr.py --config aws_textract --image ~/Pictures/car.jpg
```

# OpenAlpr Setup
```Bash
Download openalpr-2.3.0-win-64bit.zip from GitHub  https://github.com/openalpr/openalpr/releases
Open alpr Application file
Download OpenALPR source code from GitHub   https://github.com/openalpr/openalpr/releases
For python binding go to \openalpr-2.3.0\src\bindings\python folder
python setup.py install

Official guide https://github.com/openalpr/openalpr/wiki/Compilation-instructions-(Windows)
```