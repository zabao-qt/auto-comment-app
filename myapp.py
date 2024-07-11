from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from selenium import webdriver 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time


class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        button = Button(text="Start", font_size=18)
        button.bind(on_press=self.run_selenium_to_comment)

        layout.add_widget(button)
        return layout

    def run_selenium_to_comment(self, instance):
        def log_error(message):
            with open("error_log.txt", "a") as file:
                file.write(f"{message}\n")

        try: 
            #test url
            url = [
                    "http://fit.trianh.edu.vn/phong-thi-nghiem-an-toan-thong-tin/", 
                    "https://mru.home.pl/produkt/afriso-tm8-ir/#reviews"]

            content = "HomeNest vip pro"
            email = "admin@homenest.com.vn."
            phone = "admin@homenest.com.vn."
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
                    wait = WebDriverWait(driver, 10)
        
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
         
                        submit_button.click()
                        
                        # Wait for the URL to change after submission
                        time.sleep(5)

                        if driver.current_url == url:
                                time.sleep(10)
                                continue
                        
                except EC.UnexpectedAlertPresentException as alert_ex:
                    alert_text = driver.switch_to.alert.text
                    log_error(f"Unexpected alert encountered on URL {url}: {alert_text}")
                    continue  # Move to the next URL after handling the alert

   
        except Exception as e:
            print(f"An error occurred while logging in: {e}")
        
        finally:
            driver.quit()


    def run_selenium_to_login(self, instance):

        #this is just for test login function
        try: 
            #test url
            url = ["https://vocal.media/signin?successRedirect=", 
                   "https://blendermarket.com/login"]
 
            username = "thienthanbongtoi1210@gmail.com"
            password1 = "vinh12345678"
            password2 = "Vinh12345678"

            data_user = [
            {"username": "thienthanbongtoi1210@gmail.com", "password": "vinh12345678"},
            {"username": "thienthanbongtoi1210@gmail.com", "password": "Vinh12345678"}
            ]
            

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
            for user in data_user:
                for(url) in url:
                    
                        driver.get(url)
                        wait = WebDriverWait(driver, 10)
                        username_selectors = [
                            "input[type='text'][name='email']",
                            "input[type='email']",
                            "input[name='email']",
                            "input[name='username']"
                        ]
                        password_selectors = [
                            "input[type='password'][name='password']",
                            "input[type='password']",
                            "input[name='password']"
                        ]
                        login_button_selectors = [
                            "button[type='submit']",
                            "input[type='submit']",
                            "button[type='button']"
                        ]

                        username_field = None
                        for selector in username_selectors:
                            try:
                                username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                                if username_field:
                                    break
                            except:
                                print("Username field not found")
                                continue

                        password_field = None
                        for selector in password_selectors:
                            try:
                                password_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                                if password_field:
                                    break
                            except:
                                print("Password field not found")
                                continue

                        login_button = None
                        for selector in login_button_selectors:
                            try:
                                login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                                if login_button:
                                    break
                            except:
                                print("Login button not found")
                                continue

                        if username_field and password_field and login_button:
                            # Enter credentials and submit
                            username_field.send_keys(user["username"])
                            password_field.send_keys(user["password"])
                            login_button.click()

                            # Wait for the URL to change after login
                            wait.until(EC.url_changes(url))

                            # Check if login was successful by verifying the URL has changed
                            if driver.current_url != url:
                                print(f"Login successful for {user['username']} on {url}")
                                continue
                            elif driver.current_url == url:
                                print(f"Login failed for {user['username']} on {url}")
                                continue
                            else:
                                print(f"Login failed for {user['username']} on {url}")
                                continue


                    #driver.quit()
        except Exception as e:
            print(f"An error occurred while logging in: {e}")
        

if __name__ == "__main__":
    MyApp().run()
