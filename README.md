# Račun

"Račun" je jednostavni pokazni Python program koji koristi klase i objekte kao glavne gradivne elemente.


## Što su klase, a što objekti?

- **Klase** u objektno orijentiranom programiranju su nacrti, tj. predlošci po kojima se kreiraju objekti.

- **Objekti** su konkretne realizacije kreirane na temelju klasa.

![Klase i objekti](/img/klase.jpeg)

U primjeru sa slike **Smartphone** je klasa sa atributima **Procesor**, **RAM**, **Veličina ekrana** i **Memorija**. Stvarne realizacije klase Smartphone su objekti **iPhone 14 Pro**, **Samsung Galaxy S22** i **Xiaomi 12** i svaki od njih ima svoje jedinstvene atribute definirane u nacrtu tj. klasi.

## Program Račun
U programu su definirane 4 klase:
 - **Product** - definiraju proizvode koji se nalaze u trogvini
 - **InvoiceItem** - definiraju stavke tj proizvode na računu
 - **Invoice** - definira račun
 - **InvoiceRenderer** - služi za ispis računa na ekran

## Pokretanje programa
1. Otvoriti terminal i pozicionirati se u direktorij aplikacije
2. Pokrenuti program sa naredbom `python app.py`

## Uputstvo za uporabu

- ### Kreiranje proizvoda
```python
coca_cola = Product(name="Coca Cola 0.5", price_without_vat=0.75)
milk = Product(name="Milk 1L", price_without_vat=0.8)
water = Product(name="Water 1L", price_without_vat=0.4, vat=0.1)
```
- ### Kreiranje računa
```python
invoice_1 = Invoice(
	items=[InvoiceItem(product=milk), InvoiceItem(product=water, quantity=3)]
)
```
- ### Dodavanje stavke na račun
```python
invoice_1.add_invoice_item(InvoiceItem(product=coca_cola, quantity=10))
```
 - ### Ažuriranje količine proizvoda na stavci računa

 U prethodnom primjeru smo dodali treću stavku na račun, 10 komada Coca Cole. Recimo da smo se zabunili u unosu količine i sada želimo to prepraviti na 1 Coca Colu. Prvi parametar medode `update_quantity()` je redni broj stavke, a drugi parametar nova količina.
```python
invoice_1.update_quantity(3, 1)
```

- ### Brisanje stavke sa računa
Recimo da smo se ipak predomislili i ne želimo uopće imati Coca colu na računu. Stavku brišemo sa metodom `remove_invoice_item()` koja kao parametar prima redni broj stavke.
```python
invoice_1.remove_invoice_item(3)
```
- ### Ispis računa
```python
invoice_1_renderer = InvoiceRenderer(invoice_1)
invoice_1_renderer.render()
