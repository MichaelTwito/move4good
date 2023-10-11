import pytest
from backend.consts import MOCK_TOKEN, MOCK_USER, MOCK_PASSWORD,MOCK_CIVILIAN_TOKEN
from backend.mock_report_db import MockReportsDB
from backend.report import User
mock_reports = MockReportsDB()
def test_user():
    assert mock_reports.login(User(username=MOCK_USER, password='b')) == MOCK_TOKEN
def test_not_user():
    assert  mock_reports.login(User(username=MOCK_USER, password='6')) != MOCK_TOKEN

def test_admin_token():
    assert mock_reports.auth_admin(MOCK_TOKEN)

def test_civilian_token():
    assert  mock_reports.auth_user(MOCK_CIVILIAN_TOKEN)