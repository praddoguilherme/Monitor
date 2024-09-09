import subprocess
import platform
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import pytz
import logging
import os
import threading

####Config do servidor SMTP########

SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
FROM_EMAIL = "COLOCAR E-MAIL PARA ENVIO"
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD') 
TIMEZONE = pytz.timezone('America/Sao_Paulo')

if EMAIL_PASSWORD is None:
    raise ValueError("A variavel de ambiente EMAIL_PASSWORD não esta definida.")

logging.basicConfig(
    filename='ping_monitor.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

##########Bloco de Stream de Log no terminal########

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logging.getLogger().addHandler(console_handler)

####################################################

#######Dicionário para armazenar o estado dos hosts####

host_status = {}

def send_email_alert(subject, body, to_email, smtp_connection):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email

    try:
        smtp_connection.sendmail(FROM_EMAIL, to_email, msg.as_string())
        logging.info("Email de alerta enviado com o assunto: %s", subject)
    except smtplib.SMTPException as e:
        logging.error(f"Falha ao enviar email: {e}")

def get_current_time():
    return datetime.now(TIMEZONE)

def ping_host(host, count, alert_email, smtp_connection=None):

    system = platform.system()
    ping_cmd = ["ping", "-n" if system == "Windows" else "-c", str(count), host]

    try:
        logging.info(f"Executando ping no host: {host}")
        result = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
        logging.debug(f"Resultado do ping para {host}: returncode={result.returncode}")

        if result.returncode == 0:
            logging.info(f"Sucesso!: {host} esta acessivel.")

            ######Resetar o estado do host se ele estiver acessível novamente#######

            if host in host_status:
                del host_status[host]
                logging.info(f"Estado do host {host} resetado apos acessibilidade.")

        else:
            logging.warning(f"Falha!: {host} nao esta acessivel.")
            current_time = get_current_time()

            ####### Verificar se já existe um registro do host e tempo do último e-mail##############

            if host not in host_status or (current_time - host_status[host]).total_seconds() > 900:

                logging.info(f"Enviando e-mail de alerta para o host {host} que falhou.")
                send_email_alert(
                    "Alerta: Host Inacessível",
                    f"O host {host} nao esta acessivel. Hora do alerta: {current_time.strftime('%Y-%m-%d %H:%M:%S')}",
                    alert_email,
                    smtp_connection
                )
                #######Atualizar o dicionário com o horário do último envio de e-mail########

                host_status[host] = current_time
                logging.info(f"Horario do ultimo envio de e-mail para {host} atualizado.")

    except subprocess.TimeoutExpired:
        logging.error(f"Timeout ao verificar o host {host}.")
        current_time = get_current_time()

        if host not in host_status or (current_time - host_status[host]).total_seconds() > 900:
            logging.info(f"Enviando e-mail de alerta para o host {host} devido ao timeout.")
            send_email_alert(
                "Alerta: Host Timeout",
                f"O host {host} nao respondeu dentro do tempo limite. Hora do alerta: {current_time.strftime('%Y-%m-%d %H:%M:%S')}",
                alert_email,
                smtp_connection
            )

            ###########Atualizar o dicionário com o horário do último envio de e-mail###########

            host_status[host] = current_time
            logging.info(f"Horário do último envio de e-mail para {host} atualizado.")

    except Exception as e:
        logging.error(f"Erro ao verificar o host {host}: {e}")

def ping_multiple_hosts(hosts, count, interval, alert_email):

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as smtp_connection:

        smtp_connection.starttls()
        smtp_connection.login(FROM_EMAIL, EMAIL_PASSWORD)

        while True:
            threads = []
            for host in hosts:
                logging.info(f"Iniciando verificacao para {host}")
                thread = threading.Thread(target=ping_host, args=(host, count, alert_email, smtp_connection))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
            
            time.sleep(interval)


hosts_input = input("Digite os IPs ou nomes dos hosts para verificar a conectividade, separados por vírgula: ")

hosts = [host.strip() for host in hosts_input.split(',')]
    
ping_multiple_hosts(hosts, count=4, interval=20, alert_email="EMAIL DE DESTINO AQUI")