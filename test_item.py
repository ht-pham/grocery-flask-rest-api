from db import items
import pytest
import requests


BASE_URL = "http://127.0.0.1:5000/item/"

def test_get_all_items():
    get_all_url = BASE_URL+"all"
    response = requests.get(get_all_url)
    response_text = response.json()
    assert response.status_code == requests.codes.accepted
    assert response_text['0'] == items[0]

def test_initial_item():
    url = BASE_URL+"0"
    response = requests.get(url)
    response_text = response.json()
    assert response.status_code == requests.codes.ok
    assert response_text == items[0]

def test_put_item():
    url = BASE_URL+"0"
    response = requests.put(url,params={"brand":"rebranded","price":5.99})
    response_text = response.json()
    assert response.status_code == requests.codes.ok
    assert response_text == items[0]