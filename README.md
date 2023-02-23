# Prospect Quote Dear Sale Updater

## Install and run

- Ensure all the correct Prospect365 and DearSystem API keys, Authorization bearer, and Account details are added in app.py

- Run the following
```console
. venv/bin/activate
OR
source venv/bin/activate
```
```console
pip install -r requirements.txt
OR
pip3 install -r requirements.txt
```
```console
python flask --app app run --debug 
OR
python3 -m flask run --debug
```

- Flask app will be running on http://127.0.0.1:5000

## Endpoints

||||
|--- |--- |--- |
|URL|Methods|Endpoint|
|/run|GET|Run the Updater|
|/run/minutes/<int:interval>|GET|For example /run/minutes/60 will run the Updater every 60 minutes|
|/run/minutes/stop|GET|Use to stop the Updater from running every X minutes|

### Notes

- Logs are found in `logging.log`  
- Last updated datetime is found in `last_updated.txt`