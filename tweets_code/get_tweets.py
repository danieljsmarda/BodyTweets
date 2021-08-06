import time
from request_management import send_n_requests
from geolocation import geolocate_tweets

dump_path = '../private_data/dump.txt'
batch_path = '../private_data/batch.txt'

def handle_rate(request_fn):
    def wrapper(*args, max_time=900, **kwargs):
        start = time.time()
        request_fn(*args, **kwargs)
        end = time.time()
        elapsed = start - end
        if elapsed < max_time:
            time.sleep(max_time - elapsed + 1)
    return wrapper

def extract_next_token(filename):
    with open(filename, 'r', encoding='utf-16-le') as f:
        lines = f.read().splitlines()
        last_line = lines[-1]
        next_token = eval(eval(last_line))['meta']['next_token']
    return next_token

def init_batch():
    for i in range(1):
        next_token = extract_next_token(batch_path)
        send_n_requests(dump_path, batch_path, next_token=next_token, n=1)
        geolocate_tweets()
init_batch()
        