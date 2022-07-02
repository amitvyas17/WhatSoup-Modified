from selenium import webdriver
import time, csv
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common import exceptions
import sqlite3
import pandas as pd

location = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

driver_path = location + r'\\chromedriver.exe'

options = webdriver.ChromeOptions()
#options.add_argument(r"user-data-dir=E:\\Python\\Memory\\whatsapp")
driver = webdriver.Chrome( 'chromedriver.exe', options=options)

# Url to be located on
driver.get("https://web.whatsapp.com/")

# driver wait
wait = WebDriverWait(driver, 600)


def locate_chat(name):
    """Find the chat with a given name in WhatsApp web and
    click on that chat
    """
    time.sleep(12)
    try:
        x_arg = '//span[contains(text(), ' + '"' + name + '"' + ')]'
        element = wait.until(EC.element_to_be_clickable((By.XPATH, x_arg)))
        time.sleep(12)
        element.click()

    except exceptions.StaleElementReferenceException as e:
        print(e)


def scroll_to_top():
    time.sleep(2)
    # To store the parent's first childern (.firstElementChild -> js equivalent)
    arr = []

    # Scroll Untill we reach the top!
    while True:
        chato = driver.find_elements_by_class_name("_3ExzF")[0]
        arr.append(chato.text)

        js = '''
        var tl = document.querySelector("#main > div._2wjK5 > div > div");
        tl.firstElementChild.scrollIntoView();
        '''

        driver.execute_script(js)
        time.sleep(5)  # This delay is to let the whatsapp loads the chats.
        print(chato.text)
        loaded_chats = driver.find_elements_by_class_name("_3ExzF")[0]
        print(loaded_chats.text)
        if loaded_chats.text == arr[-1]:
            run_scrap_group()
            break
        else:
            continue


def js_method_scroll_to_top():
    ''' This method is to scroll to top using js code but it doesn't work as expected like
 the above method , i guess there is no better api to deal between JS and PYTHON codes in selenium '''

    time.sleep(13)
    js = '''
    var tl = document.querySelector("#main > div._2wjK5 > div > div");
var intervalId = window.setInterval(function(){
    if (tl.scrollTop === 0) {
    console.log('Reached the top!')
    clearInterval(intervalId)
    return "complete"

    } else {
        console.log("scrolling....");
        tl.firstElementChild.scrollIntoView();
    }
}, 5000);
    '''
    res = driver.execute_script(js)
    # res = driver.execute_script(js).equals("complete")  (Again where the glitch happenns with dynamic sites like whatsapp)
    while res == "complete":
        run_scrap_group()


# Empty lists to store results

l1 = []  # to store contact number
l2 = []  # to store message
l3 = []  # to store time stamp


def run_scrap_group():
    chats_text = driver.find_elements_by_class_name("_3ExzF")
    chats_timestamp = driver.find_elements_by_class_name("_17Osw")
    chats_number = driver.find_elements_by_class_name("ZJv7X")

    for i in chats_number:
        l1.append(i.text)
        print(i.text)

    for k in chats_text:
        l2.append(k.text)
        print(k.text)

    for j in chats_timestamp:
        l3.append(j.text)
        print(j.text)

    fields = ['Number', 'Message', 'Time-Stamp']
    filename = "chats.csv"

    with open(filename, 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)

        # Using zip() to deal parallely with the lists
        for t in zip(l1, l2, l3):
            print(t)
            csvwriter.writerow(list(t))


def run_scrap_contact():
    chats_text = driver.find_elements_by_class_name("_3ExzF")
    chats_timestamp = driver.find_elements_by_class_name("_17Osw")

    for k in chats_text:
        l2.append(k.text)
        print(k.text)

    for j in chats_timestamp:
        l3.append(j.text)
        print(j.text)

    fields = ['Number', 'Message', 'Time-Stamp']
    filename = "chats.csv"

    with open(filename, 'w', newline='') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)

        # Using zip() to deal parallely with the lists
        for t in zip(l2, l3):
            print(t)
            csvwriter.writerow(list(t))


def to_sqlite():
    # load data
    df = pd.read_csv('chats.csv', encoding="cp1252")
    df.columns = df.columns.str.strip()
    con = sqlite3.connect("chats_db.db")
    df.to_sql("Chats", con)
    con.close()
    print("Successfully completed..")


# saves to json file
def to_json():
    with open('chats.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        data_list = list()
        for row in reader:
            data_list.append(row)
    data = [dict(zip(data_list[0], row)) for row in data_list]
    data.pop(0)
    raw = json.dumps(data)

    with open("chats_json.json", 'w', encoding="utf-8") as f:
        f.write(raw)
    print(raw)

