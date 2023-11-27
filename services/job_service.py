from fastapi import Depends
import random
import abc

from schemas.job_schema import TaskSchema, IssueSchema, BugSchema
from services.trello_service import TrelloService
from utils.randomizers import generate_random_number, generate_random_word

class JobService(abc.ABC):
    
    @abc.abstractmethod
    def create(cls):
        pass
    
class TaskService(JobService):
    
    @classmethod
    def create(cls,task:TaskSchema, trello_service: TrelloService):
        task_dict = {
        "name": task.title,
        "idList": trello_service.list_id,
        "idLabels": [trello_service.get_or_create_label(task.category)]
        }
        return trello_service.create_card(task_dict)


class IssueService(JobService):
    
    @classmethod
    def create(cls,issue:IssueSchema, trello_service: TrelloService):
        issue_dict = {
            "name": issue.title,
            "desc": issue.description,
            "idList": trello_service.list_id,
        }
        return trello_service.create_card(issue_dict)
    
class BugService(JobService):
    
    @classmethod
    def create(cls,bug:BugSchema, trello_service: TrelloService):
        #this might be a configuration parameter, but for this porpose we will leave it like this
        id = f'bug-{generate_random_word(5)}-{generate_random_number(10000,99999)}'
        bug_dict = {
            "name": id,
            "desc": bug.description,
            "idList": trello_service.list_id,
            "idMembers": [random.choice(trello_service.get_board_valid_members(trello_service.board_id))],
            "idLabels": [trello_service.get_or_create_label(bug.category)]
        }
        return trello_service.create_card(bug_dict)
