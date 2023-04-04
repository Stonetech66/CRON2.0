from fastapi.testclient import TestClient
from fastapi import HTTPException 
from ..main import app
from unittest.mock import MagicMock, patch
from ..dependencies import get_current_user 
from .crud import Cron
client = TestClient(app)

auth_user={
    '_id' : '', 
    'email': 'cron@gmail.com', 
    'fullname': 'cronn job'
}
unauth_user= HTTPException(detail='invalid token or token has expired', status_code=401)
auth_header={'Authorization': 'Bearer Xxxxxxxxxxx'}



def test_get_crons():
  # Authenticated Request 
  with patch('CRON2.dependencies.get_current_user', MagicMock(return_value=auth_user)) :
    Cron.get_crons=MagicMock(return_value=[]) 
    resp=client.get('/v1/crons', headers=auth_header)
    assert resp.status_code == 200
    assert resp.json() == []

  # Unauthenticated Request
  with patch('CRON2.dependencies.get_current_user', MagicMock(side_effect=unauth_user)) : 
    resp=client.get('/v1/crons')
    assert resp.status_code == 401


def test_get_cron():
    # Authenticated Request 
    get_current_user=MagicMock(return_value=auth_user)
    response_data={
   "id": "642c2d7ea0209c97a399b860","url": "https://example.com","method": "get",
    "headers": {"Authorization": "Bearer xxxxxxx" },
    "body": None, "schedule": {"notify_on_error": False,
    "years": 0,"month": 0, "weekday": "MO", "days": 0, "hours": 9, "minutes": 0,
    "timezone": "Africa/Lagos","date_created": "2023-04-04T14:00:30.681282",
    "next_execution": "2023-04-10T09:00:00+01:00" } }
    Cron.get_cron= MagicMock(return_value=response_data)
    resp=client.get('/api/v1/cron/642c2d7ea0209c97a399b860', headers=auth_header)
    assert resp.status_code == 200
    assert resp.json() == cron_data

    # Unauthenticated Request 
    get_current_user= MagicMock(side_effect=unauth_user)
    resp=client.get('/api/v1/cron/642c2d7ea0209c97a399b860')
    assert resp.status_code == 401
    assert resp.json() == auth_error
    
    # Invalid Cron Id
    get_current_user= MagicMock(return_value=auth_user)
    Cron.get_cron= MagicMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.get('/api/v1/cron/642c2d7ea0209c97a399b899')
    assert resp.status_code == 404



def test_update_cron():
    # Authenticated Request 
    get_current_user= MagicMock(return_value=auth_user)
    response_data={"id": "642c2d7ea0209c97a399b860", "url":"https://example2.com","method": "get",
    "headers": { "Authorization": "Bearer xxxxxxx" }, "body": None,"schedule": {
    "notify_on_error": False,"years": 0,"month": 0,
    "weekday": "TUE","days": 0,"hours": 9,"minutes": 0,"timezone":"Africa/Lagos","date_created":"2023-04-04T14:00:30.681282","next_execution": "2023-04-10T09:00:00+01:00" }}
    Cron.update_cron= MagicMock(return_value=response_data)
    update_json={"url": "https://example2.com", "method": "get",
              "headers": {"Authorization": "Bearer xxxxxxx"},
               "timezone":"Africa/Lagos", "weekday":"TUE", "hours":9,"minutes":0,"notify_on_error": False}    
    resp= client.put('/api/v1/update-cron/642c2d7ea0209c97a399b860', headers=auth_header, json=update_json)
    assert resp.status_code == 200
    assert resp.json() == cron_data 

    # Unauthenticated Request 
    get_current_user= MagicMock(side_effect=unauth_user)
    resp=client.put('/api/v1/update-cron/642c2d7ea0209c97a399b860', json=update_json)
    assert resp.status_code == 401
   
    # invalid Cron ID 
    get_current_user= MagicMock(return_value=auth_user)
    Cron.update_cron = MagicMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.put('/api/v1/update-cron/642c2d7ea0209c97a399b756', headers=auth_header, json=json)
    assert resp.status_code == 404


def test_delete_cron():
    #Authenticated Request
    get_current_user= MagicMock(return_value=auth_user)
    Cron.delete_cron=MagicMock(return_value=True) 
    resp=client.delete('/api/v1/delete-cron/642c2d7ea0209c97a399b860', headers=auth_header)
    assert resp.status_code == 204

    # Unauthenticated Request 
    get_current_user= MagicMock(return_value=unauth_user)
    resp=client.delete('/api/v1/delete-cron/642c2d7ea0209c97a399b860')
    assert resp.status_code == 401

    # invalid Cron ID 
    get_current_user= MagicMock(return_value=auth_user)
    Cron.delete_cron = MagicMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.delete('/api/v1/delete-cron/642c2d7ea0209c97a399b560', headers=auth_header)
    assert resp.status_code == 404


def test_get_cron_response_history():
    pass

def test_delete_cron_response_history():
    pass

def test_get_response():
   pass

def test_delete_response():
   pass
