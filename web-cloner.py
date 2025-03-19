import tkinter as tk
from tkinter import filedialog, messagebox, IntVar, Checkbutton, ttk
import requests
from bs4 import BeautifulSoup
import os
import shutil
import mimetypes
import re
import threading
from urllib.parse import urlparse, urljoin, unquote
import time
import customtkinter as ctk
import webbrowser

# Control variables for pause and cancel
PAUSED = False
CANCELLED = False

# Initial CustomTkinter configuration
ctk.set_appearance_mode("dark")  # Start in dark mode
ctk.set_default_color_theme("blue")  # Base themes: blue, dark-blue, green

# Custom colors for dark mode (cyberpunk style)
DARK_COLORS = {
    "fg_color": "#121212",        # Dark main background
    "text_color": "#E0FFFF",      # Lighter cyan text for better readability
    "button_color": "#9400D3",    # Darker purple buttons for better contrast
    "button_text_color": "#FFFFFF", # White button text for maximum readability
    "progress_color": "#00DD00",  # Slightly adjusted neon green progress bar
    "accent_color": "#FF00FF",    # Magenta accent color
    "hover_color": "#B026FF",     # Brighter purple hover color
    "border_color": "#00CCCC",    # Slightly darker cyan borders
    "entry_bg_color": "#1E1E1E",  # Background color for input fields
    "checkbox_color": "#00CCCC"   # Color for checkboxes
}

# Custom colors for light mode (paper and green)
LIGHT_COLORS = {
    "fg_color": "#F5F5F5",        # Paper background color
    "text_color": "#005533",      # Dark green text, darker for better contrast
    "button_color": "#3D9140",    # Forest green buttons for better contrast
    "button_text_color": "#FFFFFF", # White button text for maximum readability
    "progress_color": "#4CAF50",  # More defined green progress bar
    "accent_color": "#007E68",    # More intense teal accent color
    "hover_color": "#2E7D32",     # Dark green hover color for better feedback
    "border_color": "#2E7D32",    # Dark green borders
    "entry_bg_color": "#FFFFFF",  # Background color for input fields
    "checkbox_color": "#4CAF50"   # Color for checkboxes
}

# Variable for current theme control
current_theme = "dark"

