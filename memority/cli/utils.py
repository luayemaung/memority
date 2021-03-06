import time

import requests
from tqdm import tqdm


class Exit(Exception):
    pass


def get_url(path, port):
    return f'http://127.0.0.1:{port}{path}'


def post(url, port):
    r = requests.post(get_url(url, port), json={})
    data = r.json()
    if data.get('status') == 'error':
        raise Exit(f"Error: {data.get('message')}")
    return data.get('result')


def check_sync_status(port):
    data = post('/checks/sync_status/', port)
    syncing = data.get('syncing')
    percent = data.get('percent')
    if syncing:
        print('Please wait for the blockchain to sync.')
        with tqdm(total=100) as progressbar:
            while True:
                if percent == -1:
                    percent = 0
                progressbar.update(int(percent) - progressbar.n)
                time.sleep(.5)
                data = post('/checks/sync_status/', port)
                syncing = data.get('syncing')
                percent = data.get('percent')
                if not syncing:
                    progressbar.update(100 - progressbar.n)
                    progressbar.close()
                    break


def check_app_updates(port):
    data = post('/checks/app_updates/', port)
    update_available = data.get('update_available')
    download_url = data.get('download_url')
    if update_available:
        raise Exit(
            'Application update available!\n'
            f'You can download it on {download_url}'
        )


def check_contract_updates(port):
    update_available = post('/checks/contract_updates/', port)
    if update_available:
        raise Exit(
            'Smart Contract needs update.\n'
            'Please update it by calling "memority_cli account update_contract"'
        )


def perform_checks(port):
    check_sync_status(port)
    check_app_updates(port)
    check_contract_updates(port)
