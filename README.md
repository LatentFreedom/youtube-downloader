# How to Run the App
Open terminal and enter the following commands.

## 1. Create virtual environment with python.
There can be different python package versions for different python applications so having a python virtual environment will help keep *this* python application in the correct state to run properly.
```
python3 -m venv env
```

## 2. Enter virtual environment
```
source env/bin/activate
```

## 3. Within the virtual environment
Upgrade pip and install the required packages to run the python app.
```
pip install --upgrade pip
pip install -r requirements.txt
```
 
## 4. Running the app
```
usage: app.py [-h] [-u URL] [-a] [-p] [-o OUTPUTPATH]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Url
  -a, --audio           Save As Audio
  -p, --playlist        Playlist Url Provided
  -o OUTPUTPATH, --output OUTPUTPATH
                        Path to save output
```