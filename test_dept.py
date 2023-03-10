from db import depts
import pytest
import requests


BASE_URL = "http://localhost:5000/dept/"

def test_dept_list():
    get_all_url = BASE_URL+"all"
    response = requests.get(get_all_url)
    response_text = response.json()
    assert response.status_code == requests.codes.ok
    assert response_text["all_depts"] == list(depts.keys())

def test_dept_subcat():
    url = BASE_URL+"Dairy"
    response = requests.get(url)
    response_text = response.json()
    assert response.status_code == requests.codes.ok
    assert response_text["Dairy"] == list(depts["Dairy"]["subcategories"])

def test_dept_itemlist():
    url = BASE_URL+"Dairy/items"
    response = requests.get(url)
    response_text = response.json()
    assert response.status_code == requests.codes.ok
    assert response_text["Dairy"] == list(depts["Dairy"]["items"])

def test_invalid_dept():
    response = requests.get(BASE_URL+"bk")
    response_text = response.json()
    assert response.status_code == requests.codes.not_found
    assert response_text["message"] == "Store not found"
    