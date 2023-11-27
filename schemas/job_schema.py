import pydantic
from enum import Enum

class JobTypeEnum(str, Enum):
    issue = "issue"
    bug = "bug"
    task = "task"

class CategoryEnum(str, Enum):
    maintenance = "Maintenance"
    research = "Research"
    test= "Test"

class JobSchema(pydantic.BaseModel):
    type: JobTypeEnum

class IssueSchema(JobSchema):
    type: JobTypeEnum = JobTypeEnum.issue
    title: str
    description: str

class BugSchema(JobSchema):
    type: JobTypeEnum = JobTypeEnum.bug
    description: str
    category : str = "Bug"

class TaskSchema(JobSchema):
    type: JobTypeEnum = JobTypeEnum.task
    title: str
    category: CategoryEnum

