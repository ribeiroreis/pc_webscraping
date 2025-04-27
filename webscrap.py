import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    
    # Configuração para ambiente CI
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--single-process")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_price(driver):
    try:
        # Seletor atualizado para o novo elemento
        price_selector = "div[class*='price_vista']"
        
        # Espera explícita combinada com verificação de conteúdo
        element = WebDriverWait(driver, 25).until(
            lambda d: d.find_element(By.CSS_SELECTOR, price_selector) if 
            d.find_element(By.CSS_SELECTOR, price_selector).text.strip() != "" else False
        )
        
        # Tratamento do texto com substituição de &nbsp;
        raw_price = element.text.replace("\u00a0", " ").strip()  # Converte &nbsp; para espaço
        price = raw_price.split("R$")[-1].strip()\
                          .replace(".", "")\
                          .replace(",", ".")
        print(f"Preço extraído: {price}")
        return price
        
    except Exception as e:
        print(f"Erro durante scraping:\n{str(e)}")
        driver.save_screenshot("error_screenshot.png")
        raise

def main():
    driver = setup_driver()
    try:
        driver.get("https://www.pichau.com.br/placa-de-video-gigabyte-radeon-rx-7600-xt-gaming-oc-16gb-gddr6-128-bit-gv-r76xtgaming-oc-16gd")
        time.sleep(3)  # Espera inicial para anti-bot
        
        price = get_price(driver)
        
        # Criar dataframe
        df = pd.DataFrame({
            "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            "price": [price]
        })
        
        # Salvar CSV
        os.makedirs("data", exist_ok=True)
        csv_filename = f"data/price_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Dados salvos em {csv_filename}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