# Translation dictionaries
translations = {
    'en': {
        'title': 'Website Cloner',
        'window_title': 'Website Cloner',
        'url_label': 'URL to clone:',
        'url_placeholder': 'Enter the URL of the website to clone',
        'url_to_clone': 'URL to clone:',
        'base_url_label': 'New base URL (absolute or relative):',
        'base_url_placeholder': 'Enter the base URL of the website',
        'new_base_url': 'New base URL (absolute or relative):',
        'output_folder_label': 'Output folder name:',
        'output_folder_placeholder': 'Enter the name of the output folder',
        'output_folder': 'Output folder name:',
        'include_images': 'Include images',
        'create_zip': 'Create ZIP file',
        'keep_folder': 'Keep uncompressed folder',
        'appearance_mode': 'Appearance Mode:',
        'ready_to_clone': 'Ready to clone',
        'clone_site': '🔄 Clone Site',
        'clone_button': '🔄 Clone Site',
        'pause': '⏸️ Pause',
        'resume': '▶️ Resume',
        'cancel': '❌ Cancel',
        'downloading_main': 'Downloading main page...',
        'analyzing_html': 'Analyzing HTML structure...',
        'processing_styles': 'Processing internal styles...',
        'identifying_resources': 'Identifying resources...',
        'downloading_resources': 'Downloading resources ({0}/{1})...',
        'compressing_site': 'Compressing cloned site...',
        'completed': 'Completed!',
        'paused': '⏸️ Paused',
        'resumed': '▶️ Resumed',
        'process_paused': 'Process paused... 🔄',
        'cancelling_process': 'Cancelling process...',
        'process_cancelled': 'Process cancelled.',
        'error_occurred': 'An error occurred while cloning the site.',
        'success_message': 'The site has been cloned and saved as \'{0}.zip\'.',
        'success_message_no_zip': 'The site has been cloned and saved in \'{0}\'.',
        'url_required': 'Both URL fields are required.',
        'output_option_required': 'You must select at least one output option: Create ZIP or Keep folder.',
        'language': 'Language',
        'language_switch': 'Español',
        'settings': '⚙️ Settings',
        'settings_button': '⚙️ Settings',
        'theme': 'Theme',
        'theme_menu': 'Theme',
        'light': 'Light',
        'dark': 'Dark',
        'light_theme': 'Light',
        'dark_theme': 'Dark',
        'dark_mode': '🌙',  # Moon icon for dark mode
        'light_mode': '☀️',  # Sun icon for light mode
        'theme_toggle_dark': '🌙',
        'theme_toggle_light': '☀️',
        'default_folder': 'cloned_site',
        'cleanup_cancelled': 'Cleaning up cancelled process...',
        'about': 'About',
        'about_title': 'About Web Cloner',
        'about_message': 'Web Cloner v1.0.0\n\n© 2025 CripterHack\n\nA user-friendly application to clone websites with a modern graphical interface.\n\nLicensed under the MIT License.',
        'donate': 'Donate via PayPal',
        'sponsor': 'Sponsor on GitHub',
        'error': 'Error',
        'success': 'Success',
        'confirm': 'Confirm',
        'cancel_confirm': 'Are you sure you want to cancel the cloning process?',
        'cloning_error': 'An error occurred during cloning',
        'process_error': 'Process error',
        'both_created': 'The site has been cloned. Files are available at:\nZIP: {0}\nFolder: {1}',
        'zip_created': 'The site has been cloned and saved as {0}',
        'folder_kept': 'The site has been cloned and saved in {0}',
        'warning_color': '#FFFF33',
        'error_color': '#FF3333',
        'success_color': '#00FF00'
    },
    'es': {
        'title': 'Clonador de Sitios Web',
        'window_title': 'Clonador de Sitios Web',
        'url_label': 'URL a clonar:',
        'url_placeholder': 'Ingrese la URL del sitio web a clonar',
        'url_to_clone': 'URL a clonar:',
        'base_url_label': 'Nueva URL base (absoluta o relativa):',
        'base_url_placeholder': 'Ingrese la URL base del sitio web',
        'new_base_url': 'Nueva URL base (absoluta o relativa):',
        'output_folder_label': 'Nombre de carpeta de salida:',
        'output_folder_placeholder': 'Ingrese el nombre de la carpeta de salida',
        'output_folder': 'Nombre de carpeta de salida:',
        'include_images': 'Incluir imágenes',
        'create_zip': 'Crear archivo ZIP',
        'keep_folder': 'Mantener carpeta sin comprimir',
        'appearance_mode': 'Modo de apariencia:',
        'ready_to_clone': 'Listo para clonar',
        'clone_site': '🔄 Clonar Sitio',
        'clone_button': '🔄 Clonar Sitio',
        'pause': '⏸️ Pausar',
        'resume': '▶️ Reanudar',
        'cancel': '❌ Cancelar',
        'downloading_main': 'Descargando página principal...',
        'analyzing_html': 'Analizando estructura HTML...',
        'processing_styles': 'Procesando estilos internos...',
        'identifying_resources': 'Identificando recursos...',
        'downloading_resources': 'Descargando recursos ({0}/{1})...',
        'compressing_site': 'Comprimiendo sitio clonado...',
        'completed': '¡Completado!',
        'paused': '⏸️ Pausado',
        'resumed': '▶️ Reanudado',
        'process_paused': 'Proceso pausado... 🔄',
        'cancelling_process': 'Cancelando proceso...',
        'process_cancelled': 'Proceso cancelado.',
        'error_occurred': 'Ha ocurrido un error al clonar el sitio.',
        'success_message': 'El sitio ha sido clonado y guardado como \'{0}.zip\'.',
        'success_message_no_zip': 'El sitio ha sido clonado y guardado en \'{0}\'.',
        'url_required': 'Ambos campos de URL son requeridos.',
        'output_option_required': 'Debe seleccionar al menos una opción de salida: Crear ZIP o Mantener carpeta.',
        'language': 'Idioma',
        'language_switch': 'English',
        'settings': '⚙️ Ajustes',
        'settings_button': '⚙️ Ajustes',
        'theme': 'Tema',
        'theme_menu': 'Tema',
        'light': 'Claro',
        'dark': 'Oscuro',
        'light_theme': 'Claro',
        'dark_theme': 'Oscuro',
        'dark_mode': '🌙',  # Moon icon for dark mode
        'light_mode': '☀️',  # Sun icon for light mode
        'theme_toggle_dark': '🌙',
        'theme_toggle_light': '☀️',
        'default_folder': 'sitio_clonado',
        'cleanup_cancelled': 'Limpiando archivos del proceso cancelado...',
        'about': 'Acerca de',
        'about_title': 'Acerca de Web Cloner',
        'about_message': 'Web Cloner v1.0.0\n\n© 2025 CripterHack\n\nUna aplicación amigable para clonar sitios web con una interfaz gráfica moderna.\n\nLicenciado bajo la Licencia MIT.',
        'donate': 'Donar vía PayPal',
        'sponsor': 'Patrocinar en GitHub',
        'error': 'Error',
        'success': 'Éxito',
        'confirm': 'Confirmar',
        'cancel_confirm': '¿Está seguro de que desea cancelar el proceso de clonación?',
        'cloning_error': 'Ocurrió un error durante la clonación',
        'process_error': 'Error en el proceso',
        'both_created': 'El sitio ha sido clonado. Los archivos están disponibles en:\nZIP: {0}\nCarpeta: {1}',
        'zip_created': 'El sitio ha sido clonado y guardado como {0}',
        'folder_kept': 'El sitio ha sido clonado y guardado en {0}',
        'warning_color': '#FFFF33',
        'error_color': '#FF3333',
        'success_color': '#00FF00'
    }
}

# Global variable for current language
current_language = 'en'

