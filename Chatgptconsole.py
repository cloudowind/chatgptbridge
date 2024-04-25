import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Yazım işlevi: Metni tek tek ekrana yazma
def type_message(text):
    for char in text:
        print(char, end='', flush=True)  # flush=True ile hemen ekrana bas
        time.sleep(0.02)  # Her harften sonra 0.02 saniye bekle
       # print("\n\n") 
# Önceki mesajları depolamak için bir liste oluşturalım
previous_messages = []

def get_all_elements(driver):
    # Tüm <p>, <code class> ve <li> öğelerini bulun
    elements = driver.find_elements(By.XPATH, "//p | //code[@class] | //li")

    # Bulunan öğelerin metin içeriğini alın ve ekrana yazın
    for element in elements:
        # Eğer öğe bir <p>, <code class> veya <li> ise
        if element.tag_name == "p" or element.tag_name == "code" or element.tag_name == "li":
            message = element.text
            # Eğer bu mesaj daha önce basılmadıysa ekrana yaz
            if message not in previous_messages:
                type_message(message + "\n")  # Yazım işlevini kullanarak ekrana yaz
                previous_messages.append(message)  # Mesajı önceki mesajlar listesine ekle
                print("\n\n") 
def main():
    # Firefox tarayıcısını başlat
    driver = webdriver.Firefox()

    # Web sitesine gidin
    driver.get('https://chat.openai.com/')

    # Mesaj gönderme işlemi için döngü oluşturun
    while True:
        # Kullanıcıdan bir mesaj alın
        message = input("type to send:: ")

        # Mesaj kutusunun yüklenmesini ve tıklanabilir olmasını bekleyin
        input_box = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'prompt-textarea')))
        # Mesaj kutusuna mesajı gönderin
        input_box.send_keys(message)
        input_box.send_keys(Keys.RETURN)

        

        # Biraz bekleyin (sayfanın güncellenmesini beklemek için)
        time.sleep(5)

        # "Stop generating" düğmesinin kaybolmasını bekleyin
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.XPATH, "//button[@aria-label='Stop generating']")))

        # Sayfadaki tüm <p>, <code class> ve <li> öğelerini alın ve ekrana yazın
        get_all_elements(driver)

        # Sonlandırma koşulu: Eğer "response is loading" metni sayfa kaynağında yoksa döngüyü devam ettir
        if "response is loading" not in driver.page_source:
            continue

if __name__ == "__main__":
    main()
