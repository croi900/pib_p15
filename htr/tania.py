import boto3


def ocr():
    # Replace with your AWS credentials
    aws_access_key_id = 'SECRET KEY'
    aws_secret_access_key = 'AWS ACESS KEY'
    region_name = 'eu-west-3'  # Replace with your desired AWS region

    # Initialize the Textract client
    textract_client = boto3.client('textract', region_name=region_name,
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)

    # Read the image file (replace 'your_image.jpg' with the actual file path)
    with open('board.jpeg', 'rb') as image_file:
        image_bytes = bytearray(image_file.read())

    # Call Amazon Textract to detect document text
    response = textract_client.detect_document_text(Document={'Bytes': image_bytes})

    with open('output.txt', 'w') as f:
        for item in response['Blocks']:
            if item['BlockType'] == 'LINE':
                f.write(item['Text'] + '\n')
