from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import platform

# Editable values
order_type = "long"  # Change to "short" to select the Short TP/SL checkbox
main_input_value = "10"  # Editable main input value (Quantity - USDT)
take_profit_value = "100"  # Editable Take Profit value
stop_loss_value = "50"  # Editable Stop Loss value

# Check if the user is on macOS or Windows
is_mac = platform.system() == "Darwin"

# Attach to the running Chrome session
chrome_options = webdriver.ChromeOptions()
chrome_options.debugger_address = "localhost:9222"
driver = webdriver.Chrome(options=chrome_options)


# Find the MEXC tab
mexc_tab = None
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if "mexc.com" in driver.current_url:
        mexc_tab = handle
        break

if mexc_tab:
    driver.switch_to.window(mexc_tab)
    time.sleep(3)

    try:
        wait = WebDriverWait(driver, 10)

        # Function to clear and type into an input field
        def clear_and_type(input_field, value):
            if is_mac:
                input_field.send_keys(Keys.COMMAND + "a")  # Select all (Mac)
            else:
                input_field.send_keys(Keys.CONTROL + "a")  # Select all (Windows)
            input_field.send_keys(Keys.BACKSPACE)  # Delete all text
            input_field.send_keys(value)

        # 1️⃣ Locate the first input field (Quantity - USDT) and type value
        main_input_container = wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "InputNumberHandle_inputNumberExtendV2Wrapper__Ns_8m")
        ))
        main_input = main_input_container.find_element(By.TAG_NAME, "input")
        clear_and_type(main_input, main_input_value)

        # 2️⃣ Find and check the corresponding checkbox based on order type (long or short)
        checkbox_label = wait.until(EC.presence_of_element_located(
            (By.XPATH, f"//label[contains(., '{order_type.capitalize()} TP/SL')]")
        ))
        checkbox = checkbox_label.find_element(By.XPATH, ".//input[@type='checkbox']")
        
        if not checkbox.is_selected():
            checkbox.click()
            print(f"✅ Checked the '{order_type.capitalize()} TP/SL' checkbox")

        # 3️⃣ Locate the Take Profit input and type the value
        take_profit_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//p[contains(text(), 'Take Profit')]/ancestor::div[contains(@class, 'component_titleWrapperNormal__l_Vch')]/following::input[@class='ant-input'][1]"
        )))
        clear_and_type(take_profit_input, take_profit_value)

        # 4️⃣ Locate the Stop Loss input and type the value
        stop_loss_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//p[contains(text(), 'Stop Loss')]/ancestor::div[contains(@class, 'component_titleWrapperNormal__l_Vch')]/following::input[@class='ant-input'][1]"
        )))
        clear_and_type(stop_loss_input, stop_loss_value)

        # 5️⃣ Click the correct order button based on trade type
        order_button_id = "contract-trade-open-long-btn" if order_type == "long" else "contract-trade-open-short-btn"
        order_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="{order_button_id}"]')))
        order_button.click()
        print(f"✅ Clicked '{order_type.capitalize()} Order' button")

    except Exception as e:
        print(f"Error: {e}")


