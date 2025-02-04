import curses
from client import messages, connector, send_message
import threading

# Фоновая нить для соединения клиента
connecting = threading.Thread(target=connector)

def main(stdscr):
    global messages  # Делаем переменную messages доступной внутри функции main
    curses.start_color()
    curses.cbreak()
    stdscr.keypad(True)

    # Запускаем фоновую нить для подключения
    connecting.start()
    
    curses.curs_set(0)
    stdscr.clear()
    
    # Начало работы с цветами (опционально)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    input_box = ''
    
    # Основной игровой цикл
    while True:
        stdscr.clear()  # Очищаем экран для обновления
        stdscr.attron(curses.color_pair(1))

        # Отображаем текущие сообщения
        stdscr.addstr(0, 0, messages)

        stdscr.attroff(curses.color_pair(1))
        stdscr.addstr(2, 0, "Введите сообщение: ")
        stdscr.addstr(2, 20, input_box + '_')  # Отображаем текущее вводимое сообщение
        
        stdscr.refresh()

        # Получаем ввод клавиш
        key = stdscr.getch()
        if key == ord('q'):
            break  # Завершить программу, если нажата клавиша 'q'
        elif key == curses.KEY_BACKSPACE or key == 127:  # Удаление символа
            input_box = input_box[:-1]
        elif key == curses.KEY_ENTER or key == 10:  # Отправляем сообщение при нажатии Enter
            if input_box:  # Проверяем, что ввод не пустой
                send_message(input_box)  # Отправляем сообщение на сервер
                input_box = ''  # Очищаем поле ввода
        else:
            input_box += chr(key)  # Добавляем символ к строке ввода

    connecting.join()  # Дождаться завершения подключения перед выходом

# Обертываем main в curses.wrapper для безопасного завершения
curses.wrapper(main)