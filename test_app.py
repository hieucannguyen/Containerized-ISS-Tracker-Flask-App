import pytest
import requests

def test_comment_route():
    response = requests.get('http://127.0.0.1:5000/comment')
    assert response.status_code == 200
    assert isinstance(response.json(), list) == True

def test_header_route():
    response = requests.get('http://127.0.0.1:5000/header')
    assert response.status_code == 200
    assert response.json()['ORIGINATOR'] == 'JSC'
    assert isinstance(response.json(), dict) == True

def test_metadata_route():
    response = requests.get('http://127.0.0.1:5000/metadata')
    assert response.status_code == 200
    assert response.json()['CENTER_NAME'] == 'EARTH'
    assert isinstance(response.json(), dict) == True

def test_epochs_route():
    response = requests.get('http://127.0.0.1:5000/epochs')
    assert response.status_code == 200
    assert isinstance(response.json(), list) == True

def test_epochs_query_route():
    response = requests.get('http://127.0.0.1:5000/epochs?limit=2&offset=1')
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert isinstance(response.json(), list) == True

def test_specific_epoch_route():
    response1 = requests.get('http://127.0.0.1:5000/epochs')
    a_epoch = response1.json()[0]['EPOCH']
    print(a_epoch)
    response2 = requests.get('http://127.0.0.1:5000/epochs/'+a_epoch)
    assert response2.status_code == 200
    assert isinstance(response2.json(), dict) == True
