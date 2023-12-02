import logging
import sys
import click
from logging import getLogger
from langchain.chat_models.gigachat import GigaChat
from parse_dialogs import process_dialogs

logger = getLogger()
logger.setLevel(logging.WARNING)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def create_chat(credentials_path: str) -> GigaChat:
    with open(credentials_path, "r") as file:
        credentials = file.read().strip()
    return GigaChat(credentials=credentials, verify_ssl_certs=False)


@click.command()
@click.option("--input", "-i", help="Path to input file", required=True)
@click.option("--output", "-o", help="Path to output file", default="report.xlsx")
@click.option("--credentials", "-c", help="Path to credentials file", default="credentials.txt")
def run(input: str, output: str, credentials: str):
    chat = create_chat(credentials)
    process_dialogs(chat, input, output)

if __name__ == "__main__":
    run()