def apply_theme_colors():
    """Apply the colors of the current theme to the interface"""
    colors = DARK_COLORS if current_theme == "dark" else LIGHT_COLORS
    
    # Apply custom colors to different elements
    app.configure(fg_color=colors["fg_color"])
    main_frame.configure(fg_color=colors["fg_color"])
    
    # Configure the theme button color
    theme_toggle_button.configure(
        fg_color=colors["button_color"],
        text_color=colors.get("button_text_color", colors["fg_color"]),
        text=translations[current_language]["light_mode"] if current_theme == "dark" else translations[current_language]["dark_mode"],
        hover_color=colors["hover_color"]
    )
    
    # Configure the settings button
    settings_button.configure(
        fg_color=colors["button_color"],
        text_color=colors.get("button_text_color", colors["fg_color"]),
        hover_color=colors["hover_color"]
    )
    
    # Configure main buttons
    btn_clone.configure(
        fg_color=colors["button_color"],
        text_color=colors.get("button_text_color", colors["fg_color"]),
        hover_color=colors["hover_color"]
    )
    btn_pause.configure(
        fg_color=colors["button_color"],
        text_color=colors.get("button_text_color", colors["fg_color"]),
        hover_color=colors["hover_color"]
    )
    btn_cancel.configure(
        fg_color=colors["button_color"],
        text_color=colors.get("button_text_color", colors["fg_color"]),
        hover_color=colors["hover_color"]
    )
    
    # Configure progress bar
    progress_bar.configure(
        progress_color=colors["progress_color"]
    )
    
    # Apply text color to labels
    for label in [
        title_label, url_label, base_url_label, output_folder_label,
        progress_label
    ]:
        label.configure(text_color=colors["text_color"])
    
    # Configure checkboxes
    include_images_check.configure(
        text_color=colors["text_color"],
        fg_color=colors.get("checkbox_color", colors["button_color"]),
        hover_color=colors["hover_color"]
    )
    create_zip_check.configure(
        text_color=colors["text_color"],
        fg_color=colors.get("checkbox_color", colors["button_color"]),
        hover_color=colors["hover_color"]
    )
    keep_folder_check.configure(
        text_color=colors["text_color"],
        fg_color=colors.get("checkbox_color", colors["button_color"]),
        hover_color=colors["hover_color"]
    )
    
    # Configure input fields
    for entry in [entry_url, entry_base_url, entry_output_folder]:
        entry.configure(
            fg_color=colors.get("entry_bg_color", colors["fg_color"]),
            text_color=colors["text_color"],
            border_color=colors["border_color"]
        )

def toggle_theme():
    """Alterna entre el tema claro y oscuro"""
    global current_theme
    
    # Cambiar el tema actual
    current_theme = "light" if current_theme == "dark" else "dark"
    
    # Configurar el modo de apariencia de CustomTkinter
    ctk.set_appearance_mode(current_theme)
    
    # Aplicar colores personalizados
    apply_theme_colors()

def update_language(new_language=None):
    global current_language
    
    # Update language if specified
    if new_language:
        current_language = new_language
    
    # Update window title
    app.title(translations[current_language]['window_title'])
    
    # Update labels and placeholder of fields
    url_label.configure(text=translations[current_language]['url_label'])
    entry_url.configure(placeholder_text=translations[current_language]['url_placeholder'])
    
    base_url_label.configure(text=translations[current_language]['base_url_label'])
    entry_base_url.configure(placeholder_text=translations[current_language]['base_url_placeholder'])
    
    output_folder_label.configure(text=translations[current_language]['output_folder_label'])
    entry_output_folder.configure(placeholder_text=translations[current_language]['output_folder_placeholder'])
    
    # Update buttons
    btn_clone.configure(text=translations[current_language]['clone_button'])
    btn_pause.configure(text=translations[current_language]['pause'])
    btn_cancel.configure(text=translations[current_language]['cancel'])
    
    # Update checkbox and language change button
    include_images_check.configure(text=translations[current_language]['include_images'])
    create_zip_check.configure(text=translations[current_language]['create_zip'])
    keep_folder_check.configure(text=translations[current_language]['keep_folder'])
    
    # Button to change language
    if current_language == 'en':
        btn_language.configure(text=translations['en']['language_switch'])
    else:
        btn_language.configure(text=translations['es']['language_switch'])
        
    # Update theme button
    theme_toggle_button.configure(text=translations[current_language][f'theme_toggle_{current_theme}'])
    
    # Update settings menu
    settings_menu.entryconfig(0, label=translations[current_language]['language'])
    settings_menu.entryconfig(5, label=translations[current_language]['about'])
    
    # Update progress label
    progress_label.configure(text=translations[current_language]['ready_to_clone'])
    
    # Update main title
    title_label.configure(text=translations[current_language]['title'])

