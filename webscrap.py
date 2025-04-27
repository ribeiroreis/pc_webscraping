import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os

# Iniciar o navegador Chrome com opções para CI
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # headless compatível com layout moderno
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Acesse a página
url = "https://www.pichau.com.br/placa-de-video-gigabyte-radeon-rx-7600-xt-gaming-oc-16gb-gddr6-128-bit-gv-r76xtgaming-oc-16gd?gad_source=1&gclid=CjwKCAjwq7fABhB2EiwAwk-YbHKPu2eP6MOxnn_AytWtx8r9Rt6YmYykZ3CJqHlnV4PF9xeKjW19qRoCrHsQAvD_BwE"
driver.get(url)

# Espera explícita para garantir que o elemento esteja visível
try:
    price_xpath = "/html/body/div[2]/div/div[2]/div[4]/div[1]/div/div[1]/div[2]/div[2]"
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, price_xpath))
    )
    
    price_element = driver.find_element(By.XPATH, price_xpath)
    price = price_element.text
    print(f"Preço encontrado: {price}")

    # Capturar o timestamp atual
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Criar um DataFrame
    df = pd.DataFrame({
        'timestamp': [timestamp],
        'price': [price]
    })

    # Criar diretório de saída se não existir
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Gerar o nome do arquivo com timestamp
    filename = f"{output_dir}/preco_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Salvar o CSV
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Arquivo salvo: {filename}")

except Exception as e:
    print(f"Erro ao encontrar o preço: {e}")

# Fecha o navegador
driver.quit()
