from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_get_crons():
    pass

def test_get_cron():
     pass

def test_update_cron():
    pass

def test_delete_cron():
   pass

def test_get_cron_response_history():
    pass

def test_delete_cron_response_history():
    pass

def test_get_response():
   pass

def test_delete_response():
   pass