def extract_css_urls(css_content, base_url):
    # This function extracts image URLs from CSS rules
    extracted_urls = []
    
    # Patterns for url() in CSS
    patterns = [
        r'url\(["\']?(.*?)["\']?\)',  # url('example.jpg'), url("example.jpg"), url(example.jpg)
        r'@import\s+["\']([^"\']+)["\']',  # @import 'example.css', @import "example.css"
        r'@import\s+url\(["\']?([^"\'()]+)["\']?\)'  # @import url('example.css'), @import url("example.css"), @import url(example.css)
    ]
    
    for pattern in patterns:
        for match in re.finditer(pattern, css_content):
            url = match.group(1).strip()
            if url and not url.startswith(('data:', 'javascript:', '#')):
                absolute_url = urljoin(base_url, url)
                extracted_urls.append(absolute_url)
    
    return extracted_urls

def normalize_url(url):
    """Normalizes URLs by ensuring they have the correct protocol"""
    if not url:
        return url
        
    # If the URL already has a protocol, return it as is
    if url.startswith(('http://', 'https://')):
        return url
    
    # Try HTTPS first (preferred)
    https_url = f"https://{url}"
    
    try:
        # Make a HEAD request to verify if the site is available with HTTPS
        response = requests.head(https_url, timeout=5)
        if response.status_code < 400:  # Any code less than 400 is considered successful
            return https_url
    except Exception:
        pass
    
    # If HTTPS is not available or gave an error, use HTTP
    return f"http://{url}"

def get_unique_folder_name(base_name):
    """Generates a unique folder name to avoid overwriting existing files"""
    if not os.path.exists(base_name):
        return base_name
    
    counter = 1
    while True:
        new_name = f"{base_name}_{counter}"
        if not os.path.exists(new_name):
            return new_name
        counter += 1

