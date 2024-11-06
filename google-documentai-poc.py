import os
from google.cloud import documentai_v1 as documentai
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

# Path to your Google Cloud service account JSON key file
SERVICE_ACCOUNT_PATH = 'invoice-ocr-credential.json'
# Set up credentials
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_PATH)

# Initialize the Document AI client
client = documentai.DocumentProcessorServiceClient(credentials=credentials)

# Google Cloud project details
project_id = os.getenv('DOCUMENTAI_PROJECT_ID', '')
location = os.getenv('DOCUMENTAI_LOCATION', '')
processor_id = os.getenv('DOCUMENTAI_PROCESSOR_ID', '')

# Configure the processor endpoint
processor_name = client.processor_path(project_id, location, processor_id)


def process_document(image_path):
    # Read the image content
    with open(image_path, 'rb') as image_file:
        image_content = image_file.read()

    # Create the Document AI request with the image content
    # Change to 'application/pdf' for PDFs
    document = {"content": image_content, "mime_type": "image/jpeg"}
    # params = documentai.ProcessRequest.Params({'language_code': 'zh-Hant'})  # For Traditional Chinese

    # Create the request
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=document
    )

    # Process the document
    result = client.process_document(request=request)
    document_data = result.document

    # Print structured data from the response
    print("Text:", document_data.text)

    # Loop through entities to get key-value pairs
    for entity in document_data.entities:
        print(f"Entity type: {entity.type_}")
        print(f"Entity mention: {entity.mention_text}")
        print(f"Confidence: {entity.confidence}")

    # You can further extract data as per your requirements
    return document_data


# Usage
image_path = 'data/010.jpg'
structured_data = process_document(image_path)
