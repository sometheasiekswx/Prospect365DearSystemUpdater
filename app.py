from flask import Flask, render_template
import requests
import datetime
import json
import logging
from apscheduler.schedulers.background import BackgroundScheduler
import time


logger = logging.getLogger('prospect_dear')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logging.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)


def update_datetime_file(last_updated):
    now = datetime.datetime.now()
    with open('last_updated.txt', 'w') as f:
        f.write(str(last_updated))


def get_datetime_from_file():
    with open('last_updated.txt', 'r') as f:
        datetime_str = f.read().strip()
        return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')


def get_prospect_quotes(last_ran):
    url = f"https://crm-odata-v1.prospect365.com/Quotes?%24filter=LastUpdatedTimestamp gt {last_ran.strftime('%Y-%m-%dT%H:%M:%S.%fZ')} and CreatedByUserId ne 'DBA' and StatusFlag eq 'A'"
    msg = f'Getting Quotes using {url}'
    logger.info(msg)
    print(msg)
    payload = {}
    headers = {
        'Authorization': 'Bearer ce58ee2da8077b7da37ffda25c6b3768'
    }
    response = requests.request('GET', url, headers=headers, data=payload)
    return response.json()['value']


def get_dear_sale(id):
    url = f'https://inventory.dearsystems.com/ExternalApi/Sale?ID={id}'
    payload = ''
    headers = {
        'api-auth-accountid': '1c86256d-59e5-435c-86f3-5541e59b61c6',
        'api-auth-applicationkey': 'cd9c11d4-3ff0-4e94-0c79-f9fccbe135f0',
    }
    response = requests.request('GET', url, headers=headers, data=payload)

    return response.json()


def update_dear_sale(new_sale):
    url = 'https://inventory.dearsystems.com/ExternalApi/v2/sale'

    headers = {
        'api-auth-accountid': '1c86256d-59e5-435c-86f3-5541e59b61c6',
        'api-auth-applicationkey': 'cd9c11d4-3ff0-4e94-0c79-f9fccbe135f0',
        'Content-Type': 'application/json',
        'Cookie': 'DEARAffinity=1c8086f6bee5867d714c634b297a636f; DEARAffinityCORS=1c8086f6bee5867d714c634b297a636f'
    }
    response = requests.request(
        'PUT', url, headers=headers, data=json.dumps(new_sale))
    return response


def run_updater():
    msg = 'Running Updater'
    logger.info(msg)
    print(msg)

    last_ran = get_datetime_from_file()
    prospect_quotes = get_prospect_quotes(last_ran)
    sale__qoute_time = []
    updated = 0
    last_updated = ''
    for prospect_quote in prospect_quotes:
        accounts_id = prospect_quote['AccountsId']
        if accounts_id is not None:
            quote_id = prospect_quote['QuoteId']
            last_updated = datetime.datetime.strptime(
                prospect_quote['LastUpdatedTimestamp'].strip(), '%Y-%m-%dT%H:%M:%S.%fZ')
            new = last_updated > last_ran
            sale__qoute_time.append(
                {'accounts_id': accounts_id, 'quote_id': quote_id, 'last_updated': last_updated, 'new': new})

            if new:
                dear_sale = get_dear_sale(accounts_id)
                logger.debug(dear_sale)
                new_dear_sale = {
                    'ID': dear_sale.get('ID'),
                    'Customer': dear_sale.get('Customer'),
                    'CustomerID': dear_sale.get('CustomerID'),
                    'Location': dear_sale.get('Location'),
                    'AdditionalAttributes': {
                        'AdditionalAttribute7': f'https://crm.prospect365.com/view/Quotation/{quote_id}',
                    }
                }
                response = update_dear_sale(new_dear_sale)
                if response.status_code != 200:
                    print(response.text)
                    logger.error(response.text)
                    logger.error(
                        f'accounts_id: {accounts_id}, quote_id: {quote_id}, last_updated: {last_updated}, last_ran: {last_ran}, new?: {new}')
                else:
                    updated += 1
                    logger.info(response.text)
                    success_msg = f'Updated Sale https://inventory.dearsystems.com/Sale#{accounts_id} with Quote https://crm.prospect365.com/view/Quote/{quote_id}'
                    print(success_msg)

    update_datetime_file(last_updated)

    msg = 'Updated last_updated.txt & Updater has completed'
    logger.info(msg)
    print(msg)

    return len(sale__qoute_time), updated



app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/')
def all_links():
    return render_template('all_links.html', title='All Links')

@app.route('/run')
def run():
    checked, updated = run_updater()
    return f'Complete! {checked} records checked and {updated} records updated'


@app.route('/run/minutes/<int:interval>')
def run_every_minute(interval):
    scheduler.add_job(func=run_updater, trigger='interval', minutes=interval)
    scheduler.start()
    return f'Updater is now running every {interval} minute'


@app.route('/run/minutes/stop')
def stop_run_every_minute():
    scheduler.shutdown()
    return f'Updater is now shutdown'
