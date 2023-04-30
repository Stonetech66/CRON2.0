from fastapi.testclient import TestClient
from fastapi import HTTPException, Header
from ..main import app
from unittest.mock import MagicMock, patch, AsyncMock
from CRON2.dependencies import get_current_user 
from .crud import Cron
from bson.objectid import ObjectId 
from datetime import datetime 
client = TestClient(app)

async def auth_user(Bearer=Header(default=None)):
 return {'_id' : ObjectId('642c2d7ea0209c97a399b869'), 'email': 'cron@gmail.com', 'fullname': 'cronn job'}

async def unauth_user(Bearer=Header(default=None)):
  raise HTTPException(detail='invalid token or token has expired', status_code=401)

auth_header={'Authorization': 'Bearer Xxxxxxxxxxx'}


def test_create_cron_valid_data():
    # Authenticated Request 
    app.dependency_overrides[get_current_user] = auth_user
    response_data={
    "_id": ObjectId("642c2d7ea0209c97a399b860"), "message":"cron Job created successfully","next_execution": "2023-04-10T09:00:00+01:00" }
    Cron.create_cron= AsyncMock(return_value=response_data)
    create_json={
     "url": "https://example.com", "method": "get",
     "headers": {"Authorization": "Bearer xxxxxxx"},
     "timezone":"Africa/Lagos", "weekday":"MON", "hours":9,"minutes":0,"notify_on_error": False
     }    
    resp= client.post('/v1/cron-jobs', headers=auth_header, json=create_json)
    assert resp.status_code == 201
    response_data["_id"] = str(response_data["_id"])
    assert resp.json() == response_data

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.post('/v1/cron-jobs', json=create_json)
    assert resp.status_code == 401
   
    # Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)



def test_get_crons():
    # Authenticated Request 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.get_crons=AsyncMock(return_value=[]) 
    resp=client.get('/v1/cron-jobs', headers=auth_header)
    assert resp.status_code == 200
    assert resp.json() == []

    # Unauthenticated Request
    app.dependency_overrides[get_current_user] =  unauth_user
    resp=client.get('/v1/cron-jobs')
    assert resp.status_code == 401

    # Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)


def test_get_cron():
    # Authenticated Request 
    app.dependency_overrides[get_current_user] = auth_user
    response_data={
     "_id": ObjectId("642c2d7ea0209c97a399b860"),"url": "https://example.com","method": "get",
    "headers": {"Authorization": "Bearer xxxxxxx" },
    "body": None, "schedule": {"notify_on_error": False,
    "years": 0,"month": 0, "weekday": "MO", "days": 0, "hours": 9, "minutes": 0,
    "timezone": "Africa/Lagos","date_created": "2023-04-04T14:00:30.681282",
    "next_execution": "2023-04-10T09:00:00+01:00" }
    }
    Cron.get_cron= AsyncMock(return_value=response_data)
    resp=client.get('/v1/cron-jobs/642c2d7ea0209c97a399b860', headers=auth_header)
    assert resp.status_code == 200
    response_data["_id"] = str(response_data["_id"])
    assert resp.json() == response_data

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.get('/v1/cron-jobs/642c2d7ea0209c97a399b860')
    assert resp.status_code == 401
    
    # Invalid Cron Id
    app.dependency_overrides[get_current_user] = auth_user
    Cron.get_cron= AsyncMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.get('/v1/cron-jobs/642c2d7ea0209c97a399b899')
    assert resp.status_code == 404

    # Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)


def test_update_cron():
    # Authenticated Request 
    app.dependency_overrides[get_current_user] = auth_user
    response_data={
    "_id": ObjectId("642c2d7ea0209c97a399b860"), "url":"https://example2.com","method": "get",
    "headers": { "Authorization": "Bearer xxxxxxx" }, "body": None,"schedule": {
    "notify_on_error": False,"years": 0,"month": 0,
    "weekday": "TUE","days": 0,"hours": 9,"minutes": 0,"timezone":"Africa/Lagos","date_created":"2023-04-04T14:00:30.681282","next_execution": "2023-04-10T09:00:00+01:00" }
    }
    Cron.update_cron= AsyncMock(return_value=response_data)
    update_json={
     "url": "https://example2.com", "method": "get",
     "headers": {"Authorization": "Bearer xxxxxxx"},
     "timezone":"Africa/Lagos", "weekday":"TUE", "hours":9,"minutes":0,"notify_on_error": False
     }    
    resp= client.put('/v1/cron-jobs/642c2d7ea0209c97a399b860', headers=auth_header, json=update_json)
    assert resp.status_code == 200
    response_data["_id"] = str(response_data["_id"])
    assert resp.json() == response_data

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.put('/v1/cron-jobs/642c2d7ea0209c97a399b860', json=update_json)
    assert resp.status_code == 401
   
    # invalid Cron ID 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.update_cron = AsyncMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.put('/v1/cron-jobs/642c2d7ea0209c97a399b756', headers=auth_header, json=update_json)
    assert resp.status_code == 404
    
    # Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)


