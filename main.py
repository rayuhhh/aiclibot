import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_functions import available_functions, call_function
from functions.config import MAX_ITER



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

def main():
    #print("Hello from bootdevaibot!")
    #print(get_files_info("calculator", "../"))
    
    verbose = "--verbose" in sys.argv # marks True if in sys arguments
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    user_prompt = sys.argv[1]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt),
    )
    # OLD CODE XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    # generate_content(client, messages, verbose)


    #### being worked on above is testing
    try:
        for i in range(MAX_ITER):
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(f"Final response: {final_response}")
                break
    except Exception as e:
        print(f"Error: {e} from generate_content")




def generate_content(client, messages, verbose):

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt),
        )
    # if "--verbose" in sys.argv:
    #     # print(f"User prompt: {user_prompt}")
    #     print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    #     print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    ##############
    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    ######################

    if not response.function_calls:
        return response.text

    function_responses = []

    for function_call_part in response.function_calls:
        #print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_response))
    #print(response.candidates)

    # [Content(parts=[Part(video_metadata=None, thought=None, code_execution_result=None, executable_code=None, file_data=None, function_call=None, function_response=None, inline_data=None, text='what files are in the root?')], role='user')]


if __name__ == "__main__":
    main()
