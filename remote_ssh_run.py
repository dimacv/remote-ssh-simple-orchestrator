import paramiko
import getpass
import logging
import datetime

# Список команд, которые необходимо выполнить
commands = [ 'uname -a'
    #'mount /nfs_shares/backup_os',
    #'/nfs_shares/backup_os/scripts/add_scan_unix.sh',
    #'lsuser scan_unix'
]


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
        server_info, *comment = line.strip().split('#', 1)
        server_info = server_info.strip()
        comment = comment[0].strip() if comment else ""
        if server_info:
            list_hosts.append({'info': server_info, 'comment': comment})


# Функция для выполнения команд на удаленном сервере
def execute_command(server, command):
    try:
        print(f"\n------------------------------------------------------------------")
        print(f"          On HOST     -   {server['host']['info']} {server['host']['comment']}")
        print(f"          Result of executed command   -   {command}\n")
        logging.info("\n------------------------------------------------------------------")
        logging.info(f"          On HOST    -   {server['host']['info']} {server['host']['comment']}")

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключение к серверу
        client.connect(
            server['host']['info'],
            username=server['username'],
            key_filename=server['key_path'],
            passphrase=ssh_key_passphrase,
            timeout=10
        )

        # Выполнение команды
        stdin, stdout, stderr = client.exec_command(command)

        logging.info(f"          Result of executed command   -   {command}\n")

        # Вывод результата
        for line in stdout:
            print(line.strip('\n'))
            logging.info(line.strip('\n'))

        logging.info("\n------------------------------------------------------------------")

        # Закрытие подключения к серверу
        client.close()
    except Exception as e:
        # Запись о неудачном подключении в отдельный файл лога ошибок
        error_message = f"     {server['host']['info']} {server['host']['comment']} - Failed connect. Error : {str(e)}"
        print(error_message)
        error_logging.error(error_message)


ssh_key_passphrase = getpass.getpass("Введите пароль для ssh ключа: ")


# Перебираем все сервера и выполняем на них команды
#for server in list_hosts:
for host in list_hosts:
    server = {'host': host, 'username': 'root', 'key_path': 'cv_p_OpenSSH-formatNEW_PS.ppk'}

    for command in commands:
        execute_command(server, command)
