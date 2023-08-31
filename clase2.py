from selenium import webdriver
import chromedriver_autoinstaller
import time
import helium as he

chromedriver_autoinstaller.install()

he.start_chrome("https://ebankpersonas.bancopatagonia.com.ar/eBanking/usuarios/cotizacionMonedaExtranjera.htm")

time.sleep(2)

cotizacion_element = he.find_all(he.S(".tdFinalRight"))

if True:
    cotizacion_text = cotizacion_element[0].web_element.text
    print("Cotizacion dolar banco Patagonia: ", cotizacion_text)
else:
    print("No se encontro la cotizacion")

#BANCO ICBC

he.go_to("https://www.icbc.com.ar/personas")

time.sleep(2)

cotizacion_element2 = he.find_all(he.S("#valor_compra_i4t1"))

if True:
    cotizacion_text2 = cotizacion_element2[0].web_element.text
    cadena = cotizacion_text2
    ultimos_nueve = cadena[-9:]

    print("Cotizacion dolar banco ICBC: ", ultimos_nueve)
else:
    print("No se encontro la cotizacion")


input()

he.kill_browser()