def fetch_and_clone_website(source_url, base_url, output_folder='cloned_site', include_images=True, create_zip=True, keep_folder=True, progress_callback=None):
    global PAUSED, CANCELLED
    
    # Variable to store the created folder to clean it in case of cancellation
    current_output_folder = None
    
    try:
        # Get a unique folder name
        unique_output_folder = get_unique_folder_name(output_folder)
        current_output_folder = unique_output_folder
        
        # Initialize progress
        if progress_callback:
            progress_callback(5, translations[current_language]['downloading_main'])
            
        # Fetch the website content
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(source_url, headers=headers)
        response.raise_for_status()

        # Verify if cancelled
        if CANCELLED:
            if progress_callback:
                progress_callback(0, translations[current_language]['process_cancelled'])
            return False, None, None

        # Parse the content with BeautifulSoup - using 'html.parser' to preserve styles
        soup = BeautifulSoup(response.text, 'html.parser')

        if progress_callback:
            progress_callback(10, translations[current_language]['analyzing_html'])
            
        # Verify if cancelled
        if CANCELLED:
            if progress_callback:
                progress_callback(0, translations[current_language]['process_cancelled'])
            return False, None, None
            
        # Modify the base URL
        base_tag = soup.find('base')
        if base_tag:
            base_tag['href'] = base_url
        else:
            base_tag = soup.new_tag('base', href=base_url)
            if soup.head:
                soup.head.insert(0, base_tag)
            else:
                head_tag = soup.new_tag('head')
                head_tag.append(base_tag)
                soup.html.insert(0, head_tag)

        # Create directory structure for the cloned site
        if os.path.exists(unique_output_folder):
            shutil.rmtree(unique_output_folder)
        os.makedirs(unique_output_folder)

        # List to store URLs of resources to download later
        resources_to_download = []

        if progress_callback:
            progress_callback(15, translations[current_language]['processing_styles'])
            
        # Verify if cancelled
        if CANCELLED:
            if progress_callback:
                progress_callback(0, translations[current_language]['process_cancelled'])
            return False, None, unique_output_folder
            
        # Process internal styles to extract image URLs
        for style_tag in soup.find_all('style'):
            if include_images and style_tag.string:
                css_urls = extract_css_urls(style_tag.string, source_url)
                for css_url in css_urls:
                    resources_to_download.append(css_url)

        # Process inline style attributes to extract image URLs
        if include_images:
            for tag in soup.find_all(lambda tag: tag.has_attr('style')):
                css_urls = extract_css_urls(tag['style'], source_url)
                for css_url in css_urls:
                    resources_to_download.append(css_url)

        # Save the modified HTML content
        with open(os.path.join(unique_output_folder, 'index.html'), 'w', encoding='utf-8') as file:
            file.write(str(soup))

        if progress_callback:
            progress_callback(25, translations[current_language]['identifying_resources'])
            
        # Verify if cancelled
        if CANCELLED:
            if progress_callback:
                progress_callback(0, translations[current_language]['process_cancelled'])
            return False, None, unique_output_folder
            
        # Download and save all linked resources (CSS, JS, images)
        for tag in soup.find_all(['link', 'script', 'img', 'a']):
            # Verify if cancelled
            if CANCELLED:
                if progress_callback:
                    progress_callback(0, translations[current_language]['process_cancelled'])
                return False, None, unique_output_folder
                
            # Wait while paused
            while PAUSED and not CANCELLED:
                if progress_callback:
                    progress_callback(-1, translations[current_language]['process_paused'])
                time.sleep(0.5)
                
            # If cancelled during pause
            if CANCELLED:
                if progress_callback:
                    progress_callback(0, translations[current_language]['process_cancelled'])
                return False, None, unique_output_folder
                
            resource_url = None
            
            if tag.name == 'link' and tag.get('href'):
                resource_url = urljoin(source_url, tag['href'])
                # If it's a CSS file, process it to extract image URLs
                if tag.get('rel') and 'stylesheet' in tag.get('rel'):
                    css_response = requests.get(resource_url, headers=headers)
                    if css_response.status_code == 200 and include_images:
                        css_urls = extract_css_urls(css_response.text, resource_url)
                        resources_to_download.extend(css_urls)
            elif tag.name == 'script' and tag.get('src'):
                resource_url = urljoin(source_url, tag['src'])
            elif tag.name == 'img' and tag.get('src'):
                if include_images:
                    resource_url = urljoin(source_url, tag['src'])
                else:
                    resource_url = None
            elif tag.name == 'a' and tag.get('href'):
                # Process anchor tags to rewrite relative links
                href = tag['href']
                if href.startswith(('http://', 'https://')):
                    continue  # Skip external links
                elif not href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                    # It's a relative link, rewrite it
                    full_url = urljoin(source_url, href)
                    # Here we could recursively clone this page too if needed
            
            if resource_url and not resource_url.startswith(('mailto:', 'tel:', 'javascript:')):
                resources_to_download.append(resource_url)
        
        # Remove duplicates
        resources_to_download = list(set(resources_to_download))
        
        if progress_callback:
            progress_callback(35, f"{translations[current_language]['downloading_resources'].format(0, len(resources_to_download))}")
        
        # Verify if cancelled
        if CANCELLED:
            if progress_callback:
                progress_callback(0, translations[current_language]['process_cancelled'])
            return False, None, unique_output_folder
        
        # Download all resources
        total_resources = len(resources_to_download)
        for i, resource_url in enumerate(resources_to_download):
            # Verify if cancelled
            if CANCELLED:
                if progress_callback:
                    progress_callback(0, translations[current_language]['process_cancelled'])
                return False, None, unique_output_folder
                
            # Wait while paused
            while PAUSED and not CANCELLED:
                if progress_callback:
                    progress_callback(-1, translations[current_language]['process_paused'])
                time.sleep(0.5)
                
            # If cancelled during pause
            if CANCELLED:
                if progress_callback:
                    progress_callback(0, translations[current_language]['process_cancelled'])
                return False, None, unique_output_folder
                
            save_resource(resource_url, unique_output_folder, source_url)
            if progress_callback and total_resources > 0:
                # Calculate progress from 35% to 90% based on the number of resources downloaded
                progress_percent = 35 + int((i / total_resources) * 55)
                progress_callback(progress_percent, translations[current_language]['downloading_resources'].format(i+1, total_resources))

        # Verify if cancelled
        if CANCELLED:
            if progress_callback:
                progress_callback(0, translations[current_language]['process_cancelled'])
            return False, None, unique_output_folder

        # If creating the ZIP file was requested
        zip_file_path = None
        if create_zip:
            if progress_callback:
                progress_callback(95, translations[current_language]['compressing_site'])
                
            # Zip the cloned site
            zip_file_path = f"{unique_output_folder}.zip"
            shutil.make_archive(unique_output_folder, 'zip', unique_output_folder)
            
            # If you don't want to keep the original folder, delete it after creating the ZIP
            if not keep_folder:
                shutil.rmtree(unique_output_folder)
                unique_output_folder = None

        # Verify if cancelled
        if CANCELLED:
            if progress_callback:
                progress_callback(0, translations[current_language]['process_cancelled'])
            return False, None, unique_output_folder
                
        if progress_callback:
            progress_callback(100, translations[current_language]['completed'])
            
        return True, unique_output_folder, zip_file_path
    except Exception as e:
        print(f"An error occurred: {e}")
        if progress_callback:
            progress_callback(0, f"Error: {str(e)}")
        return False, None, current_output_folder

