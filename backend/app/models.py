from datetime import datetime
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)
    role: str = "owner"          # owner, staff, admin
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # relationships
    policies: List["Policy"] = Relationship(back_populates="owner")
    tasks:    List["Task"]   = Relationship(back_populates="assignee")


class Policy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    title: str
    file_path: str                   # S3/MinIO key
    created_at: datetime = Field(default_factory=datetime.utcnow)

    owner: "User"              = Relationship(back_populates="policies")
    gaps:  List["Gap"]         = Relationship(back_populates="policy")


class Gap(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    policy_id: int = Field(foreign_key="policy.id")
    description: str
    severity: str               # low / medium / high
    created_at: datetime = Field(default_factory=datetime.utcnow)

    policy: "Policy"            = Relationship(back_populates="gaps")
    tasks:  List["Task"]        = Relationship(back_populates="gap")


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    gap_id: int = Field(foreign_key="gap.id")
    assigned_to: Optional[int] = Field(default=None, foreign_key="user.id")
    title: str
    due_date: Optional[datetime] = None
    status: str = "open"        # open / in_progress / done
    created_at: datetime = Field(default_factory=datetime.utcnow)

    gap: "Gap"                  = Relationship(back_populates="tasks")
    assignee: Optional["User"]  = Relationship(back_populates="tasks")
    evidence: List["Evidence"]  = Relationship(back_populates="task")


class Evidence(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    file_path: str                   # S3/MinIO key
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    task: "Task"              = Relationship(back_populates="evidence")
