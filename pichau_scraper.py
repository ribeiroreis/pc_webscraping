

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

# Adicione estas linhas no início do script
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')

# Modifique as linhas de leitura/escrita de arquivos:
df_urls = pd.read_csv(os.path.join(BASE_DIR, '..', 'urls_pichau.csv'))
...
file_path = os.path.join(DATA_DIR, 'historico_precos.csv')
file_exists = os.path.isfile(file_path)
...
new_data.to_csv(file_path, ...)

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    
    # Removida configuração problemática
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Configuração do serviço
    service = Service(ChromeDriverManager().install())
    service.creationflags = 0x08000000  # Esconde a janela do console no Windows
    
    return webdriver.Chrome(service=service, options=options)

def get_price(driver, url):
    try:
        driver.get(url)
        
        # Espera mais robusta com verificação de conteúdo
        price_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'price_vista') and contains(text(), 'R$')]"))
        )
        
        # Processamento mais seguro do preço
        price_text = price_element.get_attribute("textContent").strip()
        price = float(
            price_text
            .replace('R$', '')
            .replace('\xa0', '')
            .replace('.', '')
            .replace(',', '.')
            .strip()
        )
        return price
        
    except Exception as e:
        print(f"Erro detalhado ao obter preço: {str(e)}")
        return None

def main():
    driver = setup_driver()
    try:
        df_urls = pd.read_csv(r'C:\workspace\projects\fbref\scripts\urls_pichau.csv')
        
        for index, row in df_urls.iterrows():
            peca = row['peca']
            url = row['url']
            
            print(f"\nIniciando verificação para: {peca}")
            
            # Tenta 3 vezes para cada URL
            for tentativa in range(1, 6):
                print(f"Tentativa {tentativa}/3")
                price = get_price(driver, url)
                if price:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    new_data = pd.DataFrame([[timestamp, peca, price]], 
                                          columns=['Data_Hora', 'Peca', 'Preco'])
                    
                    file_exists = os.path.isfile('historico_precos.csv')
                    
                    new_data.to_csv('historico_precos.csv', 
                                  mode='a', 
                                  header=not file_exists, 
                                  index=False,
                                  encoding='utf-8-sig')
                    
                    print(f"✅ Sucesso: {peca} - R$ {price:.2f}")
                    break
                else:
                    print(f"⚠️ Falha na tentativa {tentativa}")
                    time.sleep(5)
            else:
                print(f"❌ Falha final após 3 tentativas: {peca}")
            
            time.sleep(3)
            
    finally:
        driver.quit()

if __name__ == "__main__":
    # Configura logs do Chrome
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
    main()
