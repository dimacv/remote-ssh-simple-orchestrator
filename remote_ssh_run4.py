import paramiko
import getpass
import logging
import datetime

# Получение текущей даты и времени
current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# Определение формата вывода в основной лог
log_file_name = f'log_file_{current_datetime}.log'
logging.basicConfig(filename=log_file_name, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Определение формата вывода в лог ошибок
error_log_file_name = f'errorlog_{current_datetime}.log'
error_logging = logging.getLogger('error_logger')
error_logging.setLevel(logging.ERROR)
error_log_handler = logging.FileHandler(error_log_file_name)
error_log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
error_logging.addHandler(error_log_handler)

# Чтение списка удаленных серверов из файла
list_hosts = []
with open('server_list.txt', 'r') as file:
    for line in file:
        server_info, comment = line.strip().split('#', 1)
        server_info = server_info.strip()
        if server_info:
            list_hosts.append({'info': server_info, 'comment': comment.strip()})

# Остальной код остается без изменений...
# ... (оставьте все, что было после чтения списка серверов)

# Функция для выполнения команд на удаленном сервере
def execute_command(server, command):
    try:
        # Тот же код функции, что и ранее...
    except Exception as e:
        # Запись о неудачном подключении в отдельный файл лога ошибок
        error_message = f"Failed to connect to {server['info']}: {str(e)}"
        print(error_message)
        error_logging.error(error_message)

# Остальной код остается без изменений...
# ... (оставьте все, что было после функции execute_command)
