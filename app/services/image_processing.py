import base64

def get_base64_image(image_file) -> str:
    image_data = image_file.read()
    base64_image = base64.b64encode(image_data).decode('utf-8')
    return base64_image