def save_resource(resource_url, output_dir, source_url):
    try:
        parsed_url = urlparse(resource_url)
        
        # Skip URLs with unsupported schemes
        if parsed_url.scheme not in ('http', 'https', ''):
            print(f"Skipping unsupported URL scheme: {resource_url}")
            return
        
        # Handle relative URLs    
        if not parsed_url.scheme:
            resource_url = urljoin(source_url, resource_url)
            parsed_url = urlparse(resource_url)
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': source_url
        }
        
        response = requests.get(resource_url, stream=True, headers=headers)
        response.raise_for_status()

        # Decode the URL to get the correct file name
        path = unquote(parsed_url.path)
        resource_path = os.path.join(output_dir, path.lstrip('/'))
        
        if resource_path.endswith('/') or not os.path.basename(resource_path):
            resource_path = os.path.join(resource_path, 'index.html')

        # Create directories if they don't exist
        os.makedirs(os.path.dirname(resource_path), exist_ok=True)
        
        # Determine content type
        content_type = response.headers.get('Content-Type', '')
        extension = os.path.splitext(resource_path)[1].lower()
        
        # Save text files as text, binary files as binary
        if 'text/' in content_type or extension in ('.css', '.js', '.html', '.htm', '.svg', '.xml'):
            with open(resource_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
                
            # If it's CSS, extract and download referenced images
            if extension == '.css':
                css_urls = extract_css_urls(response.text, resource_url)
                for css_url in css_urls:
                    if not css_url.startswith('data:'):
                        save_resource(css_url, output_dir, resource_url)
        else:
            with open(resource_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
                
        print(f"Saved resource: {resource_url} -> {resource_path}")
    except Exception as e:
        print(f"Failed to save resource {resource_url}: {e}")

def update_progress(value, message):
    """Function to update the progress bar and message with improved formatting"""
    colors = DARK_COLORS if current_theme == "dark" else LIGHT_COLORS
    
    # Update process in the UI
    if value == -1:  # Special value for paused state
        progress_label.configure(
            text=message,
            text_color=colors["warning_color"]
        )
    elif value == 0:  # Special value for cancelled state
        progress_label.configure(
            text=message,
            text_color=colors["error_color"]
        )
        progress_bar.set(0)
    else:
        normalized_value = value / 100
        progress_bar.set(normalized_value)
        progress_label.configure(
            text=message,
            text_color=colors["success_color"] if value >= 100 else colors["text_color"]
        )
    
    # Force update to avoid freezing
    app.update()

def toggle_pause():
    """Function to toggle the pause state"""
    global PAUSED
    PAUSED = not PAUSED
    
    if PAUSED:
        btn_pause.configure(text=translations[current_language]['resume'])
    else:
        btn_pause.configure(text=translations[current_language]['pause'])

def cancel_process():
    """Function to cancel the cloning process"""
    global CANCELLED
    
    # Ask for confirmation before cancelling
    if messagebox.askyesno(
        translations[current_language]['confirm'],
        translations[current_language]['cancel_confirm']
    ):
        CANCELLED = True
        update_progress(0, translations[current_language]['cleanup_cancelled'])
        
        # Reset UI
        btn_clone.configure(state="normal")
        btn_pause.configure(state="disabled")
        btn_cancel.configure(state="disabled")

def cleanup_cancelled_files(folder_path, zip_path):
    """Limpia los archivos creados por un proceso cancelado"""
    if folder_path and os.path.exists(folder_path):
        try:
            update_progress(0, translations[current_language]['cleanup_cancelled'])
            shutil.rmtree(folder_path)
        except Exception as e:
            print(f"Error cleaning up folder: {e}")
    
    if zip_path and os.path.exists(zip_path):
        try:
            update_progress(0, translations[current_language]['cleanup_cancelled'])
            os.remove(zip_path)
        except Exception as e:
            print(f"Error cleaning up ZIP file: {e}")

def clone_site_thread():
    """Function to run the cloning process in a separate thread"""
    global PAUSED, CANCELLED
    
    # Get values from UI
    url = entry_url.get().strip()
    base_url = entry_base_url.get().strip() or url
    output_folder = entry_output_folder.get().strip() or "cloned_site"
    
    # Visual validation
    if not url:
        messagebox.showerror(
            translations[current_language]['error'],
            translations[current_language]['url_required']
        )
        return
        
    # Validate the output options
    if create_zip_var.get() == 0 and keep_folder_var.get() == 0:
        messagebox.showerror(
            translations[current_language]['error'],
            translations[current_language]['output_option_required']
        )
        return
    
    # Normalize URLs if needed
    url = normalize_url(url)
    base_url = normalize_url(base_url) if base_url else url
    
    # Update UI for cloning state
    btn_clone.configure(state="disabled")
    btn_pause.configure(state="normal")
    btn_cancel.configure(state="normal")
    
    # Reset control flags
    PAUSED = False
    CANCELLED = False
    
    # Execute the cloning process in a separate thread to not block the interface
    threading.Thread(target=lambda: execute_cloning(url, base_url, output_folder), daemon=True).start()

def execute_cloning(url, base_url, output_folder):
    """Function to execute the actual cloning process"""
    try:
        success, zip_path, folder_path = fetch_and_clone_website(
            url, 
            base_url, 
            output_folder, 
            include_images_var.get(), 
            create_zip_var.get(),
            keep_folder_var.get(),
            update_progress
        )
            
        # Process is completed
        app.after(0, lambda: complete_cloning(success, zip_path, folder_path))
            
    except Exception as e:
        # Handle errors
        error_message = str(e)
        app.after(0, lambda: handle_error(error_message))

def complete_cloning(success, zip_path, folder_path):
    """Function to handle the completion of the cloning process"""
    # Reset UI
    btn_clone.configure(state="normal")
    btn_pause.configure(state="disabled")
    btn_cancel.configure(state="disabled")
    
    # Show success message if completed successfully
    if success:
        if create_zip_var.get() and keep_folder_var.get():
            # Both ZIP and folder
            messagebox.showinfo(
                translations[current_language]['success'],
                translations[current_language]['both_created'].format(
                    zip_path + ".zip" if zip_path else "",
                    folder_path if folder_path else ""
                )
            )
        elif create_zip_var.get():
            # Only ZIP
            messagebox.showinfo(
                translations[current_language]['success'],
                translations[current_language]['zip_created'].format(
                    zip_path + ".zip" if zip_path else ""
                )
            )
        elif keep_folder_var.get():
            # Only folder
            messagebox.showinfo(
                translations[current_language]['success'],
                translations[current_language]['folder_kept'].format(
                    folder_path if folder_path else ""
                )
            )

def handle_error(error_message):
    """Function to handle errors during the cloning process"""
    # Reset UI
    btn_clone.configure(state="normal")
    btn_pause.configure(state="disabled")
    btn_cancel.configure(state="disabled")
    
    # Show error message
    messagebox.showerror(
        translations[current_language]['error'],
        f"{translations[current_language]['cloning_error']}: {error_message}"
    )
    
    # Reset progress bar
    update_progress(0, translations[current_language]['process_error'])

# Interconnection between checkboxes for mandatory selection logic
def update_checkbox_states(*args):
    """Function to handle the logic of the output checkboxes"""
    create_zip_value = create_zip_var.get()
    keep_folder_value = keep_folder_var.get()
    
    # If both are disabled, force at least one to be active
    # The last one that was disabled is reactivated
    if create_zip_value == 0 and keep_folder_value == 0:
        # We use the last checkbox that was attempted to be disabled
        if args and args[0] == 'create_zip':
            keep_folder_var.set(1)
        else:
            create_zip_var.set(1)

def show_about_dialog():
    """Show the About dialog with program information and support links"""
    # Create a custom about dialog window
    about_window = ctk.CTkToplevel(app)
    about_window.title(translations[current_language]['about_title'])
    about_window.geometry("500x350")  # Increased size for better text display
    about_window.resizable(False, False)
    
    # Make it modal
    about_window.transient(app)
    about_window.grab_set()
    
    # Calculate position for center of parent window
    x = app.winfo_x() + (app.winfo_width() // 2) - (500 // 2)
    y = app.winfo_y() + (app.winfo_height() // 2) - (350 // 2)
    about_window.geometry(f"+{x}+{y}")
    
    # Main frame
    main_frame = ctk.CTkFrame(about_window)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # App info
    info_label = ctk.CTkLabel(
        main_frame, 
        text=translations[current_language]['about_message'],
        font=ctk.CTkFont(size=14),
        justify="center",
        wraplength=460  # Set wraplength to ensure text wraps properly
    )
    info_label.pack(pady=20)
    
    # Function to open URLs
    def open_url(url):
        webbrowser.open(url)
    
    # Support buttons
    buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    buttons_frame.pack(pady=10)
    
    # PayPal button
    paypal_button = ctk.CTkButton(
        buttons_frame,
        text=translations[current_language]['donate'],
        command=lambda: open_url("https://www.paypal.com/paypalme/cripterhack"),
        width=180,  # Increased width for longer text
        height=35
    )
    paypal_button.pack(pady=5)
    
    # GitHub Sponsors button
    github_button = ctk.CTkButton(
        buttons_frame,
        text=translations[current_language]['sponsor'],
        command=lambda: open_url("https://github.com/sponsors/CripterHack"),
        width=180,  # Increased width for longer text
        height=35
    )
    github_button.pack(pady=5)
    
    # Close button
    close_button = ctk.CTkButton(
        main_frame,
        text="OK",
        command=about_window.destroy,
        width=100,
        height=35
    )
    close_button.pack(pady=10)

# Main application window using CustomTkinter
app = ctk.CTk()
app.title(translations[current_language]['window_title'])
app.geometry("650x600")  # Increase height a bit for the new field

# Main frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Top frame for title and buttons
top_frame = ctk.CTkFrame(main_frame)
top_frame.pack(fill="x", pady=10)

# Title
title_label = ctk.CTkLabel(top_frame, text=translations[current_language]['title'], font=ctk.CTkFont(size=26, weight="bold"))
title_label.pack(side="left", expand=True)

# Container for right buttons
top_buttons_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
top_buttons_frame.pack(side="right")

# Button to toggle between themes
theme_toggle_button = ctk.CTkButton(
    top_buttons_frame,
    text=translations[current_language]['theme_toggle_dark'],
    width=40,
    height=30,
    corner_radius=8,
    command=toggle_theme
)
theme_toggle_button.pack(side="left", padx=(0, 10))

# Settings button
settings_button = ctk.CTkButton(
    top_buttons_frame,
    text=translations[current_language]['settings'],
    width=40,
    height=30,
    corner_radius=8,
    command=lambda: settings_menu.tk_popup(settings_button.winfo_rootx(), settings_button.winfo_rooty() + settings_button.winfo_height())
)
settings_button.pack(side="left")

# Settings menu
settings_menu = tk.Menu(app, tearoff=0)
settings_menu.add_command(label=translations[current_language]['language'], state="disabled")
settings_menu.add_separator()
settings_menu.add_command(label="English", command=lambda: update_language('en'))
settings_menu.add_command(label="Español", command=lambda: update_language('es'))
settings_menu.add_separator()
settings_menu.add_command(label=translations[current_language]['about'], command=show_about_dialog)

# Form frame
form_frame = ctk.CTkFrame(main_frame)
form_frame.pack(fill="x", pady=10)

# URL field
url_label = ctk.CTkLabel(form_frame, text=translations[current_language]['url_label'], anchor="w")
url_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

entry_url = ctk.CTkEntry(form_frame, placeholder_text=translations[current_language]['url_placeholder'], height=35)
entry_url.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

# Base URL field
base_url_label = ctk.CTkLabel(form_frame, text=translations[current_language]['base_url_label'], anchor="w")
base_url_label.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))

entry_base_url = ctk.CTkEntry(form_frame, placeholder_text=translations[current_language]['base_url_placeholder'], height=35)
entry_base_url.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))

