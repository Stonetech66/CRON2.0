from fastapi.testclient import TestClient
from fastapi import HTTPException, Header
from ..main import app
from unittest.mock import MagicMock, patch, AsyncMock
from CRON2.dependencies import get_current_user 
from .crud import Cron
from bson.objectid import ObjectId 
client = TestClient(app)

async def auth_user():
 return {'_id' : ObjectId('642c2d7ea0209c97a399b869'), 'email': 'cron@gmail.com', 'fullname': 'cronn job'}

async def unauth_user():
  raise HTTPException(detail='invalid token or token has expired', status_code=401)

auth_header={'Authorization': 'Bearer Xxxxxxxxxxx'}



def test_get_crons():
    # Authenticated Request 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.get_crons=AsyncMock(return_value=[]) 
    resp=client.get('/v1/crons', headers=auth_header)
    assert resp.status_code == 200
    assert resp.json() == []

    # Unauthenticated Request
    app.dependency_overrides[get_current_user] =  unauth_user
    resp=client.get('/v1/crons')
    assert resp.status_code == 401

    # Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)


def test_get_cron():
    # Authenticated Request 
    app.dependency_overrides[get_current_user] = auth_user
    response_data={
     "id": "642c2d7ea0209c97a399b860","url": "https://example.com","method": "get",
    "headers": {"Authorization": "Bearer xxxxxxx" },
    "body": None, "schedule": {"notify_on_error": False,
    "years": 0,"month": 0, "weekday": "MO", "days": 0, "hours": 9, "minutes": 0,
    "timezone": "Africa/Lagos","date_created": "2023-04-04T14:00:30.681282",
    "next_execution": "2023-04-10T09:00:00+01:00" }
    }
    Cron.get_cron= AsyncMock(return_value=response_data)
    resp=client.get('/v1/cron/642c2d7ea0209c97a399b860', headers=auth_header)
    assert resp.status_code == 200
    assert resp.json() == cron_data

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.get('/v1/cron/642c2d7ea0209c97a399b860')
    assert resp.status_code == 401
    
    # Invalid Cron Id
    app.dependency_overrides[get_current_user] = auth_user
    Cron.get_cron= MagicMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.get('/api/v1/cron/642c2d7ea0209c97a399b899')
    assert resp.status_code == 404

    # Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)


def test_update_cron():
    # Authenticated Request 
    app.dependency_overrides[get_current_user] = auth_user
    response_data={
    "id": "642c2d7ea0209c97a399b860", "url":"https://example2.com","method": "get",
    "headers": { "Authorization": "Bearer xxxxxxx" }, "body": None,"schedule": {
    "notify_on_error": False,"years": 0,"month": 0,
    "weekday": "TUE","days": 0,"hours": 9,"minutes": 0,"timezone":"Africa/Lagos","date_created":"2023-04-04T14:00:30.681282","next_execution": "2023-04-10T09:00:00+01:00" }
    }
    Cron.update_cron= MagicMock(return_value=response_data)
    update_json={
     "url": "https://example2.com", "method": "get",
     "headers": {"Authorization": "Bearer xxxxxxx"},
     "timezone":"Africa/Lagos", "weekday":"TUE", "hours":9,"minutes":0,"notify_on_error": False
     }    
    resp= client.put('/v1/update-cron/642c2d7ea0209c97a399b860', headers=auth_header, json=update_json)
    assert resp.status_code == 200
    assert resp.json() == cron_data 

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.put('/v1/update-cron/642c2d7ea0209c97a399b860', json=update_json)
    assert resp.status_code == 401
   
    # invalid Cron ID 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.update_cron = MagicMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.put('/v1/update-cron/642c2d7ea0209c97a399b756', headers=auth_header, json=json)
    assert resp.status_code == 404
    
    # Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)


def test_delete_cron():
    #Authenticated Request
    app.dependency_overrides[get_current_user] = auth_user
    Cron.delete_cron=MagicMock(return_value=True) 
    resp=client.delete('/v1/delete-cron/642c2d7ea0209c97a399b860', headers=auth_header)
    assert resp.status_code == 204

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.delete('/v1/delete-cron/642c2d7ea0209c97a399b860')
    assert resp.status_code == 401

    # invalid Cron ID 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.delete_cron = MagicMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.delete('/v1/delete-cron/642c2d7ea0209c97a399b560', headers=auth_header)
    assert resp.status_code == 404

    #  Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)

def test_get_cron_response_history():
    pass

def test_delete_cron_response_history():
    pass

def test_get_response():
   pass

def test_delete_response():
   pass
