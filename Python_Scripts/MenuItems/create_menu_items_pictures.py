import base64

with open("Default Image.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

with open("output.txt", "w") as output_file:
    output_file.write(encoded_string.decode('utf-8'))
