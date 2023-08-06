#!/usr/bin/env python3

import requests

# custom hub via $PWD/.fsm-hub
hub = "http://localhost:1024"
try:
    hub = open(".fsm-hub").read().strip() or hub
except FileNotFoundError:
    pass

http = requests.Session()

def config():
    rsp = http.get(f"{hub}/")
    rsp.raise_for_status()
    return rsp.json()

def get(id):
    rsp = http.get(f"{hub}/{id}")
    rsp.raise_for_status()
    payload = rsp.json()

def new(state):
    rsp = http.post(f"{hub}/lock/{module_name}")
    rsp.raise_for_status()
    return rsp.json()

def lock(state):
    rsp = http.post(f"{hub}/lock/{module_name}")
    rsp.raise_for_status()
    return rsp.json()

def transit(id, next_state, patch_data):
    rsp = http.post(f"{hub}/transit/{id}/{next_state}", json=patch_data)
    rsp.raise_for_status()  # hub is gone or logic is broken, so just exit

if __name__ == '__main__':
    pass
