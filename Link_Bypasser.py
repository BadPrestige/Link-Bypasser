#!/usr/bin/env python3

import requests
import argparse
import colorama
from colorama import Fore, Style
from urllib.parse import urlparse
from datetime import datetime
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

colorama.init(autoreset=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36"
}

ACORTADORES_COMUNES = set([
    'bit.ly', 'tinyurl.com', 'is.gd', 't.co', 'goo.gl', 'ow.ly', 'buff.ly', 'rebrand.ly', 'shorte.st', 'adf.ly',
    'bc.vc', 'linkvertise.com', 'ouo.io', '1link.club', 'cutt.ly', 'shorturl.at', 'v.gd', 'bl.ink', 'soo.gd',
    'ity.im', 'mcaf.ee', 'tiny.cc', 'qr.ae', 'urlzs.com', 'clk.sh', 'short.am', 'droplink.co', 'megaurl.in',
    'link-to.net', 'linktr.ee', 'lnk.bio', 'linksly.co', 'hypel.ink', 'social-unlock.com', 'gg.gg', 'adshort.co',
    'tny.im', 'adcraft.co', 'adfoc.us', 'lnkfi.re', 'zws.im', 'yourls.org', 'cutpaid.com', 'shrinkme.io', 'exe.io',
    'link.tl', 'linkbucks.com', 'shrinkearn.com', 'adshort.link', 'linkrex.net', 'daughablelea.com', 'psurls.com'
])

ENLACES_IRRELEVANTES = set([
    "fonts.googleapis.com", "fonts.gstatic.com", "google-analytics.com", "ads", "doubleclick.net"
])

def limpiar_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

def usar_selenium(url):
    try:
        options = Options()
        options.headless = True
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'user-agent={HEADERS["User-Agent"]}')

        with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options) as driver:
            driver.set_page_load_timeout(20)
            driver.get(url)
            time.sleep(5)
            return driver.current_url
    except Exception as e:
        return f"{Fore.RED}[Selenium Error] {e}"

def extraer_links_relevantes(html):
    encontrados = re.findall(r'(https?://[\w\.-]+(?:/[\w\./\-%\?=&#]*)?)', html)
    filtrados = []
    for link in encontrados:
        dominio = urlparse(link).netloc
        if not any(x in dominio for x in ENLACES_IRRELEVANTES):
            filtrados.append(link)
    return list(set(filtrados))

def seguir_redirecciones(url):
    url = limpiar_url(url)
    try:
        with requests.Session() as session:
            session.headers.update(HEADERS)
            response = session.head(url, allow_redirects=True, timeout=20)
            historia = [resp.url for resp in response.history]
            historia.append(response.url)

            final = historia[-1]

            if any(domain in final for domain in ACORTADORES_COMUNES):
                try:
                    response = session.get(final, timeout=20)
                    links_utiles = extraer_links_relevantes(response.text)
                    if links_utiles:
                        historia.append(links_utiles[0])
                except:
                    pass

            if any(domain in historia[-1] for domain in ACORTADORES_COMUNES):
                selenium_result = usar_selenium(historia[-1])
                if selenium_result and selenium_result != historia[-1]:
                    historia.append(selenium_result)

            return historia
    except requests.RequestException as e:
        return [f"{Fore.RED}Error: {e}"]

def procesar_url(url):
    print(f"{Fore.CYAN}🔗 Procesando: {url}")
    inicio = datetime.now()
    resultado = seguir_redirecciones(url)
    tiempo = (datetime.now() - inicio).total_seconds()

    for salto, link in enumerate(resultado, 1):
        color = Fore.GREEN if salto == len(resultado) else Fore.YELLOW
        print(f"  {color}[{salto}] {link}")

    if any(domain in resultado[-1] for domain in ACORTADORES_COMUNES):
        try:
            decision = input(f"{Fore.MAGENTA}[/] He detectado que el resultado es otra URL redirigente. ¿Quieres probar con esa URL? [yes/no]: ").lower()
            if decision in ('yes', 'y'):
                procesar_url(resultado[-1])
        except KeyboardInterrupt:
            print(f"\n{Fore.RED}Cancelado por el usuario.")

    print(f"{Style.DIM}⏱️ Tiempo total: {tiempo:.2f} segundos")
    print(Style.DIM + "─" * 60)

def procesar_lista(archivo):
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                url = linea.strip()
                if url and es_url_valida(url):
                    procesar_url(url)
                elif url:
                    print(f"{Fore.RED}❌ URL inválida: {url}")
    except FileNotFoundError:
        print(f"{Fore.RED}❌ Archivo no encontrado: {archivo}")

def es_url_valida(url):
    try:
        resultado = urlparse(url)
        return all([resultado.scheme in ("http", "https"), resultado.netloc])
    except:
        return False

def main():
    parser = argparse.ArgumentParser(
        description=f"{Fore.MAGENTA}🔍 Link Bypasser | Descubre el destino real de enlaces acortados"
    )
    parser.add_argument("-u", "--url", help="URL acortada a desenmascarar")
    parser.add_argument("-f", "--file", help="Archivo con múltiples URLs")
    args = parser.parse_args()

    if args.url:
        if es_url_valida(args.url):
            procesar_url(args.url)
        else:
            print(f"{Fore.RED}❌ URL inválida")

    elif args.file:
        procesar_lista(args.file)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
