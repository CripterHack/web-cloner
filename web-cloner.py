import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from bs4 import BeautifulSoup
import os
import shutil
from urllib.parse import urlparse, urljoin

def fetch_and_clone_website(source_url, base_url):
    try:
        # Fetch the website content
        response = requests.get(source_url)
        response.raise_for_status()

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Modify the base URL
        base_tag = soup.new_tag('base', href=base_url)
        soup.head.insert(0, base_tag)

        # Create directory structure for the cloned site
        output_dir = 'cloned_site'
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)

        # Save the modified HTML content
        with open(os.path.join(output_dir, 'index.html'), 'w', encoding='utf-8') as file:
            file.write(str(soup))

        # Download and save all linked resources (CSS, JS, images)
        for tag in soup.find_all(['link', 'script', 'img']):
            if tag.name == 'link' and tag.get('href'):
                resource_url = urljoin(source_url, tag['href'])
                save_resource(resource_url, output_dir)
            elif tag.name == 'script' and tag.get('src'):
                resource_url = urljoin(source_url, tag['src'])
                save_resource(resource_url, output_dir)
            elif tag.name == 'img' and tag.get('src'):
                resource_url = urljoin(source_url, tag['src'])
                save_resource(resource_url, output_dir)

        # Zip the cloned site
        shutil.make_archive('cloned_site', 'zip', output_dir)

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def save_resource(resource_url, output_dir):
    try:
        response = requests.get(resource_url, stream=True)
        response.raise_for_status()

        parsed_url = urlparse(resource_url)
        resource_path = os.path.join(output_dir, parsed_url.path.lstrip('/'))

        os.makedirs(os.path.dirname(resource_path), exist_ok=True)
        with open(resource_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
    except Exception as e:
        print(f"Failed to save resource {resource_url}: {e}")

def clone_site():
    source_url = entry_url.get().strip()
    base_url = entry_base_url.get().strip()

    if not source_url or not base_url:
        messagebox.showerror("Error", "Both URL fields are required.")
        return

    if fetch_and_clone_website(source_url, base_url):
        messagebox.showinfo("Success", "The site has been cloned and saved as 'cloned_site.zip'.")
    else:
        messagebox.showerror("Error", "An error occurred while cloning the site.")

# Create the main window
root = tk.Tk()
root.title("Website Cloner")

# Create and place the URL input fields and labels
label_url = tk.Label(root, text="URL to clone:")
label_url.pack(pady=5)

entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

label_base_url = tk.Label(root, text="New base URL:")
label_base_url.pack(pady=5)

entry_base_url = tk.Entry(root, width=50)
entry_base_url.pack(pady=5)

# Create and place the Clone button
btn_clone = tk.Button(root, text="Clone Site", command=clone_site)
btn_clone.pack(pady=20)

# Run the main event loop
root.mainloop()
