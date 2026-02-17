from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    username: str = Field(description='Provide a Username', min_length=3)
    email: str = Field(description='Provide a valid EmailID', min_length=3)
    first_name: str = Field(description='Provide a first name')
    last_name: str = Field(description='Provide a last name')
    password: str = Field(description='Provide a password', min_length=8)
    role: str | None = Field(description='type of user', default = None)

class UpdateUserRequest(BaseModel):
    username: str = Field(description='Provide a Username', min_length=3)
    email: str = Field(description='Provide a valid EmailID', min_length=3)
    first_name: str = Field(description='Provide a first name')
    last_name: str = Field(description='Provide a last name')
    is_active: bool = Field(description='is the user still active?')
    role: str | None = Field(description='type of user', default = None)

class UpdatePasswordRequest(BaseModel):
    password: str = Field(description='Old Password to change', min_length=8)
    new_password: str = Field(description='New Password to send', min_length=8)