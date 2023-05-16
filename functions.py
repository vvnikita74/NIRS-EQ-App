def get_file_name(path):
    # Find the index of the last slash in the path
    last_slash = path.rfind("/")
    # Find the index of the last dot in the path
    last_dot = path.rfind(".")
    # Extract the file name substring from the path
    file_name = path[last_slash+1:last_dot]
    return file_name


def str_format_to_pyformat(str_format):
    match str_format:
        case "Int16": return 8
        case "Int24": return 4
        case "Int8": return 16
        case "Float32": return 1
        case "UInt8": return 32

