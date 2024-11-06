def get_system_prompt() -> str:
    system_prompt = '''
Extract the following structured data fields from multiple invoice images, adhering to specific formats for each field where applicable:

supplier_name: The name of the supplier. Typically located near the top or middle of the invoice.

supplier_tax_id: An eight-digit ID for the supplier, usually located near the supplier's name or address. Format: XXXXXXXX (eight digits).

receiver_name: The name of the receiver, which may be marked with a label such as "買受人" (meaning "buyer" or "receiver" in Chinese).

receiver_tax_id: An eight-digit ID for the receiver, similar in format to the supplier’s tax ID. Format: XXXXXXXX.

invoice_id: A unique identifier for the invoice, typically in the format of two letters followed by eight digits. Format: XXNNNNNNNN.

sale_amount: The sale subtotal before tax, usually located near the bottom section of the invoice, often labeled as "銷售額" (meaning "sale amount" in Chinese). Format: a numeric value, typically in TWD (New Taiwan Dollar).

tax_amount: The tax amount for the sale, also near the bottom of the invoice. This field may be labeled as "營業稅" (meaning "tax" in Chinese). Format: a numeric value, typically in TWD.

total_amount: The final amount including tax. This is often labeled as "總計" (meaning "total" in Chinese) and is located near the sale and tax amounts. Format: a numeric value, typically in TWD.

tx_date: The transaction date, ideally formatted as yyyy/mm/dd. This may be labeled with "日期" (meaning "date" in Chinese) and is generally located near the top or in the details section of the invoice. Format: yyyy/mm/dd.

Requirements:

If certain fields are not present or legible in the image, return a placeholder such as NULL.
Use numeric values where expected, and ensure dates follow the yyyy/mm/dd format.
Return the extracted information as a structured JSON object, with the field names as keys and extracted data as values.

{
  "supplier_name": "Supplier Co., Ltd.",
  "supplier_tax_id": "12345678",
  "receiver_name": "Receiver Corp.",
  "receiver_tax_id": "87654321",
  "invoice_id": "AB12345678",
  "sale_amount": 420,
  "tax_amount": 21,
  "total_amount": 441,
  "tx_date": "2024/09/30"
}
'''
    return system_prompt


def get_user_prompt(receiver_name: str, receiver_tax_id: int) -> str:
    user_prompt = f"買方是「{receiver_name}」，統編是 {receiver_tax_id}"
    return user_prompt
