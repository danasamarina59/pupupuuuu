from db import init_db
from repositories import get_all_clients, get_all_masters, get_all_services, get_client_appointments
from services import book_appointment, confirm_booking, cancel_booking


def main_menu():
    # 1. Инициализация БД при старте
    init_db()

    # 2. Вывод справочной информации
    print("\n👥 Клиенты:")
    for c in get_all_clients():
        print(f"  [{c.client_id}] {c.full_name} — {c.phone}")

    print("\n💇 Мастера:")
    for m in get_all_masters():
        print(f"  [{m.master_id}] {m.full_name} ({m.specialization})")

    print("\n💅 Услуги:")
    for s in get_all_services():
        print(f"  [{s.service_id}] {s.name} — {s.price}₽ ({s.duration_min} мин)")

    print("\n" + "=" * 40)

    # 3. Демонстрация работы сервиса (Бронирование)
    print("Попытка создать новую запись через сервисный слой...")
    try:
        # Пытаемся записать клиента №2 к мастеру №1 на стрижку (ID 2)
        new_id, master_name, service_name = book_appointment(
            client_id=2,
            master_id=1,
            service_id=2,
            date="2025-10-13",
            start_time="14:00"
        )
        print(f"✅ Успешно создана запись #{new_id} к мастеру {master_name} на {service_name}")

        # Подтверждаем её
        confirm_booking(new_id)
        print(f"✅ Запись #{new_id} подтверждена")

    except Exception as e:
        # Обработка ошибок, которые выбрасывает сервис
        print(f"❌ Ошибка бронирования: {e}")

    # 4. Просмотр записей клиента
    print(f"\n📅 Записи клиента #2:")
    for a in get_client_appointments(2):
        print(f"  {a.start_time} — {a.service_name} у {a.master_name} [{a.status}]")


if __name__ == "__main__":
    main_menu() #zalupabobra