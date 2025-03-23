#imports and variables from utils file
from utils import *

def scrape_the_ocean():
    # Set up the WebDriver
    driver = get_driver()

    #we need data from coral raceway 1 and 2
    cora_raceway_nums = [1,2]
    for num in cora_raceway_nums:
        try:
            # Step 1: Open the Data Agreement page (login page)
            driver.get("https://data.b2.arizona.edu/Bio2OceanData/DataAgreement.jsp")
            print("step 1\n")
            # Step 2: Wait for login fields and enter credentials
            wait = WebDriverWait(driver, 10)  # Maximum 10 seconds wait
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
            password_field = driver.find_element(By.NAME, "password")

            username_field.send_keys(USERNAME)
            password_field.send_keys(PASSWORD)
            password_field.send_keys(Keys.RETURN)

            time.sleep(3)  # Wait for login to complete
            print("step 2\n")
            
            # Step 4
            dropdown = driver.find_element(By.NAME, "slopes")
            #this is where the array is used
            dropdown.send_keys("Coral Raceway "+str(num))
            
            #select all variables
            variable_dropdown = driver.find_element(By.NAME, "variablem")
            variable_dropdown_wrapped = Select(variable_dropdown)
            for option in variable_dropdown_wrapped.options:
                variable_dropdown_wrapped.select_by_value(option.get_attribute("value"))
            
            
            # Step 5: Click the "Get Data" button
            get_data_button = driver.find_element(By.XPATH, "//input[@value='Get Data']")
            get_data_button.click()
            time.sleep(2)
            print("step 5\n")
            # Step 6: Switch to the popup window
            main_window = driver.current_window_handle  # Store main window handle
            for handle in driver.window_handles:
                if handle != main_window:
                    driver.switch_to.window(handle)  # Switch to popup window
                    break
            print("step 6\n")
            # Step 7: Locate and download the CSV file (adjust selector as needed)
            csv_link = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, ".csv")))
            csv_link.click()
            print("CSV file download initiated.")

            # Step 8: Switch back to the main window (if needed)
            driver.switch_to.window(main_window)

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            time.sleep(5)  # Allow time for download

    driver.quit()
