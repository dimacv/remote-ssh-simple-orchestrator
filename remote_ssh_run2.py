import paramiko
import getpass
import logging

# Список удаленных серверов
list_hosts = ["DBPDPFDR1",
              "DBPDPFDR3",
              "10.45.20.28",
              "10.45.20.29", 
              "10.45.20.30", 
              "10.45.20.31",
              "10.45.20.36", 
              "10.45.20.37", 
              ]

# Список команд, которые необходимо выполнить
commands = [
    'mount /nfs_shares/backup_os', 
    '/nfs_shares/backup_os/scripts/add_scan_unix.sh', 
    'lsuser scan_unix'
    ]


servers = []
for host in list_hosts:
    servers.append({'host': host, 'username': 'root', 'key_path': 'My_OpenSSH_NEWformat.ppk'})

# Определение формата вывода в лог
logging.basicConfig(filename='log_file.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Функция для выполнения команд на удаленном сервере
def execute_command(server, command):

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
        passphrase = ssh_key_passphrase

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

ssh_key_passphrase = getpass.getpass("Введите пароль для ssh ключа: ")


# Перебираем все сервера и выполняем на них команды
for server in servers:
    for command in commands:
        execute_command(server, command)

