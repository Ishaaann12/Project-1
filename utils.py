import os

def safe_path(filename):
    """Returns a safe path, adjusting for `/app/` in Podman."""
    base_path = os.getenv('AIPROXY_TOKEN') and '/app/data' or 'data'
    return os.path.join(base_path, filename)

def read_file(path):
    """Reads the content of a file and returns it as a string."""
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return f.read()

def write_file(path, content):
    """Writes content to a specified file."""
    with open(path, 'w') as file:
        file.write(content)


# import os

# def read_file(path):
#     """Reads the content of a file and returns it as a string."""
#     if not os.path.exists(path):
#         return None
#     with open(path, "r") as f:
#         return f.read()

# def safe_path(filename):
#     """Returns a safe path within the /data directory."""
#     return os.path.join("data", filename)

# def write_file(path, content):
#     """Writes content to a specified file."""
#     with open(path, 'w') as file:
#         file.write(content)