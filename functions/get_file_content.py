from .config import MAX_CHARS
import os
from google.genai import types


def get_file_content(working_directory, file_path):
    new_f_path = os.path.join(os.path.abspath(working_directory), file_path)

    if not new_f_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(new_f_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:

        with open(new_f_path, "r") as f:
            file_content_str = f'{f.read(MAX_CHARS)}'
        return file_content_str
    
    except Exception as e:
        print(f'Error: {e}')

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the first {MAX_CHARS} characters of contents from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to file whose contents should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)