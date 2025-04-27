import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import os

# Iniciar o navegador Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Acesse a página
url = "https://www.pichau.com.br/placa-de-video-gigabyte-radeon-rx-7600-xt-gaming-oc-16gb-gddr6-128-bit-gv-r76xtgaming-oc-16gd"
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
except Exception as e:
    print(f"Erro ao encontrar o preço: {e}")
    price = None

# Fecha o navegador
driver.quit()

# Criar um dataframe com data/hora e preço
data = {
    "timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    "price": [price]
}
df = pd.DataFrame(data)

# Garantir que a pasta data/ existe
os.makedirs("data", exist_ok=True)

# Salvar CSV com timestamp
timestamp_now = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"data/price_{timestamp_now}.csv"
df.to_csv(csv_filename, index=False)

print(f"Arquivo salvo em {csv_filename}")
