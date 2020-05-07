from selenium import webdriver

#Selenium package includes several utilitities
# for waiting until things are ready
#https://selenium-python.readthedocs.io/waits.html
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
import time


driver = webdriver.Chrome()

#Allow the driver to poll the DOM for up to 10s when
# trying to find an element
driver.implicitly_wait(10)

#We might also want to explicitly define wait conditions
# on a particular element
wait = WebDriverWait(driver, 10)

# This is correct only if you followed the readme exactly,
# you may need to change this
driver.get("http://localhost:9000/")

def nbgallery_login(driver, wait, user, pwd):
    ''' Login to nbgallery.
        Return once the login dialogue has disappeared.
    '''
 
    driver.find_element_by_id("gearDropdown").click()
 
    element = driver.find_element_by_name("user[email]")
    element.click()
 
    element.clear()
    element.send_keys(user)
 
    element = driver.find_element_by_name("user[password]")
    element.clear()
    element.send_keys(pwd)
    element.click()
 
    driver.find_element_by_xpath("//input[@value='Login']").click()

def form_2(path, desc, tags, title=None, private=False):
    #Part 2
    element = driver.find_element_by_id("stageTitle")
    element.click()

    #Is there notebook metadata we can search for title?
    if not title:
        title = path.split('/')[-1].replace('.ipynb','')
    element.clear()
    element.send_keys(title)

    element = driver.find_element_by_id("stageDescription")
    element.click()

    #Is there notebook metadata we can search for description?
    #Any other notebook metadata we could make use of here?
    element.clear()
    #Description needs to be not null
    desc= 'No description.' if not desc else desc
    element.send_keys(desc)

    element = driver.find_element_by_id("stageTags-tokenfield")
    element.click()
    #time.sleep(1)

    #Handle various tagging styles
    #Is there notebook metadata we can search for tags?
    tags = '' if not tags else tags
    if isinstance(tags, list):
        tags=','.join(tags)
    tags = tags if tags.endswith(',') else tags+','

    element.clear()
    element.send_keys(tags) #need the final comma to set it?

    if private:
        driver.find_element_by_id("stagePrivate").click()

    driver.find_element_by_xpath('//*[@id="stageForm"]/div[9]/div/div/label/input').click()
    driver.find_element_by_id("stageSubmit").click()

    #https://blog.codeship.com/get-selenium-to-wait-for-page-load/
    #Wait for new page to load
    wait.until(EC.staleness_of(driver.find_element_by_tag_name('html')))


#path is full path to file
def form_1(path, desc, tags, title, private=False):
    if not path.endswith('.ipynb'):
        print('Not a notebook (.ipynb) file? [{}]'.format(path))

    element = wait.until(EC.element_to_be_clickable((By.ID, 'uploadModalButton')))
    element.click()

    driver.find_element_by_id("uploadFile").send_keys(path);
    driver.find_element_by_xpath('//*[@id="uploadFileForm"]/div[3]/div/div/label/input').click()
    driver.find_element_by_id("uploadFileSubmit").click()
    form_2(path, desc, tags, title, private=private)
    
def bulk_upload(username, password, path, tags, desc, titles):
    nbgallery_login(driver, 1000, username, password)
    time.sleep(2)
    for i, file_path in enumerate(Path(path).glob('**/*.ipynb')):
        tag = tags[i % len(tags)] # would remove mod in real application
        description = desc[i % len(desc)] # would remove mod in real application
        print(file_path)
        form_1(str(file_path),description, tag, None)
        time.sleep(1)

