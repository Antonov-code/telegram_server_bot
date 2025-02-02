import configparser
import psutil
import telebot
import time

config = configparser.ConfigParser()
config.read('config.ini')
API_KEY = config.get('DEFAULT', 'api_key')


bot = telebot.TeleBot(API_KEY)


def get_server_status():
    cpu_load = psutil.cpu_percent(interval=1)  # Загрузка CPU
    memory = psutil.virtual_memory()  # ОЗУ
    disk = psutil.disk_usage('/')  # Использование диска
    status = (
        f"📊 *Статус сервера:*\n"
        f"🖥 *CPU*: {cpu_load}%\n"
        f"💾 *RAM*: {memory.percent}% (использовано {memory.used // (1024**3)}ГБ из {memory.total // (1024**3)}ГБ)\n"
        f"📀 *Disk*: {disk.percent}% (свободно {disk.free // (1024**3)}ГБ из {disk.total // (1024**3)}ГБ)"
    )
    return status



def get_network_usage():
    before = psutil.net_io_counters()  # Получаем данные до задержки
    time.sleep(1)  # Ждём 1 секунду
    after = psutil.net_io_counters()  # Получаем данные после задержки

    bytes_sent = after.bytes_sent - before.bytes_sent
    bytes_recv = after.bytes_recv - before.bytes_recv
    
    status = (
        f"📨 Скорость отдачи: {bytes_sent / 1024:.2f} KB/s\n"
        f"📡 Скорость загрузки: {bytes_recv / 1024:.2f} KB/s"
    )
    return status


def get_process():
    # all_proc = []
    # for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
    #     proc_row = f"🔹 PID: {proc.info['pid']} | Процесс: {proc.info['name']} | Владелец: {proc.info['username']}\n"
    #     all_proc.append(proc_row)
    # return str(all_proc)
    return "Функция недоступна!"
    
@bot.message_handler(commands=['start', 'main', 'help'])
def send_status(message):
    help_info = """/status - статус;\n/network - загрузка/отдача трафика в данный момент;\n/proc - процессы;\n/penis - ."""
    bot.send_message(message.chat.id, help_info, parse_mode="Markdown")

@bot.message_handler(commands=['status'])
def send_status(message):
    status = get_server_status()
    bot.send_message(message.chat.id, status, parse_mode="Markdown")

@bot.message_handler(commands=['network'])
def send_status(message):
    status = get_network_usage()
    bot.send_message(message.chat.id, status, parse_mode="Markdown")

@bot.message_handler(commands=['proc'])
def send_status(message):
    status = get_process()
    bot.send_message(message.chat.id, status, parse_mode="Markdown")


bot.polling()