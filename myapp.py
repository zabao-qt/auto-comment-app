from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.common.exceptions import UnexpectedAlertPresentException, NoSuchElementException
import time
import datetime

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        button = Button(text="Start", font_size=18)
        button.bind(on_press=self.run_selenium_to_comment)

        layout.add_widget(button)
        return layout

    def run_selenium_to_comment(self, instance):
        def log_error(message):
            try:
                # Create a unique log file name using a timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                log_file_name = f"error_log_{timestamp}.txt"

                # Get the absolute path to the directory of the current script
                script_directory = os.path.dirname(os.path.realpath(__file__))
                log_file_path = os.path.join(script_directory, log_file_name)

                with open(log_file_path, "w") as file:  # Use "w" to overwrite for each new log
                    file.write(f"{message}\n")
            except Exception as logging_error:
                # Handle potential errors within the logging process
                print(f"Error logging message: {logging_error}")

        try: 
            #test url
            url = ["http://fit.trianh.edu.vn/phong-thi-nghiem-an-toan-thong-tin/",  
                    "https://www.golfonline.sk/odborne-clanky/greenkeeping/plesen-snezna-a-plesen-snezna-siva/", 
                    "https://mru.home.pl/produkt/afriso-tm8-ir/#reviews",
                    "https://www.fivereasonssports.com/news/4-types-of-candy-most-adults-will-like/",
                    "https://www.lizsteel.com/a-new-favourite-teapot-to-sketch/",
                    "https://www.neobienetre.fr/forum-bien-etre-medecines-douces-developpement-personnel/topic/play-game-for-fun/",
                    "https://bulevard.bg/interviews/ivaylo-zahariev-v-ekskluzivno-intervyu-19.html",
                    "https://www.thelowdownblog.com/2018/03/riding-in-smartphone-powered-self.html"]

            content = "Chúng tôi là chuyên gia hàng đầu trong lĩnh vực SEO, Thiết kế Website và Marketing......."
            email = "admin@homenest.com.vn"
            phone = "https://homenest.com.vn/ve-chung-toi/"
            author = "HomeNest"

            #path to chromedriver
            script_directory = os.path.dirname(os.path.realpath(__file__))
            chromedriver_path = os.path.join(script_directory, "chromedriver.exe")

            # Initialize the Chrome WebDriver 
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.sensors": 2})
            chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--accept_insecure_certs")
            chrome_options.add_argument("--allow-running-insecure-content")
            chrome_options.add_argument("--allow-insecure-localhost")
            chrome_options.add_argument("--ignore-certificate-errors")
            driver = webdriver.Chrome(options=chrome_options)

            for(url) in url:
                try:    
                    driver.get(url)
                    wait = WebDriverWait(driver, 1)
        
                    # Define selectors
                    selectors = {
                        "comment": ["textarea[name='comment']", "textarea", "input[type='text'][name='comment']", "input[type='text']", "input[name='comment']"],
                        "author": ["input[type='text'][name='author']", "input[type='text']", "input[name='author']"],
                        "email": ["input[type='text'][name='email']", "input[type='email']", "input[name='email']"],
                        "phone": [ "input[type='text'][name='url']","input[type='text']", "input[name='url']"],
                        "submit": ["input[type='submit'][name='submit']", "input[type='submit']", "input[name='submit']"]
                    }

                    # Function to find element by selectors
                    def find_element_by_selectors(selectors):
                        for selector in selectors:
                            try:
                                element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                                if element:
                                    print(f"Found element with selector: {selector}")
                                    return element
                            except Exception as e:
                                print(f"Could not find element with selector: {selector} on page: {driver.current_url}. Error: {e}")

                    # Find elements
                    comment_field = find_element_by_selectors(selectors['comment'])
                    author_field = find_element_by_selectors(selectors['author'])
                    email_field = find_element_by_selectors(selectors['email'])
                    phone_field = find_element_by_selectors(selectors['phone'])
                    submit_button = find_element_by_selectors(selectors['submit'])

                    if not all([comment_field, author_field, email_field, phone_field, submit_button]):
                        log_error(f"One or more fields were not found on page: {driver.current_url}")
                        continue
                    else: 
                        # Enter credentials and submit
                        comment_field.send_keys(content)
                        email_field.send_keys(email)
                        phone_field.send_keys(phone)
                        author_field.send_keys(author)

                        # Scroll to the submit button and click it
                        driver.execute_script("arguments[0].scrollIntoView(true);", comment_field)
                        time.sleep(1)  # Adding delay to ensure the element is ready for interaction
                        submit_button.click()
                        time.sleep(2)
                except UnexpectedAlertPresentException:
                    log_error(f"Unexpected alert encountered on URL {url}")
                    continue  # Move to the next URL after handling the alert
                
                except Exception as e:
                    log_error(f"An error occurred while trying to comment on URL {url}: {e}")
   
        except Exception as e:
            print(f"An error occurred while logging in: {e}")


    
if __name__ == "__main__":
    MyApp().run()