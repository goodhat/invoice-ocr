
from pydantic import BaseModel
import random


class Invoice(BaseModel):
    supplier_name: str
    supplier_tax_id: int
    receiver_name: str
    receiver_tax_id: int
    invoice_id: str
    sale_amount: float
    tax_amount: float
    total_amount: float
    tx_date: str


class Invoices(BaseModel):
    invoices: list[Invoice]


def generate_dummy_invoices(num: int) -> Invoices:
    return Invoices(
        invoices=[generate_dummy_invoice(i) for i in range(num)]
    )


def generate_dummy_invoice(index: int) -> Invoice:
    return Invoice(
        supplier_name=f"Supplier {index}",
        supplier_tax_id=10000000 + index,
        receiver_name=f"Receiver {index}",
        receiver_tax_id=88888888,
        invoice_id=f"DV-{index:04d}",
        sale_amount=round(random.uniform(100, 1000), 2),
        tax_amount=round(random.uniform(10, 100), 2),
        total_amount=round(random.uniform(110, 1100), 2),
        tx_date="2024/01/01"
    )
