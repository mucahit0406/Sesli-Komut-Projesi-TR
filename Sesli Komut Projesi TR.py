import os
import sys
import subprocess
import random
import speech_recognition as sr # pip install SpeechRecognition
from selenium import webdriver # pip install selenium
from selenium.webdriver.common.keys import Keys
import asyncio 
import pyautogui # pip install pyautogui
from selenium.webdriver.common.by import By
from gtts import gTTS # pip install gTTS
from playsound import playsound # pip install playsound
from fuzzywuzzy import fuzz # pip install fuzzywuzzy

class sesliasistan():
    def seslendirme(self, metin):
        xtts = gTTS(text=metin, lang="tr")
        dosya = "dosya" + str(random.randint(0, 123412341234)) + ".mp3"
        xtts.save(dosya)
        playsound(dosya)
        os.remove(dosya)

asistan = sesliasistan()

async def recognize_speech_async():
    r = sr.Recognizer()
    loop = asyncio.get_event_loop()

    with sr.Microphone() as source:
        print("Sesli komut bekleniyor...")
        audio = await loop.run_in_executor(None, r.listen, source)

        try:
            command = await loop.run_in_executor(None, lambda: r.recognize_google(audio, language="tr-TR"))
            print("Algılanan komut:", command)
            return command.lower()
        except sr.UnknownValueError:
            print("Anlaşılamayan bir ses")
            return ""
        except sr.RequestError as e:
            print("İnternete bağlanılamıyor; {0}".format(e))
            return ""

async def hava_durumu_sehir():
    asistan.seslendirme("Hangi şehrin hava durumunu istersiniz?")
    command = await recognize_speech_async()
    print(f"Hava durumu komutu alındı: {command}")
    if command:
        driver = webdriver.Chrome()
        url = f"https://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?il={command}"
        driver.get(url)
        asistan.seslendirme(f"{command} için hava durumu tahmini açıldı.")



async def open_kisayol(path, name):
    os.system(r'start "" "{}"'.format(path))
    asistan.seslendirme(f"{name} açılıyor")

async def open_youtube(search_query):
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com/")
    driver.set_page_load_timeout(10)

    search_box = driver.find_element("name", "search_query")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    driver.set_page_load_timeout(10)

    while True:
        command = await recognize_speech_async()
        if "pencereyi kapat" in command:
            driver.quit()
            asistan.seslendirme("Tarayıcı kapatılıyor")
            break
        elif "aşağı in" in command:
            pyautogui.press('pagedown')
            asistan.seslendirme("Aşağı iniliyor")
        elif "ilk sıradaki videoya tıkla" in command:
            ilk_video = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/ytd-thumbnail/a/yt-image/img")
            ilk_video.click()
            asistan.seslendirme("Videoya tıkladım")
        elif "2 sıradaki videoya tıkla" in command:
            ikinci_video = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[2]/div[1]/ytd-thumbnail/a/yt-image/img")
            ikinci_video.click()
            asistan.seslendirme("İkinci sıradaki videoya tıklanıyor")
        elif "3 sıradaki videoya tıkla" in command:
            üçüncü_video = driver.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[3]/div[1]/ytd-thumbnail/a/yt-image/img")
            üçüncü_video.click()
            asistan.seslendirme("Üçüncü sıradaki videoya tıklanıyor")

commands = {
    "bip'i aç": ("sizin dosya yolunuz", "BiP"),
    "spotify'ı aç": ("#dosya yolunu buraya belirtin", "Spotify"),#Dosya yollarınızı kendi bilgisayarınızdan ekleyin
    "excel'i aç": ("#", "Excel"),
    "word'u aç": ("#", "Word"),
    "discord'u aç": ("", "Discord"),
    "chrome'u aç": ("", "Google Chrome"),
    "brave'i aç": ("", "Brave"),
    "ddrace network'ü aç": ("", "DDrace Network"),
    "epic games launcher'ı aç": ("", "Epic Games Launcher"),
    "firefox'u aç": ("", "Firefox"),
    "pubg'yi aç": ("", "PUBG MOBİLE"),
    "operayı aç": ("", "Opera GX"),
    "powerpoint'i aç": ("", "PowerPoint"),
    "robloxu aç": ("", "Roblox Studio"),
    "steam'i aç": ("", "Steam"),
    "vizyon stüdyoyu aç": ("", "Visual Studio 2022"),
    "whatsapp'ı aç": ("", "WhatsApp"),
    "zoom'u aç": ("", "Zoom Workspace")

}

direct_commands = {
    "youtube'yi aç": "youtube_open",
    "youtube'da ara": "youtube_search",
}

async def handle_direct_commands(command):
    if "youtube'yi aç" in command:
        asistan.seslendirme("YouTube açılıyor")
        await open_youtube("")
    elif "youtube'da ara" in command:
        search_query = command.replace("youtube'da ara", "").strip()
        asistan.seslendirme(f"YouTube'da aranıyor: {search_query}")
        await open_youtube(search_query)

async def main():
        # Program her başlatıldığında sesli mesaj gönder
        asistan.seslendirme("Monster hazır")

        while True:
            try:
                while True:
                    print("Tetikleyici bekleniyor: 'Hey Monster'")
                    command = await recognize_speech_async()

                    if "hey monster" in command:
                        asistan.seslendirme("Sizi dinliyorum")
                        print("Komut bekleniyor...")
                        command = await recognize_speech_async()

                        # "Monster kendini yeniden başlat" komutunu kontrol et
                        if "monster kendini yeniden başlat" in command:
                            asistan.seslendirme("Sistem yeniden başlatılıyor.")
                            return  # Programın kalanını sonlandır
                        if "hava durumu" in command or  "bugünki hava durumu" in command or "bugünkü hava durumu" in command:
                            await hava_durumu_sehir()
                        # Direkt komutları kontrol et
                        if any(direct_command in command for direct_command in direct_commands):
                            await handle_direct_commands(command)
                            continue

                        # Komutun benzerlik oranını kontrol et
                        all_commands = list(commands.keys())
                        best_match = max(all_commands, key=lambda x: fuzz.ratio(command, x))
                        best_ratio = fuzz.ratio(command, best_match)
                        print(f"Best match: {best_match} ({best_ratio}%)")

                        if best_ratio > 70:  # %70 benzerlik oranını eşik olarak belirliyoruz
                            if best_match in commands:
                                await open_kisayol(*commands[best_match])
                        else:
                            print("Anlaşılamayan komut:", command)
                            asistan.seslendirme("Anlaşılmayan komut")
                    else:
                        print("Tetikleyici algılanmadı.")
            except Exception as e:
                print(f"Hata: {e}")
                asistan.seslendirme("Bir hata oluştu, sistem tekrar başlatılıyor.")
                # Hata oluştuğunda döngüyü başa al
                continue


if __name__ == "__main__":
    asyncio.run(main())
