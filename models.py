from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: int
    login: str
    password_hash: str
    role: str
    created_at: str


@dataclass
class Client:
    client_id: int
    user_id: Optional[int]
    full_name: str
    phone: str
    email: Optional[str]
    birth_date: Optional[str]
    notes: Optional[str]


@dataclass
class Master:
    master_id: int
    user_id: Optional[int]
    full_name: str
    specialization: str
    phone: Optional[str]
    hire_date: Optional[str]
    is_active: bool


@dataclass
class Service:
    service_id: int
    name: str
    category: str
    price: float
    duration_min: int
    description: Optional[str]


@dataclass
class Schedule:
    schedule_id: int
    master_id: int
    work_date: str
    start_time: str
    end_time: str


@dataclass
class Appointment:
    appointment_id: int
    client_id: int
    master_id: int
    service_id: int
    start_time: str
    end_time: str
    status: str
    created_at: str

    # Дополнительные поля для удобного вывода (из JOIN-запросов)
    service_name: Optional[str] = None
    master_name: Optional[str] = None