import paramiko
import getpass
import logging

# Определение формата вывода в основной лог
logging.basicConfig(filename='log_file.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Определение формата вывода в лог ошибок
error_logging = logging.getLogger('error_logger')
error_logging.setLevel(logging.ERROR)
error_log_handler = logging.FileHandler('errorlog.log')
error_log_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
error_logging.addHandler(error_log_handler)

# Чтение списка удаленных серверов из файла
with open('server_list.txt', 'r') as file:
    list_hosts = [line.strip() for line in file.readlines()]

# Остальной код остается без изменений...
# ... (оставьте все, что было после чтения списка серверов)

# Функция для выполнения команд на удаленном сервере
def execute_command(server, command):
    try:
        # Тот же код функции, что и ранее...
    except Exception as e:
        # Запись о неудачном подключении в отдельный файл лога ошибок
        error_message = f"Failed to connect to {server['host']}: {str(e)}"
        print(error_message)
        error_logging.error(error_message)