# Output folder field
output_folder_label = ctk.CTkLabel(form_frame, text=translations[current_language]['output_folder_label'], anchor="w")
output_folder_label.grid(row=4, column=0, sticky="w", padx=10, pady=(10, 0))

entry_output_folder = ctk.CTkEntry(form_frame, placeholder_text=translations[current_language]['output_folder_placeholder'], height=35)
entry_output_folder.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 10))

# Configure weights for form_frame to make it responsive
form_frame.grid_columnconfigure(0, weight=1)

# Options frame
options_frame = ctk.CTkFrame(main_frame)
options_frame.pack(fill="x", pady=10)

# First row for include_images checkbox
options_row1 = ctk.CTkFrame(options_frame, fg_color="transparent")
options_row1.pack(fill="x", pady=5)

# Checkbox for including images
include_images_var = tk.IntVar(value=1)
include_images_check = ctk.CTkCheckBox(
    options_row1, 
    text=translations[current_language]['include_images'], 
    variable=include_images_var,
    onvalue=1, 
    offvalue=0
)
include_images_check.pack(side="left", padx=10)

# Button to change language
btn_language = ctk.CTkButton(
    options_row1,
    text=translations[current_language]['language_switch'],
    command=lambda: update_language('es' if current_language == 'en' else 'en'),
    width=130,
    height=30
)
btn_language.pack(side="right", padx=10)

