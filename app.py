import itertools
import locale
from datetime import datetime
from typing import List

# settings
SHOP_NAME = "Pero shop"
VAT = 0.25
CURRENCY = "€"
RENDER_ITEM_CHARS = 25


# class definitions
class Product:
    id_obj = itertools.count()

    def __init__(self, name: str, price_without_vat: float, vat: float = VAT) -> None:
        self.id = next(Product.id_obj) + 1
        self.name = name
        self.price_without_vat = price_without_vat
        self.vat = vat

    def __repr__(self) -> str:
        return f"[{self.id}] {self.name}"

    @property
    def price_with_vat(self) -> float:
        return round(self.price_without_vat + (self.price_without_vat * self.vat), 2)

    def update_price_without_vat(self, price) -> None:
        self.price_without_vat = price

    def update_name(self, name) -> None:
        self.name = name


class InvoiceItem:
    def __init__(self, product: Product, quantity: int = 1) -> str:
        self.order = None
        self.product = product
        self.quantity = quantity

    @property
    def price_with_vat(self) -> float:
        return round(self.product.price_with_vat * self.quantity, 2)

    @property
    def price_without_vat(self) -> float:
        return round(self.product.price_without_vat * self.quantity, 2)

    @property
    def vat(self) -> float:
        return round(self.price_with_vat - self.price_without_vat, 2)

    def __repr__(self) -> str:
        return f"{self.order}. {self.product.name} {self.quantity}"


class Invoice:
    id_obj = itertools.count()

    def __init__(self, items: List[InvoiceItem]) -> None:
        # This is for invoice number in specified format
        self.order = next(Invoice.id_obj) + 1

        if items:
            self.items = items
            self.update_items_orders()
        else:
            self.items = []

        self.timestamp = datetime.now()

    @property
    def id(self) -> float:
        return f"I-{self.timestamp.strftime('%Y%m%d')}-{str(self.order).rjust(5, '0')}"

    @property
    def sum_with_vat(self) -> float:
        return round(
            sum([invoice_item.price_with_vat for invoice_item in self.items]), 2
        )

    @property
    def sum_without_vat(self) -> float:
        return round(
            sum([invoice_item.price_without_vat for invoice_item in self.items]), 2
        )

    @property
    def vat(self) -> float:
        return round(self.sum_with_vat - self.sum_without_vat, 2)

    def update_items_orders(self) -> None:
        count = itertools.count()
        for invoice_item in self.items:
            invoice_item.order = next(count) + 1

    def update_quantity(self, invoice_item_ord_num: int, new_quantity: int) -> None:
        updated = False
        for item in self.items:
            if item.order == invoice_item_ord_num:
                item.quantity = new_quantity
                updated = True
                break

        if not updated:
            print("Invoice item with selected order does not exists.")

    def remove_invoice_item(self, invoice_item_ord_num: int) -> None:
        removed = False
        for item in self.items:
            if item.order == invoice_item_ord_num:
                self.items.remove(item)
                removed = True
                self.update_items_orders()
                break

        if not removed:
            print("Invoice item with selected order does not exists.")

    def add_invoice_item(self, invoice_item: InvoiceItem) -> None:
        self.items.append(invoice_item)
        self.update_items_orders()


class InvoiceRenderer:
    def __init__(self, invoice) -> None:
        locale.setlocale(locale.LC_ALL, "de_DE")
        self.invoice = invoice

    @property
    def invoice_items_headers(self) -> list:
        return (
            self.get_cell_text("#"),
            self.get_cell_text("Product"),
            self.get_cell_text("Price"),
            self.get_cell_text("Quantity"),
            self.get_cell_text("Price sum without VAT"),
            self.get_cell_text("VAT %"),
            self.get_cell_text(f"VAT {CURRENCY}"),
            self.get_cell_text("Price sum with VAT"),
        )

    def get_cell_text(self, text: str) -> str:
        str_text = str(text)
        if len(str_text) >= RENDER_ITEM_CHARS:
            return str_text[:RENDER_ITEM_CHARS]
        else:
            return str_text.ljust(RENDER_ITEM_CHARS)

    def get_price(self, price) -> str:
        return f"{locale.currency(price, grouping=True, symbol=False)} €"

    def get_invoice_items_headers(self) -> str:
        return "".join(self.invoice_items_headers)

    def get_separators(self, separator):
        return separator * RENDER_ITEM_CHARS * len(self.invoice_items_headers)

    def get_invoice_items_body(self, invoice_items: List[InvoiceItem]) -> str:
        output = ""
        for idx, item in enumerate(invoice_items):
            output += "".join(
                (
                    self.get_cell_text(f"{item.order}."),
                    self.get_cell_text(item.product.name),
                    self.get_cell_text(self.get_price(item.product.price_without_vat)),
                    self.get_cell_text(item.quantity),
                    self.get_cell_text(self.get_price(item.price_without_vat)),
                    self.get_cell_text(f"{int(item.product.vat*100)} %"),
                    self.get_cell_text(self.get_price(item.vat)),
                    self.get_cell_text(self.get_price(item.price_with_vat)),
                    "\n\t" if not len(invoice_items) == idx + 1 else "",
                )
            )

        return output

    def render(self) -> str:
        if not len(self.invoice.items):
            print("Invoice has no items")
            exit()
        date_rendered = self.invoice.timestamp.strftime("%d.%m.%Y %H:%M:%S")
        print(
            f"""
        {SHOP_NAME}
        {self.get_separators('=')}
        {self.get_cell_text("Invoice ID:")} {self.get_cell_text(self.invoice.id)}
        {self.get_cell_text("Invoice date:")} {self.get_cell_text(date_rendered)}
        {self.get_separators('-')}
        ITEMS:
        {self.get_invoice_items_headers()}
        {self.get_invoice_items_body(self.invoice.items)}
        {self.get_separators('-')}
        {self.get_cell_text("Price without VAT:")} {self.get_price(self.invoice.sum_without_vat)}
        {self.get_cell_text("VAT:")} {self.get_price(self.invoice.vat)}
        {self.get_separators('.')}
        {self.get_cell_text("Price with VAT:")} {self.get_price(self.invoice.sum_with_vat)}
        {self.get_separators('.')}
        {self.get_separators('=')}
        """
        )


# create products
coca_cola = Product(name="Coca Cola 0.5", price_without_vat=0.75)

milk = Product(name="Milk 1L", price_without_vat=0.8)

water = Product(name="Water 1L", price_without_vat=0.4, vat=0.1)

# create invoice
invoice_1 = Invoice(
    items=[InvoiceItem(product=milk), InvoiceItem(product=water, quantity=3)]
)
invoice_1.add_invoice_item(InvoiceItem(product=coca_cola, quantity=1))

# render invoice
invoice_1_renderer = InvoiceRenderer(invoice_1)
invoice_1_renderer.render()
