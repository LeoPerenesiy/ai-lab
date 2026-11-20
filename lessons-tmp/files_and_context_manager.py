class FileOpener:
    def __init__(self, file_path: str, mode:str):
        self.file_path = file_path
        self.mode = mode

    def __enter__(self):
        self.file = open(self.file_path, self.mode)
        return self.file
    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

with FileOpener('data.txt', 'r') as file:
    print(file.read())
