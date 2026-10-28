from database.db import get_connection
from models.models import Client, Master, Service, Appointment


# ==================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ПРЕОБРАЗОВАНИЯ ====================
def _map_client(row) -> Client:
    return Client(
        row['client_id'], row['user_id'], row['full_name'],
        row['phone'], row['email'], row['birth_date'], row['notes']
    )


def _map_master(row) -> Master:
    return Master(
        row['master_id'], row['user_id'], row['full_name'],
        row['specialization'], row['phone'], row['hire_date'], bool(row['is_active'])
    )


def _map_service(row) -> Service:
    return Service(
        row['service_id'], row['name'], row['category'],
        row['price'], row['duration_min'], row['description']
    )


def _map_appointment(row) -> Appointment:
    # Безопасно проверяем наличие дополнительных полей из JOIN-запросов
    service_name = row['service_name'] if 'service_name' in row.keys() else None
    master_name = row['master_name'] if 'master_name' in row.keys() else None

    return Appointment(
        row['appointment_id'], row['client_id'], row['master_id'], row['service_id'],
        row['start_time'], row['end_time'], row['status'], row['created_at'],
        service_name, master_name
    )


# ==================== 1. USERS (ПОЛЬЗОВАТЕЛИ) ====================
def get_all_users():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM users").fetchall()


def get_user_by_login(login: str):
    """Ищет пользователя по логину для авторизации."""
    with get_connection() as conn:
        return conn.execute("SELECT * FROM users WHERE login = ?", (login,)).fetchone()


# ==================== 2. CLIENTS (КЛИЕНТЫ) ====================
def get_all_clients() -> list[Client]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM clients ORDER BY full_name").fetchall()
        return [_map_client(r) for r in rows]


def get_client_by_id(client_id: int) -> Client | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM clients WHERE client_id = ?", (client_id,)).fetchone()
        return _map_client(row) if row else None


# ==================== 3. MASTERS (МАСТЕРА) ====================
def get_all_masters(only_active: bool = True) -> list[Master]:
    with get_connection() as conn:
        sql = "SELECT * FROM masters"
        if only_active:
            sql += " WHERE is_active = 1"
        rows = conn.execute(sql).fetchall()
        return [_map_master(r) for r in rows]


def get_master_by_id(master_id: int) -> Master | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM masters WHERE master_id = ?", (master_id,)).fetchone()
        return _map_master(row) if row else None


# ==================== 4. SERVICES (УСЛУГИ) ====================
def get_all_services() -> list[Service]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM services ORDER BY category, name").fetchall()
        return [_map_service(r) for r in rows]


def get_service_by_id(service_id: int) -> Service | None:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM services WHERE service_id = ?", (service_id,)).fetchone()
        return _map_service(row) if row else None


# ==================== 5. MASTER_SERVICES (СВЯЗЬ) ====================
def get_all_master_services():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM master_services").fetchall()


# ==================== 6. SCHEDULES (РАСПИСАНИЕ) ====================
def get_all_schedules():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM schedules").fetchall()


def get_master_schedule_for_day(master_id: int, date: str):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM schedules WHERE master_id = ? AND work_date = ?",
            (master_id, date)
        ).fetchall()


# ==================== 7. APPOINTMENTS (ЗАПИСИ) ====================
def create_appointment(client_id: int, master_id: int, service_id: int, start_time: str, end_time: str,
                       status: str = 'pending') -> int:
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO appointments (client_id, master_id, service_id, start_time, end_time, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (client_id, master_id, service_id, start_time, end_time, status)
        )
        return cur.lastrowid


def update_appointment_status(appointment_id: int, status: str):
    with get_connection() as conn:
        conn.execute("UPDATE appointments SET status = ? WHERE appointment_id = ?", (status, appointment_id))


def get_client_appointments(client_id: int) -> list[Appointment]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT a.*, s.name AS service_name, m.full_name AS master_name
            FROM appointments a
            JOIN services s ON s.service_id = a.service_id
            JOIN masters  m ON m.master_id  = a.master_id
            WHERE a.client_id = ?
            ORDER BY a.start_time DESC
        """, (client_id,)).fetchall()
        return [_map_appointment(r) for r in rows]


def get_master_appointments_for_day(master_id: int, date: str) -> list[Appointment]:
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT a.*, s.name AS service_name, c.full_name AS client_name
            FROM appointments a
            JOIN services s ON s.service_id = a.service_id
            JOIN clients  c ON c.client_id  = a.client_id
            WHERE a.master_id = ? AND date(a.start_time) = ?
            ORDER BY a.start_time
        """, (master_id, date)).fetchall()

        res = []
        for r in rows:
            app = _map_appointment(r)
            # Добавляем имя клиента динамически для меню мастера
            app.client_name = r['client_name']
            res.append(app)
        return res