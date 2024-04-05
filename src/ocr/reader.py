
# File to read files and images to text using ocr



class  ReadFile:
    def __init__(self, file_name):
        self.file_name = file_name

    def read_file(self):
        with open(self.file_name, 'r') as file:
            return file.read()

    def read_image(self):
        with open(self.file_name, 'rb') as file:
            return file.read()
        

#  A class that writes the given  text to a file

class WriteFile:
    def __init__(self, file_name):
        self.file_name = file_name

    def write_file(self, text):
        with open(self.file_name, 'w') as file:
            file.write(text)