def test_delete_cron():
    #Authenticated Request
    app.dependency_overrides[get_current_user] = auth_user
    Cron.delete_cron=AsyncMock(return_value=True) 
    resp=client.delete('/v1/cron-jobs/642c2d7ea0209c97a399b860', headers=auth_header)
    assert resp.status_code == 204

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.delete('/v1/cron-jobs/642c2d7ea0209c97a399b860')
    assert resp.status_code == 401

    # invalid Cron ID 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.delete_cron = AsyncMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.delete('/v1/cron-jobs/642c2d7ea0209c97a399b560', headers=auth_header)
    assert resp.status_code == 404

    #  Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)

def test_get_cron_response_history():
    #Authenticated Request
    app.dependency_overrides[get_current_user] = auth_user
    Cron.get_response_history=AsyncMock(return_value=[])
    Cron.get_cron= AsyncMock(return_value={})
    resp=client.get('/v1/response/history/642c2d7ea0209c97a399b860', headers=auth_header)
    assert resp.status_code == 200

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.get('/v1/response/history/642c2d7ea0209c97a399b860')
    assert resp.status_code == 401

    # invalid Cron ID 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.get_cron= AsyncMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID')) 
    resp=client.get('/v1/response/history/642c2d7ea0209c97a399b880', headers=auth_header)
    assert resp.status_code == 404

    #  Revert the dependency changes
    app.dependency_overrides.pop(get_current_user)
 

def test_clear_cron_response_history():
    #Authenticated Request
    app.dependency_overrides[get_current_user] = auth_user
    Cron.clear_response_history=AsyncMock(return_value=True) 
    Cron.get_cron= AsyncMock(return_value=[])
    resp=client.delete('/v1/response/history/642c2d7ea0209c97a399b860', headers=auth_header)
    assert resp.status_code == 204

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.delete('/v1/response/history/642c2d7ea0209c97a399b860')
    assert resp.status_code == 401

    # invalid Cron ID 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.get_cron = AsyncMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.delete('/v1/response/history/642c2d7ea0209c97a399b880', headers=auth_header)
    assert resp.status_code == 404

 

def test_get_response():
    #Authenticated Request
    app.dependency_overrides[get_current_user] = auth_user   
    response_data={
    "_id" :ObjectId("642c2d7ea0578c97a566b790"), 
    "status":200 , "timestamp":datetime.utcnow(), "cron_id":"642c2d7ea0209c97a399b860", "url" :"http://example.com"} 
    Cron.get_response=AsyncMock(return_value=response_data) 
    resp=client.get('/v1/response/642c2d7ea0578c97a566b790', headers=auth_header)
    assert resp.status_code == 200
    response_data["_id"] = str(response_data["_id"])
    response_data["timestamp"] = response_data["timestamp"].strftime('%Y-%m-%dT%H:%M:%S.%f')
    assert resp.json() == response_data

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.get('/v1/response/642c2d7ea0578c97a566b790')
    assert resp.status_code == 401

    # invalid Response ID 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.get_response = AsyncMock(side_effect=HTTPException(status_code=404, detail='invalid Response ID'))
    resp=client.get('/v1/response/642c2d7ea0578c97a566b789', headers=auth_header)
    assert resp.status_code == 404

 

def test_delete_response():
    #Authenticated Request
    app.dependency_overrides[get_current_user] = auth_user
    Cron.delete_response=AsyncMock(return_value=True) 
    resp=client.delete('/v1/response/642c2d7ea0578c97a566b790', headers=auth_header)
    assert resp.status_code == 204

    # Unauthenticated Request 
    app.dependency_overrides[get_current_user] = unauth_user
    resp=client.delete('/v1/response/642c2d7ea0578c97a566b790')
    assert resp.status_code == 401

    # invalid Response ID 
    app.dependency_overrides[get_current_user] = auth_user
    Cron.delete_response = AsyncMock(side_effect=HTTPException(status_code=404, detail='invalid Cron ID'))
    resp=client.delete('/v1/response/642c2d7ea0578c67b566b790', headers=auth_header)
    assert resp.status_code == 404

  
