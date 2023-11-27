import pytest
from services.job_service import TaskService, IssueService, BugService
from services.trello_service import TrelloService
from schemas.job_schema import TaskSchema, IssueSchema, BugSchema

from unittest.mock import Mock

@pytest.fixture
def mocker():
    return Mock()

@staticmethod
def test_create_task_calls_services(mocker):


    value_mocked={
        "id": "1234asd",
        "title": "test",
        "description": "",
        "idLabels": ["Maintenance_id"],
        "shortUrl": "https://trello.com/c/1234asdQ",
        "url": "https://trello.com/c/1234asd/21-this-is-a-task",
        "idMembers": []
    }


    
    # Mock TaskSchema and TrelloService
    task_schema_mock = TaskSchema(title="test", category="Maintenance")
    trello_service_mock = Mock(spec=TrelloService)

    # Mock specific methods of TrelloService
    trello_service_mock.list_id = "test_list_id"
    trello_service_mock.get_or_create_label.return_value = "Maintenance_id"
    trello_service_mock.create_card.return_value = value_mocked

    # call the service
    created_card_id = TaskService.create(task_schema_mock, trello_service_mock)

    # verify the calls and results
    trello_service_mock.get_or_create_label.assert_called_once_with("Maintenance")
    trello_service_mock.create_card.assert_called_once_with({
        "name": "test",
        "idList": "test_list_id",
        "idLabels": ["Maintenance_id"]
    })
    assert created_card_id == value_mocked