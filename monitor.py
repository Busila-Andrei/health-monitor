import yaml
import logging
import smtplib
from email.mime.text import MIMEText
from checks.registry import build_checks

logging.basicConfig(
    filename="monitor.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_config(path="config.yml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def send_email_alert(failed_results, email_config):
    body = "\n".join(str(r) for r in failed_results)
    msg = MIMEText(body)
    msg['Subject'] = "Health Monitor Alert"
    msg['From'] = email_config['sender']
    msg['To'] = email_config['receiver']

    with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
        server.starttls()
        server.login(email_config['sender'], email_config['password'])
        server.send_message(msg)


def main():
    config = load_config()
    checks = build_checks(config["checks"])

    results = []
    for check in checks:
        result = check.run()
        results.append(result)
        log_level = logging.INFO if result.ok else logging.WARNING
        logging.log(log_level, str(result))

    failed = [r for r in results if not r.ok]

    if failed:
        send_email_alert(failed, config['email'])
        logging.warning(f"Alert sent for {len(failed)} failed check(s)")


if __name__ == "__main__":
    main()