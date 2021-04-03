# Hot To Run App
Open terminal and enter the following commands.

1. Create virtual environment with python
```
python3 -m venv menv
```

2. Enter virtual environment
```
source menv/bin/activate
```

3. Within virtual environment
```
pip install --upgrade pip
pip install -r requirements.txt
```

4. Running the app
```
usage: app.py [-h] [-u URL] [-a] [-p]

optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  Url
  -a, --audio        Save As Audio
  -p, --playlist     Playlist Url Provided
```