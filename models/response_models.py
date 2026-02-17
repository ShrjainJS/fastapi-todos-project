from pydantic import BaseModel, Field, ConfigDict

# Create a response model for API Response for Tasks
class TodoReturn(BaseModel):
    id: int = Field(description='Task ID')
    title: str = Field(description='Task title')
    description: str = Field(description='Task description')
    priority: int = Field(description='Task priority')
    complete: bool = Field(description='Is task completed?')

    # To use with SQLAlchemy 2.0 Objects
    # This configuration allows for pydantic to identify ORM 'object' and convert it into standard python dict which pydantic and fast API expects.
    model_config = ConfigDict(from_attributes=True)

class UserReturn(BaseModel):
    id: int = Field(description='Returned User ID')
    username: str = Field(description='Returned username')
    email: str = Field(description='Returned username')
    first_name: str = Field(description='Retuned first name')
    last_name: str = Field(description='Retuned last name')
    hashed_password: str = Field(description='password hashed')
    is_active: bool = Field(description='Is user active?')
    role: str = Field(description='Retuned user role')

    model_config = ConfigDict(from_attributes=True)