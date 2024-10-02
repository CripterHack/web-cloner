# Website Cloner 🌐

This project is a simple website cloner built with Python. It allows users to clone a website and modify its base URL, saving all resources locally.

## Features ✨

- Clone any website by providing its URL
- Modify the base URL of the cloned site
- Download and save all linked resources (CSS, JS, images)
- Package the cloned site into a zip file
- User-friendly GUI built with tkinter

## Requirements 📋

- Python 3.11.5
- Required Python packages:
  - tkinter
  - requests
  - beautifulsoup4

## Installation 🚀

1. Clone this repository:
   ```
   git clone https://github.com/CripterHack/website-cloner.git
   ```
2. Navigate to the project directory:
   ```
   cd website-cloner
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage 🖥️

1. Run the script:
   ```
   python web-cloner.py
   ```
2. Enter the URL of the website you want to clone in the "URL to clone" field.
3. Enter the new base URL in the "New base URL" field.
4. Click the "Clone Site" button.
5. If successful, the cloned site will be saved as 'cloned_site.zip' in the same directory.

## Creating an Executable 📦

To create an executable file from the Python script, follow these steps:

1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Navigate to the directory containing your Python script.
3. Run PyInstaller:
   ```
   pyinstaller --onefile --windowed web-cloner.py
   ```
4. The executable will be created in the `dist` folder.

## To-Do List 📝

- [ ] Add support for JavaScript rendering
- [ ] Implement multi-threading for faster downloads
- [ ] Add option to specify output directory
- [ ] Create a progress bar for the cloning process
- [ ] Add support for authentication on websites
- [ ] Implement error handling and logging
- [ ] Create a command-line interface version

## Testing 🧪

### Tested Environments
- Windows 11, Python 3.11.5
- Arch Linux, Python 3.9

### Functionality Tested
- Basic website cloning
- Resource downloading (CSS, JS, images)
- Base URL modification

### To Be Tested
- Performance with large websites
- Handling of dynamic content
- Behavior with various URL structures
- Cross-browser compatibility of cloned sites

## Disclaimer ⚠️

This tool is for educational purposes only. Make sure you have the right to clone and modify any website before using this tool. The authors are not responsible for any misuse of this software.

## Contributing 🤝

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/yourusername/website-cloner/issues) if you want to contribute.

## License 📄

[MIT](https://choosealicense.com/licenses/mit/)
