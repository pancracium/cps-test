from PIL import Image

def convert_to_ico(input_path, output_path):
    img = Image.open(input_path)
    img.save(output_path, format='ICO')

# Usage example
input_file = input("File name: ")
name = input_file.split(".")[0]
output_file = name + ".ico"
convert_to_ico(input_file, output_file)