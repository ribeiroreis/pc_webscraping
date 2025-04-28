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
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")
    
    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option("useAutomationExtension", False)
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def get_price(driver, url):
    try:
        driver.get(url)
        price_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'price_vista') and contains(text(), 'R$')]"))
        )
        
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
        print(f"Erro ao obter preço: {str(e)}")
        return None

def main():
    # Configura caminhos dos arquivos
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    urls_path = os.path.join(base_dir, 'urls_pichau.csv')
    data_path = os.path.join(base_dir, 'data', 'historico_precos.csv')
    
    # Cria diretório data se não existir
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    
    driver = setup_driver()
    try:
        df_urls = pd.read_csv(urls_path)
        
        for index, row in df_urls.iterrows():
            peca = row['peca']
            url = row['url']
            
            print(f"\nIniciando verificação para: {peca}")
            
            for tentativa in range(1, 4):
                print(f"Tentativa {tentativa}/3")
                price = get_price(driver, url)
                if price:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    new_data = pd.DataFrame([[timestamp, peca, price]], 
                                          columns=['Data_Hora', 'Peca', 'Preco'])
                    
                    file_exists = os.path.isfile(data_path)
                    
                    new_data.to_csv(data_path, 
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
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
    main()
