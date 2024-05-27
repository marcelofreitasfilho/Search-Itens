import time
import re
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By

def find_prices(term, text_widget):
    # Open the browser
    chrome = webdriver.Chrome()
    chrome.get('https://www.google.com.br/?hl=pt-BR')
    
    # Select html attributes
    search_bar = chrome.find_element(By.NAME, 'q')
    search_button = chrome.find_element(By.XPATH, '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[4]/center/input[1]')
    
    # Interact with the elements, by clearing, sending keys and clicking
    search_bar.clear()
    search_bar.send_keys(term)
    search_button.click()
    
    # Wait for the page to load
    time.sleep(10)
    
    # Loop through the results cards
    cards = chrome.find_elements(By.XPATH, "//*[contains(@class, 'clickable-card')]")
    
    # Clear the text widget before displaying new results
    text_widget.delete(1.0, tk.END)
    
    # Iterate through the cards and extract the title, price, store and link
    for card in cards:
        total = card.get_attribute('aria-label')
        link = card.get_attribute('href')
        my_split = r'\b(?:por|de)\b'
        splited_value = re.split(my_split, total)
        my_return = [x.strip() for x in splited_value]
        
        if len(my_return) >= 3:
            title = my_return[0]
            price = my_return[1].replace('\\xa', '')
            store = my_return[2]
            
            # Display the result in the text widget
            text_widget.insert(tk.END, f'Title: {title}\nPrice: {price}\nStore: {store}\nLink: {link}\n\n')
    
    # Quit the browser
    chrome.quit()

# Create the GUI
root = tk.Tk()
root.title('Search Prices')
root.geometry('500x400')

# Creating labels, entry and button widgets

# Label widget to display the search term
link_label = tk.Label(root, text='Search Term:')
link_label.config(width=50)
link_label.pack()

# Entry widget to get the search term
link_entry = tk.Entry(root)
link_entry.config(width=50)
link_entry.pack()

# Widget to display results
results_text = tk.Text(root, wrap=tk.WORD, height=15, width=50)
results_text.pack()

# Button widget to trigger the search
search_button = tk.Button(root, text='Search', command=lambda: find_prices(link_entry.get(), results_text))
search_button.pack()

root.mainloop()
