import os
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
load_dotenv()
ACCOUNT_EMAIL = os.getenv("EMAIL")
ACCOUNT_PASSWORD = os.getenv("PASSWORD")
GYM_URL=os.getenv("URL")
def retry(func,retries,description):
    for i in range(retries):
        try:
            result=func()
            print(f"Succes {description}")
            return result
        except:
            print(f"Failed {description}, Try {i+1} / {retries}")
            time.sleep(2)
def log_in():
    driver.get(GYM_URL)
    log_in_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))
    log_in_button.click()
    email_form = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email-input")))
    email_form.send_keys(ACCOUNT_EMAIL)
    password_form = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password-input")))
    password_form.send_keys(ACCOUNT_PASSWORD)
    submit_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "submit-button")))
    submit_button.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "day-filter")))
def book_class():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "day-filter")))
    classes_list = driver.find_elements(By.CSS_SELECTOR, "p[id^='class-time']")
    already_checked_counter = 0
    new_booking_counter = 0
    waitilisting_counter = 0
    detailed_report = []
    for element in classes_list:
        wrapper_element = element.find_element(By.XPATH, "ancestor::div[@class='Schedule_dayGroup__y79__']")
        day_wrapper = wrapper_element.find_element(By.TAG_NAME, "h2").text
        if "Wed" in day_wrapper or "Fri" in day_wrapper:
            if "6:00 PM" in element.text:
                class_element = element.find_element(By.XPATH, "ancestor::div[starts-with(@id,'class-card')]")
                booking_button = class_element.find_element(By.TAG_NAME, "button")
                if booking_button.text == "Booked":
                    print(f"Already Booked: Spin Class on {day_wrapper} at {element.text}")
                    already_checked_counter += 1
                    detailed_report.append(f"Already Booked: {day_wrapper} at {element.text}")
                elif booking_button.text == "Waitlisted":
                    print(f"Already Waitlisted on {day_wrapper} at {element.text}")
                    already_checked_counter += 1
                    detailed_report.append(f"Already Waitlisted: {day_wrapper} at {element.text}")
                elif booking_button.text == "Join Waitlist":
                    booking_button.click()
                    WebDriverWait(driver, 10).until(lambda d: booking_button.text == "Waitlisted")
                    print(f"Joined Waitlist on {day_wrapper} at {element.text}")
                    waitilisting_counter += 1
                    detailed_report.append(f"Joined Waitlist: {day_wrapper} at {element.text}")
                else:
                    booking_button.click()
                    WebDriverWait(driver, 10).until(lambda d: booking_button.text == "Booked")
                    print(f"Succesfully Booked:Class on {day_wrapper} at {element.text}")
                    new_booking_counter += 1
                    detailed_report.append(f"Succesfully Booked: {day_wrapper} at {element.text}")
    total_proccessed = new_booking_counter + waitilisting_counter + already_checked_counter
    print(f"""Booking Summary
        Classes booked:{new_booking_counter}
        Waitlists Joined:{waitilisting_counter}
        Already Booked/waitlisted:{already_checked_counter}
        Total Wed and Fri classes proccessed:{total_proccessed} 
    """)
    return total_proccessed
def get_my_bookings():
    my_bookings = driver.find_element(By.ID, "my-bookings-link")
    my_bookings.click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "my-bookings-page")))
    time.sleep(1)
    list_with_booking = driver.find_elements(By.CSS_SELECTOR, ".MyBookings_bookingCard__VRdrR")
    number_of_bookings = 0
    # print("-----DETAILED CLASS LIST-----")
    # for i in detailed_report:
    #     print(i)
    print("Verifying on my booking page")
    for book in list_with_booking:
        day = book.find_element(By.XPATH, ".//p[strong[text()='When:']]").text
        if "Wed" in day or "Fri" in day:
            title_class = book.find_element(By.TAG_NAME, "h3").text
            print(f"Verified: {title_class}")
            number_of_bookings += 1
    return number_of_bookings
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
# Πρώτα φτιάχνεις τους κανόνες και το μονοπάτι του προφίλ
user_data_dir=os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)
retry(log_in,retries=7,description="Log in")

total=retry(book_class,7,"Booking class")

number_of_bookings=retry(get_my_bookings,7,"Geting my bookings")
print("----Verification Result----")
print(f"Expected: {total}")
print(f"Found: {number_of_bookings}")
if number_of_bookings==total:
    print("All Booking Verified!")
else:
    print(f"Not Verified! missing {number_of_bookings-total} bookings")