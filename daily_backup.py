import subprocess
from datetime import datetime
import os

# Assuming the script is in the project root
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCRAPY_PROJECT_ROOT = os.path.join(PROJECT_ROOT, "auto_ria")


def create_database_dump(database_name, username, password, dumps_folder):
    # Create the "dumps" folder if it doesn't exist
    dumps_folder_path = os.path.join(PROJECT_ROOT, dumps_folder)
    os.makedirs(dumps_folder_path, exist_ok=True)
    output_file_path = os.path.join(dumps_folder_path, f'dump_{datetime.now().strftime("%Y%m%d%H%M%S")}.dump')
    # Formulate the command to run pg_dump
    command = [
        'pg_dump',
        '-h', 'localhost',
        '-U', username,
        '-d', database_name,
        '-Fc',
        '-f', output_file_path
    ]

    # Set the PGPASSWORD environment variable to provide the password
    os.environ['PGPASSWORD'] = password

    # Run the pg_dump command
    subprocess.run(command, cwd=SCRAPY_PROJECT_ROOT)


def main():
    database_name = "AutoRiaDB"
    username = "postgres"
    password = ""
    dumps_folder = "dumps"

    create_database_dump(database_name, username, password, dumps_folder)


if __name__ == "__main__":
    main()
