# Импорт теперь из папки repositories
from repositories.repositories import (
    get_client_by_id, get_master_by_id, get_service_by_id,
    get_master_appointments_for_day, create_appointment,
    update_appointment_status
)
import datetime

# ... остальной ваш код (book_appointment, confirm_booking и т.д.) ...


def book_appointment(client_id: int, master_id: int, service_id: int, date: str, start_time: str):
    """
    Сервис бронирования записи (аналог create_reservation из методички).
    Выполняет проверки существования объектов и бизнес-правил.
    """
    # 1. Проверка: существует ли клиент?
    client = get_client_by_id(client_id)
    if not client:
        raise Exception("Клиент с таким ID не найден")

    # 2. Проверка: существует ли мастер и активен ли он?
    master = get_master_by_id(master_id)
    if not master or not master.is_active:
        raise Exception("Мастер не найден или временно не работает")

    # 3. Проверка: существует ли услуга?
    service = get_service_by_id(service_id)
    if not service:
        raise Exception("Услуга не найдена")

    # 4. Проверка на накладку по времени (бизнес-правило)
    # Формируем полную дату-время начала
    full_start_time = f"{date} {start_time}"

    existing_appointments = get_master_appointments_for_day(master_id, date)
    for app in existing_appointments:
        if app.start_time == full_start_time and app.status in ('pending', 'confirmed'):
            raise Exception(f"У мастера {master.full_name} уже есть запись на {full_start_time}")

    # 5. Если все проверки пройдены — создаем запись
    # Вычисляем время окончания (упрощенно, прибавляем duration_min)
    # В идеале нужно использовать datetime, но для лабы можно пропустить или сделать простую логику
    end_time = "TODO: Вычислить end_time"

    # Для простоты пока передадим заглушку end_time, либо реализуйте логику сложения времени
    import datetime
    start_dt = datetime.datetime.strptime(full_start_time, "%Y-%m-%d %H:%M")
    end_dt = start_dt + datetime.timedelta(minutes=service.duration_min)
    end_time_str = end_dt.strftime("%Y-%m-%d %H:%M")

    new_id = create_appointment(client_id, master_id, service_id, full_start_time, end_time_str)
    return new_id, master.full_name, service.name


def confirm_booking(appointment_id: int):
    """Подтверждение записи администратором."""
    update_appointment_status(appointment_id, 'confirmed')
    return True


def cancel_booking(appointment_id: int):
    """Отмена записи."""
    update_appointment_status(appointment_id, 'cancelled')
    return True