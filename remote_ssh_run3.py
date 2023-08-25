import paramiko
import getpass
import logging

# Определение формата вывода в лог
logging.basicConfig(filename='log_file.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Чтение списка удаленных серверов из файла
with open('server_list.txt', 'r') as file:
    list_hosts = [line.strip() for line in file.readlines()]

# Список команд, которые необходимо выполнить
commands = [
    'mount /nfs_shares/backup_os', 
    '/nfs_shares/backup_os/scripts/add_scan_unix.sh', 
    'lsuser scan_unix'
]

# Функция для выполнения команд на удаленном сервере
def execute_command(server, command):
    try:
        print('\n------------------------------------------------------------------')
        print('On HOST                    -   {}'.format(server['host']))
        print('Result of executed command   -   {} \n'.format(command))
        # вывод в лог
        logging.info('\n------------------------------------------------------------------')
        logging.info('On HOST                    -   {}'.format(server['host']))
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Подключение к серверу
        client.connect(
            server['host'],
            username=server['username'],
            key_filename=server['key_path'],
            passphrase=ssh_key_passphrase,
            timeout=10  # Добавлен таймаут для подключения
        )

        # Выполнение команды
        stdin, stdout, stderr = client.exec_command(command)

        logging.info('Result of executed command   -   {}'.format(command))

        # Вывод результата
        for line in stdout:
            print(line.strip('\n'))
            logging.info(line.strip('\n'))

        logging.info('\n------------------------------------------------------------------')

        # Закрытие подключения к серверу
        client.close()
    except Exception as e:
        # Запись о неудачном подключении в отдельный файл лога
        error_message = f"Failed to connect to {server['host']}: {str(e)}"
        print(error_message)
        logging.error(error_message)

ssh_key_passphrase = getpass.getpass("Введите пароль для ssh ключа: ")

# Перебираем все сервера и выполняем на них команды
for host in list_hosts:
    server = {'host': host, 'username': 'root', 'key_path': 'My_OpenSSH_NEWformat.ppk'}
    for command in commands:
        execute_command(server, command)
