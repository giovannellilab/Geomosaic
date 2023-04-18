
import os


def validate_working_dir(working_dir):
    if not os.path.exists(working_dir):
        print(f"Inserted wdir path '{working_dir}' does not exists.")
        exit(code=1)

    if not os.path.isdir(working_dir):
        print(f"{working_dir} is not a directory")
        exit(code=1)
