import subprocess
import os
from google.genai import types

def run_python_file(working_directory, file_path,args=None):
    abs_working_dir = os.path.abspath(working_directory)
    new_f_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not new_f_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(new_f_path):
        return f'Error: File "{file_path}" not found.'

    if not new_f_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        return_string = ""
        commands = ["python", new_f_path]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )

        if result.stdout == b'':
            return_string = f"No outut produced.\n"

        if result.stdout != b'':
            return_string = f"STDOUT: {result.stdout}\n"

            if result.stderr != b'':
                return_string += f"STDERR: {result.stderr}\n"

        if result.check_returncode() != None:
            return_string+= f"Process exited with code {result.check_returncode()}"
        
        return return_string
    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)