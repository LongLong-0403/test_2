from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class ActivityCreateRequest(BaseModel):  # schema nhận dữ liệu tạo hoạt động
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    assignee_id: int | None = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: datetime | None = None

class ActivityUpdateRequest(BaseModel):  # schema nhận dữ liệu cập nhật hoạt động
    title: str | None = Field(default=None,min_length=1,max_length=200)
    description: str | None = None
    assignee_id: int | None = None
    status: str | None = None
    priority: str | None = None
    due_date: datetime | None = None


class ActivityResponse(BaseModel):  # schema trả dữ liệu hoạt động
    id: int
    club_id: int
    title: str
    description: str | None
    assignee_id: int | None
    status: str
    priority: str
    due_date: datetime | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)