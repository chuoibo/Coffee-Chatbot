import yaml

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