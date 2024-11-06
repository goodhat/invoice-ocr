from openai import OpenAI
import base64
import os
import prompts
from models import Invoices, Invoice, generate_dummy_invoices
from typing import List
import csv
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
openai_api_key: str = os.getenv('OPENAI_API_KEY', '')
receiver_name: str = os.getenv('RECEIVER_NAME', '')
receiver_tax_id: str = os.getenv('RECEIVER_TAX_ID', '')
openai_model: str = os.getenv('OPENAI_MODEL', '')
data_folder: str = './data'
output_filename: str = 'invoices.csv'

DRY_RUN: bool = True

client = OpenAI(api_key=openai_api_key)


def convert_image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_fields_from_image(base64_images: List[str]) -> Invoices:
    # Prepare the message with the prompt and image
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": prompts.get_system_prompt(),
                },
            ],
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompts.get_user_prompt(receiver_name, receiver_tax_id),
                }
            ],
        }
    ]

    messages[1]["content"].extend([
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{image}"},
        } for image in base64_images
    ])

    parameters = {
        "model": openai_model,
        "messages": messages,
        "response_format": Invoices,
    }

    if DRY_RUN:
        invoices = generate_dummy_invoices(len(base64_images))
    else:
        completion = client.beta.chat.completions.parse(**parameters)
        invoices = completion.choices[0].message.parsed
        print(invoices)

    return invoices


def invoices_to_csv(invoices: List[Invoice], filename: str) -> None:
    fieldnames = Invoice.__fields__.keys()

    with open(filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for invoice in invoices:
            writer.writerow(invoice.dict())


def process_invoices_and_save_to_csv(folder_path: str, output_filename: str, batch_size: int = 3) -> None:
    invoices: List[Invoice] = []
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(
        ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif'))]

    for i in tqdm(range(0, len(image_files), batch_size)):
        batch_image_files = image_files[i:i + batch_size]

        # Convert batch images to base64
        base64_images: List[str] = []
        for image_file in batch_image_files:
            image_path = os.path.join(folder_path, image_file)
            base64_images.append(convert_image_to_base64(image_path))

        invoices.extend(extract_fields_from_image(base64_images).invoices)

    print(invoices)
    invoices_to_csv(invoices, output_filename)


process_invoices_and_save_to_csv(data_folder, output_filename)
