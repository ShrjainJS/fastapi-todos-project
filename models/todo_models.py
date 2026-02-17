from pydantic import BaseModel, Field

class TodoRequest(BaseModel):
    title: str = Field(description='Title for the task.', min_length=3)
    description: str | None = Field(description='Description for the task.', default=None)
    priority: int = Field(description='Priority of task.', gt=0)
    complete: bool = Field(description='Is the task completed.')

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Sample Task Title",
                "description": "Lorem ipsum dolor sit amet.",
                "priority": 4,
                "complete": False
            }
        }
    }
