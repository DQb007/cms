from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class LoginRequest(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)


class ChangePasswordRequest(BaseModel):
    old_password: str = Field(min_length=1, max_length=255)
    new_password: str = Field(min_length=6, max_length=255)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


class UserProfile(BaseModel):
    id: int
    username: str | None

    model_config = ConfigDict(from_attributes=True)


class CourseBase(BaseModel):
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=255)
    url: HttpUrl | str | None = None
    price: int = Field(ge=0)
    category: str | None = Field(default=None, max_length=255)


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class CourseOut(BaseModel):
    id: int
    code: str
    name: str
    url: str | None
    price: int
    category: str | None
    create_time: datetime | None
    creator: str | None
    modify_time: datetime | None
    modifier: str | None

    model_config = ConfigDict(from_attributes=True)


class CourseListResponse(BaseModel):
    items: list[CourseOut]
    total: int
    page: int
    page_size: int


class CourseBatchDeleteRequest(BaseModel):
    ids: list[int] = Field(min_length=1, max_length=100)


class CourseBatchDeleteResponse(BaseModel):
    deleted: int


class CategoryResponse(BaseModel):
    categories: list[str]
