import os
# Теперь мы импортируем из папок!
from database.db import init_db
from repositories.repositories import (
    get_all_clients, get_all_masters, get_all_services,
    get_client_appointments, get_master_appointments_for_day,
    get_user_by_login
)
from services.services import book_appointment, confirm_booking, cancel_booking


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\nНажмите Enter для продолжения...")


# ==================== МЕНЮ АДМИНИСТРАТОРА ====================
def admin_menu(user):
    while True:
        clear()
        print(f"===== ПАНЕЛЬ АДМИНИСТРАТОРА ({user['login']}) =====")
        print("1. Просмотр всех клиентов")
        print("2. Просмотр всех мастеров")
        print("3. Просмотр прайс-листа услуг")
        print("4. Подтвердить запись")
        print("5. Отменить запись")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            clear()
            print("👥 Список клиентов:")
            for c in get_all_clients():
                print(f"  [{c.client_id}] {c.full_name} — {c.phone}")
            pause()
        elif choice == "2":
            clear()
            print("💇 Список мастеров:")
            for m in get_all_masters():
                print(f"  [{m.master_id}] {m.full_name} ({m.specialization})")
            pause()
        elif choice == "3":
            clear()
            print("💅 Прайс-лист:")
            for s in get_all_services():
                print(f"  [{s.service_id}] {s.name} — {s.price}₽ ({s.duration_min} мин)")
            pause()
        elif choice == "4":
            try:
                app_id = int(input("Введите ID записи для подтверждения: "))
                confirm_booking(app_id)
                print("✅ Запись успешно подтверждена!")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
            pause()
        elif choice == "5":
            try:
                app_id = int(input("Введите ID записи для отмены: "))
                cancel_booking(app_id)
                print("✅ Запись успешно отменена!")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
            pause()
        elif choice == "0":
            break


# ==================== МЕНЮ КЛИЕНТА ====================
def client_menu(user):
   
    client_id = user['user_id']

    while True:
        clear()
        print(f"===== ЛИЧНЫЙ КАБИНЕТ КЛИЕНТА ({user['login']}) =====")
        print("1. Мои активные записи")
        print("2. Записаться на услугу")
        print("3. Отменить запись")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            clear()
            print("📅 Ваши записи:")
            apps = get_client_appointments(client_id)
            if not apps:
                print("  У вас пока нет записей.")
            for a in apps:
                print(f"  ID: {a.appointment_id} | {a.start_time} — {a.service_name} у {a.master_name} [{a.status}]")
            pause()
        elif choice == "2":
            clear()
            print("Доступные мастера:")
            for m in get_all_masters(): print(f"  [{m.master_id}] {m.full_name}")
            print("\nДоступные услуги:")
            for s in get_all_services(): print(f"  [{s.service_id}] {s.name}")

            try:
                master_id = int(input("\nID мастера: "))
                service_id = int(input("ID услуги: "))
                date = input("Дата (ГГГГ-ММ-ДД): ")
                time = input("Время (ЧЧ:ММ): ")

                new_id = book_appointment(client_id, master_id, service_id, date, time)
                print(f"✅ Вы записаны! Номер записи: {new_id}")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
            pause()
        elif choice == "3":
            try:
                app_id = int(input("Введите ID записи для отмены: "))
                cancel_booking(app_id)
                print("✅ Запись отменена!")
            except Exception as e:
                print(f"❌ Ошибка: {e}")
            pause()
        elif choice == "0":
            break


# ==================== МЕНЮ МАСТЕРА ====================
def master_menu(user):
    master_id = user['user_id']

    while True:
        clear()
        print(f"===== КАБИНЕТ МАСТЕРА ({user['login']}) =====")
        print("1. Мое расписание на день")
        print("0. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            date = input("Введите дату (ГГГГ-ММ-ДД): ")
            clear()
            print(f"📅 Ваши записи на {date}:")
            apps = get_master_appointments_for_day(master_id, date)
            if not apps:
                print("  На этот день записей нет.")
            for a in apps:
                print(f"  {a.start_time[11:16]} — {a.service_name} [{a.status}]")
            pause()
        elif choice == "0":
            break


# ==================== АВТОРИЗАЦИЯ И ГЛАВНОЕ МЕНЮ ====================
def login():
    clear()
    print("===== ВХОД В СИСТЕМУ =====")
    login_val = input("Логин: ")
    input("Пароль: ") 

    # Ищем пользователя в базе
    user = get_user_by_login(login_val)

    if not user:
        print("❌ Пользователь не найден!")
        pause()
        return None

    print(f"✅ Успешный вход! Ваша роль: {user['role']}")
    pause()
    return user


def main():
    init_db()

    while True:
        user = login()
        if user:
            if user['role'] == 'admin':
                admin_menu(user)
            elif user['role'] == 'master':
                master_menu(user)
            elif user['role'] == 'client':
                client_menu(user)
        else:
            break


if __name__ == "__main__":
    main()
