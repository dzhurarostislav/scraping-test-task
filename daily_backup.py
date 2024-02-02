import os
import subprocess

from datetime import datetime
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCRAPY_PROJECT_ROOT = os.path.join(PROJECT_ROOT, "auto_ria")


load_dotenv()

def create_database_dump(database_name, username, password, dumps_folder):
    dumps_folder_path = os.path.join(PROJECT_ROOT, dumps_folder)
    os.makedirs(dumps_folder_path, exist_ok=True)
    output_file_path = os.path.join(dumps_folder_path, f"dump_{datetime.now().strftime('%Y%m%d%H%M%S')}.dump")

    command = [
        "pg_dump",
        "-h", "localhost",
        "-U", username,
        "-d", database_name,
        "-Fc",
        "-f", output_file_path
    ]

    os.environ["PGPASSWORD"] = password

    subprocess.run(command, cwd=SCRAPY_PROJECT_ROOT)


def main():
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    database_name = os.getenv("DATABASE")
    dumps_folder = "dumps"

    create_database_dump(database_name, username, password, dumps_folder)


if __name__ == "__main__":
    main()
