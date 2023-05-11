import paramiko
import getpass

# Список удаленных серверов
servers = [
    {'host': '10.45.20.17', 'username': 'root', 'key_path': 'cv_p_OpenSSH-formatNEW_PS.ppk'},
    {'host': '10.45.20.19', 'username': 'root', 'key_path': 'cv_p_OpenSSH-formatNEW_PS.ppk'},
    {'host': '10.45.20.20', 'username': 'root', 'key_path': 'cv_p_OpenSSH-formatNEW_PS.ppk'},
]

# Список команд, которые необходимо выполнить
commands = [
    'uname -a',
    'uptime',
    'script_backup.sh &',
     'python3 my_py_script.py'
]

# Функция для выполнения команд на удаленном сервере
def execute_command(server, command):
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

    # Вывод результата
    print('\n------------------------------------------------------------------')
    print('On HOST                    -   {}'.format(server['host']))
    print('Result of executed command   -   {} \n'.format(command))
    for line in stdout:
        print(line.strip('\n'))

    # Закрытие подключения к серверу
    client.close()

ssh_key_passphrase = getpass.getpass("Введите пароль для ssh ключа: ")

# Перебираем все сервера и выполняем на них команды
for server in servers:
    for command in commands:
        execute_command(server, command)


#input("Введите любой символ и нажмите Enter, чтобы закрыть программу...")

