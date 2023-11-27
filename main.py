from fastapi import FastAPI, HTTPException, Response, status
from dotenv import load_dotenv
from pydantic import ValidationError
import os


from services.trello_service import TrelloService
from schemas.job_schema import TaskSchema, IssueSchema, BugSchema, JobTypeEnum
from services.job_service import TaskService, IssueService, BugService


app = FastAPI()

env = load_dotenv()
if not env:
    raise Exception("Cannot load the .env file")


api_key = os.environ.get("TRELLO_API_KEY")
token = os.environ.get("TRELLO_TOKEN")
trello_board_id = os.environ.get("TRELLO_BOARD_ID")
list_name = os.environ.get("TRELLO_LIST_NAME")

trello_service = TrelloService.get_or_create(api_key=api_key, token=token, trello_board_id=trello_board_id, list_name=list_name)

@app.post("/")
def read_root(payload: dict, response:Response):
        job_selector = {
            JobTypeEnum.task: (TaskSchema,TaskService),
            JobTypeEnum.issue: (IssueSchema,IssueService),
            JobTypeEnum.bug: (BugSchema,BugService),
        }
        try:
            class_validator,service = job_selector[payload.get('type')]
        except:
            raise HTTPException(400, "Invalid job type, valid types are: task, issue, bug")
        try:
            job = class_validator(**payload)
            response.status_code = status.HTTP_201_CREATED
            return service.create(job, trello_service)
            
             
        except KeyError:
            raise  HTTPException(500,"There was an error on the server side")
        except ValidationError as e:
            raise HTTPException(400, e.errors())

    
