import yaml

from src.utils.response import get_chat_response

def load_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        raise
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file '{file_path}': {e}")
        raise


def double_check_json_output(client,model_name,json_string):
    prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    Do NOT return a single letter outside of the json string.
        {json_string}
    """

    messages = [{"role": "user", "content": prompt}]

    response = get_chat_response(client,model_name,messages)

    return response