# Second row for create_zip and keep_folder checkboxes
options_row2 = ctk.CTkFrame(options_frame, fg_color="transparent")
options_row2.pack(fill="x", pady=5)

# Checkbox for creating ZIP
create_zip_var = tk.IntVar(value=1)
create_zip_check = ctk.CTkCheckBox(
    options_row2, 
    text=translations[current_language]['create_zip'], 
    variable=create_zip_var,
    onvalue=1, 
    offvalue=0,
    command=lambda: update_checkbox_states('create_zip')
)
create_zip_check.pack(side="left", padx=10)

# Checkbox for keeping uncompressed folder
keep_folder_var = tk.IntVar(value=1)
keep_folder_check = ctk.CTkCheckBox(
    options_row2, 
    text=translations[current_language]['keep_folder'], 
    variable=keep_folder_var,
    onvalue=1, 
    offvalue=0,
    command=lambda: update_checkbox_states('keep_folder')
)
keep_folder_check.pack(side="left", padx=10)

# Progress frame
progress_frame = ctk.CTkFrame(main_frame)
progress_frame.pack(fill="x", pady=10)

progress_var = ctk.IntVar()
progress_bar = ctk.CTkProgressBar(
    progress_frame,
    height=24,  # Increase the height more to make it more visible
    corner_radius=8,  # More rounded corners
    border_width=0,
    progress_color=DARK_COLORS["progress_color"]  # Neon green color for the bar
)
progress_bar.pack(fill="x", padx=10, pady=10)
progress_bar.set(0)  # Initialize at 0

# Progress label 
progress_label = ctk.CTkLabel(progress_frame, text=translations[current_language]['ready_to_clone'], height=20)
progress_label.pack(pady=(0, 10))

# Buttons frame
buttons_frame = ctk.CTkFrame(main_frame)
buttons_frame.pack(fill="x", pady=10)

# Clone button
btn_clone = ctk.CTkButton(
    buttons_frame, 
    text=translations[current_language]['clone_button'], 
    command=clone_site_thread, 
    width=130, 
    height=38, 
    corner_radius=8, 
    border_width=0
)
btn_clone.pack(side="left", padx=5)

# Pause button (initially disabled)
btn_pause = ctk.CTkButton(
    buttons_frame, 
    text=translations[current_language]['pause'], 
    command=toggle_pause, 
    width=130, 
    height=38, 
    corner_radius=8, 
    border_width=0, 
    state="disabled"
)
btn_pause.pack(side="left", padx=5)

# Cancel button (initially disabled)
btn_cancel = ctk.CTkButton(
    buttons_frame, 
    text=translations[current_language]['cancel'], 
    command=cancel_process, 
    width=130, 
    height=38, 
    corner_radius=8, 
    border_width=0, 
    state="disabled"
)
btn_cancel.pack(side="left", padx=5)

# Apply initial theme to all elements
apply_theme_colors()

# Start the application
if __name__ == "__main__":
    # Update the language of the interface
    update_language()
    # Start the app
    app.mainloop()
