import os

base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, "input.txt")


def extract_data(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            return
        

extract_data(file_path)