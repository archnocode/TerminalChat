import socket
import threading
import time

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 65432))

clients_sockets = []
max_clients = 2

def handle_client(client_socket):
    while True:
        try:
            client_socket.sendall("Hello World!".encode())  # пример отправляемого сообщения
            time.sleep(1)
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")
            break
    client_socket.close()

def accept_clients():
    server_socket.listen()
    print("Ожидание подключения клиентов...")

    while True:
        if len(clients_sockets) < max_clients:
            client_socket, client_address = server_socket.accept()
            print(f"Подключен: {client_address}")
            clients_sockets.append(client_socket)
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

try:
    accept_clients()
except KeyboardInterrupt:
    print("Сервер завершен...")
finally:
    for client in clients_sockets:
        client.close()
    server_socket.close()