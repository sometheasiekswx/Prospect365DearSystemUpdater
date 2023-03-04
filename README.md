# Prospect Quote Dear Sale Updater

## Install and run

- Ensure all the correct Prospect365 and DearSystem API keys, Authorization bearer, and Account details are added in app.py
- Change directory to the Prospect365DearSystemUpdater folder (ex. /home/ubuntu/Prospect365DearSystemUpdater)
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

## 03/03-2023 Update - Installed on Ubuntu server

App is now running in the background on the Ubuntu server 

Code location: /home/ubuntu/Prospect365DearSystemUpdater

### Set New Interval

- Log unto the ubuntu server 
- Visit the URL http://127.0.0.1:5000/run/minutes/stop in a browser OR running

```
wget http://127.0.0.1:5000/run/minutes/stop
```

-  Set new interval by visiting the URL http://127.0.0.1:5000/run/minutes/{your new interval} OR running

```
wget http://127.0.0.1:5000/run/minutes/{your new interval}
```

### If updater is down, run
```console
. venv/bin/activate
```
```console
pip3 install -r requirements.txt
```
```
nohup python3 -m flask run >/dev/null & disown
```