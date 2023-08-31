from selenium import webdriver
import chromedriver_autoinstaller
import time
import helium as he
import csv
import json

chromedriver_autoinstaller.install()

#--------------------------------------------------------------------------------------------------------
#BUSCAR PRODUCTOS FULLHARD
#--------------------------------------------------------------------------------------------------------

product = input("Ingrese el producto a buscar: ")
ind = int(input("Ingrese el número de productos a buscar: "))

he.start_chrome("https://www.fullh4rd.com.ar/")
time.sleep(2)

search_box = he.find_all(he.S("#searchid"))[0]
he.click(search_box)
he.write(product, into=search_box)
he.press(he.ENTER)
time.sleep(2)

# Ordenar por menor precio
he.click(he.S(".filter .cats .active"))
time.sleep(2)

# Buscar producto y precio
product_name = he.find_all(he.S(".info h3"))
product_price = he.find_all(he.S(".info .price span"))

# Lista para almacenar los resultados
fullhard_results = []

# Obtener los datos de los productos
if product_name:
    for prod in product_name[:ind]:
        name = prod.web_element.text
        price_element = product_price[product_name.index(prod)].web_element
        price = price_element.text.replace("$", "").replace(" ", "").replace(",", "")
        fullhard_results.append({"Producto": name, "Precio": price})

# #--------------------------------------------------------------------------------------------------------
# #BUSCAR PRODUCTOS MERCADOLIBRE
# #--------------------------------------------------------------------------------------------------------

he.go_to("https://www.mercadolibre.com.ar/")
time.sleep(2)

search_box2 = he.find_all(he.S(".nav-search-input"))[0]
he.click(search_box2)
he.write(product, into=search_box2)
he.press(he.ENTER)
time.sleep(2)

filter_menu = he.find_all(he.S(".andes-dropdown__trigger"))[0]
he.click(filter_menu)
time.sleep(2)

# Hacer clic en el filtro "Menor precio" utilizando XPath
try:
    filter_option = he.find_all(he.S("//span[contains(text(), 'Menor precio')]"))[0]
    he.click(filter_option)
    print("Filtro 'Menor precio' aplicado")
except IndexError:
    print("No se encontró la opción de filtro 'Menor precio'")

time.sleep(3)

product_name2 = he.find_all(he.S(".ui-search-item__title"))
product_price2 = he.find_all(he.S(".andes-money-amount__fraction"))

# Lista para almacenar los resultados
mercadolibre_results = []

if product_name2:
    for prod in product_name2[:ind]:
        name = prod.web_element.text
        price_element = product_price2[product_name2.index(prod)].web_element
        price = price_element.text.replace("$", "").replace(" ", "").replace(".", "").replace(",", "")
        mercadolibre_results.append({"Producto": name, "Precio": price})

# #--------------------------------------------------------------------------------------------------------
# #BUSCAR PRODUCTOS LIBREOPCION
# #--------------------------------------------------------------------------------------------------------

he.go_to(f"https://www.libreopcion.com/{product}?o=asc")
time.sleep(5)

# Buscar producto y precio
product_name3 = he.find_all(he.S(".description"))
product_price3 = he.find_all(he.S(".price-final"))

# Lista para almacenar los resultados
libreopcion_results = []

if product_name3:
    for prod, price_element in zip(product_name3[:ind], product_price3[:ind]):
        name = prod.web_element.text

        # Obtener el precio sin los últimos dos caracteres "00"
        price_text = price_element.web_element.text
        if price_text.endswith("00"):
            price_text = price_text[:-2]

        price = price_text.replace("$", "").replace(".", "").replace(",", "")
        libreopcion_results.append({"Producto": name, "Precio": price})

# Guardar resultados en un archivo CSV
csv_filename = f"{product}_results.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["Producto", "Precio"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for result in fullhard_results:
        writer.writerow(result)

    for result in mercadolibre_results:
        writer.writerow(result)

    for result in libreopcion_results:
        writer.writerow(result)

print(f"Los resultados se han guardado en el archivo '{csv_filename}'.")

# Guardar resultados en un archivo JSON
json_filename = f"{product}_results.json"
with open(json_filename, "w", encoding="utf-8") as jsonfile:
    json.dump({"Fullh4rd": fullhard_results, "MercadoLibre": mercadolibre_results, "LibreOpcion": libreopcion_results}, jsonfile, indent=4)

print(f"Los resultados se han guardado en el archivo '{json_filename}'.")

input()

he.kill_browser()