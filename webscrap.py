import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os

# Configurar o Chrome no modo headless
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

# Iniciar o driver
driver = webdriver.Chrome(options=options)


# URL do produto
url = "https://www.pichau.com.br/placa-de-video-gigabyte-radeon-rx-7600-xt-gaming-oc-16gb-gddr6-128-bit-gv-r76xtgaming-oc-16gd?gad_source=1&gclid=CjwKCAjwq7fABhB2EiwAwk-YbHKPu2eP6MOxnn_AytWtx8r9Rt6YmYykZ3CJqHlnV4PF9xeKjW19qRoCrHsQAvD_BwE"
driver.get(url)

# Localizar o preço na página
try:
    price_xpath = "/html/body/div[2]/div/div[2]/div[4]/div[1]/div/div[1]/div[2]/div[2]"
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
    
    price_element = driver.find_element(By.XPATH, price_xpath)
    price = price_element.text.strip()
    print(f"Preço encontrado: {price}")

    # Capturar o timestamp atual
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Criar pasta output se não existir
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Caminho do arquivo CSV
    file_path = f"{output_dir}/historico.csv"

    # Criar um DataFrame com os novos dados
    new_data = pd.DataFrame({'timestamp': [timestamp], 'price': [price]})

    # Se o arquivo já existir, adicionar sem sobrescrever
    if os.path.exists(file_path):
        new_data.to_csv(file_path, mode='a', header=False, index=False, encoding='utf-8-sig')
    else:
        new_data.to_csv(file_path, mode='w', header=True, index=False, encoding='utf-8-sig')

    print(f"Dados salvos em {file_path}")

except Exception as e:
    print(f"Erro ao encontrar o preço: {e}")

# Fechar o navegador
driver.quit()
