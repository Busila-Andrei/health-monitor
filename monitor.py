import psutil
import smtplib
import logging
import json
import time
from email.mime.text import MIMEText
from datetime import datetime

logging.basicConfig(
    filename="monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_disk_usage(path="/"):
    return psutil.disk_usage(path).percent

def get_battery():
    battery = psutil.sensors_battery()
    if battery is None:
        return None
    return battery.percent

def check_thresholds(metrics, thresholds):
    problems = []
    if metrics['cpu'] > thresholds['cpu']:
        problems.append(f"CPU la {metrics['cpu']}, threshold {thresholds['cpu']}%")
    if metrics['ram'] > thresholds['ram']:
        problems.append(f"RAM la {metrics['ram']}, threshold {thresholds['ram']}%")
    if metrics['disk'] > thresholds['disk']:
        problems.append(f"Disk la {metrics['disk']}, threshold {thresholds['disk']}%")
    return problems

def send_email_alert(problems, email_config):
    body = "\n".join(problems)
    msg = MIMEText(body)
    msg['Subject'] = "Alerta System Healt Monitor"
    msg['From'] = email_config['sender']
    msg['To'] = email_config['receiver']

    with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
        server.starttls()
        server.login(email_config['sender'], email_config['password'])
        server.send_message(msg)


def main():
    config = load_config()
    metrics = {
        'cpu': get_cpu_usage(),
        'ram': get_ram_usage(),
        'disk': get_disk_usage(),
    }
    logging.info(f"CPU={metrics['cpu']}% RAM={metrics['ram']}% Disk={metrics['disk']}%")

    problems = check_thresholds(metrics, config['thresholds'])

    if problems:
        send_email_alert(problems, config['email'])
        logging.warning(f"Alerta trimisa: {problems}")

if __name__ == "__main__":
    main()
