import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    
    if directory is None:
        return f"Error: No directory specified"

    new_dir = os.path.abspath(os.path.join(working_directory, directory))
    #print(new_dir)
    #print("hi")
    if not os.path.abspath(new_dir).startswith(os.path.abspath(working_directory)):
        # new_dir = os.path.join(working_directory, directory)
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(new_dir):
        return f'Error: "{directory}" is not a directory'

    return_str = ""
    for item in os.listdir(new_dir):
        item_path = os.path.join(new_dir, item)
        return_str += f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}\n"
    return return_str

#print(get_files_info("calculator", "."))
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)