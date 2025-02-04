import socket
import threading
import sys
import os
import time
from config import ip, name

messages = ""

def clear_screen():
    # Определяем функцию для очистки экрана
    os.system('cls' if os.name == 'nt' else 'clear')

def receive_messages(client_socket):
    global messages
    while True:
        try:
            message = client_socket.recv(2048).decode()
            if message:  # если получили сообщение
                messages += message + "\n"  # добавляем к общим сообщениям
        except Exception as e:
            print("Ошибка при получении сообщения:", e)
            break

def connector():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, 65432))
    
    client_socket.sendall(name.encode())

    # Запускаем поток для получения сообщений
    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.daemon = True  # делает поток фоновым
    thread.start()

    try:
        while True:
            clear_screen()
            print(messages)  # выводим все сообщения
            time.sleep(1)

    except KeyboardInterrupt:
        print("Выход из клиента...")
    finally:
        client_socket.close()

def send_message(message):
    global messages
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, 65432))
            s.sendall(message.encode('utf-8'))
            msg = s.recv(1024).decode('utf-8')  # Получаем ответ от сервера, если требуется
            messages += msg + '\n'  # Обновляем переменную messages
    except Exception as e:
        messages += f"Ошибка при отправке сообщения: {str(e)}\n"

if __name__ == "__main__":
    connector()