
from selenium.webdriver.common.by import By
from string import ascii_letters
from random import choice
from selenium_driver import chrome_driver
from time import sleep, time
from copy import copy

def login_tests(url):
    credentials = {"email":random_string(5)+"@"+random_string(5),
                   "password":random_string(64),
                   "secret":random_string(64),
                   "fruit":random_string(10)}
    credentials["repeat_password"] = credentials["password"]
    sign_up = test_sign_up(url,credentials)
    sign_in = test_sign_in(url,credentials)
    for test_name,test_result in sign_up.items():
        print(test_name,":",test_result)
    for test_name,test_result in sign_in.items():
        print(test_name,":",test_result)

def test_sign_in(url,credentials):
    results = {}
    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signin_email_input", credentials["email"])
    driver.find_and_send(By.ID, "signin_password_input", credentials["password"])
    driver.find_and_send(By.ID, "signin_secret_input", credentials["secret"])
    driver.find_and_click(By.ID, "signin_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"home").strip() == "Welcome to the login screen."
        assert start_time+1.0 < time() < start_time+3.0
        results["signin_regular"] = True
    except AssertionError:
        results["signin_regular"] = False
    driver.close()

    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signin_email_input", credentials["email"].replace("@","a"))
    driver.find_and_send(By.ID, "signin_password_input", credentials["password"])
    driver.find_and_send(By.ID, "signin_secret_input", credentials["secret"])
    driver.find_and_click(By.ID, "signin_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"status_msg_text").strip() != "Successfully signed up."
        assert time() < start_time+0.5
        results["signin_bad_email"] = True
    except AssertionError:
        results["signin_bad_email"] = False
    driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()

    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signin_email_input", credentials["email"])
    driver.find_and_send(By.ID, "signin_password_input", credentials["password"][:9])
    driver.find_and_send(By.ID, "signin_secret_input", credentials["secret"])
    driver.find_and_click(By.ID, "signin_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"status_msg_text").strip() != "Successfully signed up."
        assert time() < start_time+0.5
        results["signin_short_password"] = True
    except AssertionError:
        results["signin_short_password"] = False
    driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()

    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signin_email_input", credentials["email"])
    driver.find_and_send(By.ID, "signin_password_input", credentials["password"]+"extra")
    driver.find_and_send(By.ID, "signin_secret_input", credentials["secret"])
    driver.find_and_click(By.ID, "signin_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"status_msg_text").strip() != "Successfully signed up."
        assert start_time+1.0 < time() < start_time+3.0
        results["signin_wrong_password"] = True
    except AssertionError:
        results["signin_wrong_password"] = False
    driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()
    return results

def test_sign_up(url,credentials):
    results = {}
    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signup_email_input", credentials["email"])
    driver.find_and_send(By.ID, "signup_password_input", credentials["password"])
    driver.find_and_send(By.ID, "signup_repeat_password_input", credentials["repeat_password"])
    driver.find_and_send(By.ID, "signup_secret_input", credentials["secret"])
    driver.find_and_send(By.ID, "signup_fruit_input", credentials["fruit"])
    driver.find_and_click(By.ID, "signup_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"status_msg_text").strip() == "Successfully signed up."
        assert start_time+1.0 < time() < start_time+3.0
        results["signup_regular"] = True
    except AssertionError:
        results["signup_regular"] = False
    driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()

    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signup_email_input", credentials["email"])
    driver.find_and_send(By.ID, "signup_password_input", credentials["password"])
    driver.find_and_send(By.ID, "signup_repeat_password_input", credentials["repeat_password"])
    driver.find_and_send(By.ID, "signup_secret_input", credentials["secret"])
    driver.find_and_send(By.ID, "signup_fruit_input", credentials["fruit"])
    driver.find_and_click(By.ID, "signup_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"status_msg_text").strip() == "Successfully signed up."
        assert start_time+1.0 < time() < start_time+3.0
        results["signup_duplicate"] = True
    except AssertionError:
        results["signup_duplicate"] = False
    driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()

    results["signup_empty_field"] = True
    for key in credentials:
        temp_credentials = copy(credentials)
        temp_credentials[key] = ""
        driver = chrome_driver(url)
        driver.find_and_send(By.ID, "signup_email_input", temp_credentials["email"])
        driver.find_and_send(By.ID, "signup_password_input", temp_credentials["password"])
        driver.find_and_send(By.ID, "signup_repeat_password_input", temp_credentials["repeat_password"])
        driver.find_and_send(By.ID, "signup_secret_input", temp_credentials["secret"])
        driver.find_and_send(By.ID, "signup_fruit_input", temp_credentials["fruit"])
        driver.find_and_click(By.ID, "signup_button")
        start_time = time()
        try:
            if key == "fruit":
                assert driver.get_inner_html(By.ID,"status_msg_text").strip() == "Successfully signed up."
                assert start_time+1.0 < time() < start_time+3.0
            else:
                assert driver.get_inner_html(By.ID,"status_msg_text").strip() != "Successfully signed up."
                assert time() < start_time+0.5
        except AssertionError:
            results["signup_empty_field"] = False
            break
        driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()

    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signup_email_input", credentials["email"])
    driver.find_and_send(By.ID, "signup_password_input", credentials["password"])
    driver.find_and_send(By.ID, "signup_repeat_password_input", credentials["repeat_password"]+"extra")
    driver.find_and_send(By.ID, "signup_secret_input", credentials["secret"])
    driver.find_and_send(By.ID, "signup_fruit_input", credentials["fruit"])
    driver.find_and_click(By.ID, "signup_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"status_msg_text").strip() != "Successfully signed up."
        assert time() < start_time+0.5
        results["signup_wrong_repeatpassword"] = True
    except AssertionError:
        results["signup_wrong_repeatpassword"] = False
    driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()

    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signup_email_input", credentials["email"].replace("@","a"))
    driver.find_and_send(By.ID, "signup_password_input", credentials["password"])
    driver.find_and_send(By.ID, "signup_repeat_password_input", credentials["repeat_password"])
    driver.find_and_send(By.ID, "signup_secret_input", credentials["secret"])
    driver.find_and_send(By.ID, "signup_fruit_input", credentials["fruit"])
    driver.find_and_click(By.ID, "signup_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"status_msg_text").strip() != "Successfully signed up."
        assert time() < start_time+0.5
        results["signup_bad_email"] = True
    except AssertionError:
        results["signup_bad_email"] = False
    driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()

    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signup_email_input", credentials["email"])
    driver.find_and_send(By.ID, "signup_password_input", credentials["password"][:9])
    driver.find_and_send(By.ID, "signup_repeat_password_input", credentials["repeat_password"][:9])
    driver.find_and_send(By.ID, "signup_secret_input", credentials["secret"])
    driver.find_and_send(By.ID, "signup_fruit_input", credentials["fruit"])
    driver.find_and_click(By.ID, "signup_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"status_msg_text").strip() != "Successfully signed up."
        assert time() < start_time+0.5
        results["signup_short_password"] = True
    except AssertionError:
        results["signup_short_password"] = False
    driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()

    driver = chrome_driver(url)
    driver.find_and_send(By.ID, "signup_email_input", credentials["email"])
    driver.find_and_send(By.ID, "signup_password_input", credentials["password"])
    driver.find_and_send(By.ID, "signup_repeat_password_input", credentials["repeat_password"])
    driver.find_and_send(By.ID, "signup_secret_input", credentials["secret"][:9])
    driver.find_and_send(By.ID, "signup_fruit_input", credentials["fruit"])
    driver.find_and_click(By.ID, "signup_button")
    start_time = time()
    try:
        assert driver.get_inner_html(By.ID,"status_msg_text").strip() != "Successfully signed up."
        assert time() < start_time+0.5
        results["signup_short_secret"] = True
    except AssertionError:
        results["signup_short_secret"] = False
    driver.find_and_click(By.ID, "status_msg_ack")
    driver.close()
    return results

def random_string(length):
    return "".join([choice(ascii_letters) for _ in range(length)])

