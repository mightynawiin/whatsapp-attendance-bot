from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import math
import time

def get_attendance_data(reg_no, password):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    # options.add_argument('--headless')  # optional
    # options.add_argument('--disable-gpu')

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(3)

        driver.get("http://mitsims.in/")

        # Click Student link
        student_link = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "studentLink")))
        student_link.click()
        time.sleep(1)

        # Registration number
        regno_input = next((i for i in driver.find_elements(By.ID, "inputStuId") if i.is_displayed()), None)
        if regno_input is None:
            return None, "Login failed: Register No input not found."
        regno_input.clear()
        regno_input.send_keys(reg_no)

        # Password
        password_input = next((p for p in driver.find_elements(By.ID, "inputPassword") if p.is_displayed()), None)
        if password_input is None:
            return None, "Login failed: Password input not found."
        try:
            password_input.clear()
            password_input.send_keys(password)
        except Exception:
            # JS fallback
            js_script = f"""
                let input = document.getElementById('inputPassword');
                if (input) {{
                    input.value = '{password}';
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            """
            driver.execute_script(js_script)

        # Login button
        login_button = next((b for b in driver.find_elements(By.ID, "studentSubmitButton") if b.is_displayed()), None)
        if login_button is None:
            return None, "Login failed: Login button not found."
        login_button.click()

        # Wait for attendance dashboard
        semester_activity_div = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "semesterActivity"))
        )
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//fieldset[contains(., 'Note :') and contains(., 'Green :')]"))
        )

        # --- ADDITIONAL SLEEP TO LET DATA RENDER ---
        time.sleep(2)

        # Extract attendance table
        df = pd.DataFrame()
        headers = ["S.NO", "SUBJECT CODE", "CLASSES ATTENDED", "TOTAL CONDUCTED", "ATTENDANCE %"]

        rows_data = []
        all_fieldsets = semester_activity_div.find_elements(By.CSS_SELECTOR, "fieldset.x-fieldset")
        for data_fieldset in all_fieldsets[1:]:
            if "Note :" in data_fieldset.text and "Green :" in data_fieldset.text:
                continue
            row_cells = []
            cell_elements = data_fieldset.find_elements(By.CSS_SELECTOR, ".x-form-display-field span")
            for cell_element in cell_elements:
                cell_text = cell_element.get_attribute('innerText') or cell_element.get_attribute('textContent') or cell_element.text
                cleaned_text = cell_text.strip().replace('\xa0', '').replace('\u200b', '')
                row_cells.append(cleaned_text)
            if row_cells:
                rows_data.append(row_cells)

        if rows_data:
            temp_df = pd.DataFrame(rows_data, columns=headers)
            for col in ['S.NO', 'CLASSES ATTENDED', 'TOTAL CONDUCTED', 'ATTENDANCE %']:
                temp_df[col] = pd.to_numeric(temp_df[col], errors='coerce')
            temp_df.dropna(subset=['S.NO', 'CLASSES ATTENDED', 'TOTAL CONDUCTED', 'ATTENDANCE %'], inplace=True)
            return temp_df, None
        else:
            return None, "Attendance data extraction failed: No rows found."

    except (WebDriverException, TimeoutException, NoSuchElementException) as se_e:
        if driver:
            driver.save_screenshot("error_screenshot.png")
        return None, f"Browser automation error: {type(se_e).__name__}: {se_e}"
    except Exception as e:
        return None, f"Unexpected error: {type(e).__name__}: {e}"
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    # For testing
    attendance_df, error_message = get_attendance_data("23691a3294", "Password")
    if attendance_df is not None:
        print("Average Attendance:", round(attendance_df['ATTENDANCE %'].mean(), 2))
    else:
        print("Error:", error_message)
