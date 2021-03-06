import requests

from ..utils import get_url


async def miner_request(args):
    r = requests.post(
        get_url('/miner_request/', port=args.memority_core_port),
        json={}
    )
    data = r.json()
    if data.get("status") == 'success':
        print(f'The request was successfully sent. Request status: {data.get("request_status")}.')
    else:
        print(f'Error sending request: {data.get("message")}')

