import pickle


def save_pickle_file(data, file_path):
    """
    Save a Python object to a pickled file.

    Parameters:
    - data: The Python object to be saved.
    - file_path: The file path where the pickled file will be saved.
    """
    with open(file_path, 'wb') as file:
        pickle.dump(data, file)
    print(f"Data saved to {file_path}")


def read_pickle_file(file_path):
    """
    Read a pickled file and return the Python object.

    Parameters:
    - file_path: The file path of the pickled file.

    Returns:
    - The Python object loaded from the pickled file.
    """
    with open(file_path, 'rb') as file:
        data = pickle.load(file)
    print(f"Data loaded from {file_path}")

    return data
