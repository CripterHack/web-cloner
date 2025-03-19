#!/bin/bash
echo "Building Web Cloner for macOS..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add create-dmg if not installed
if ! command -v create-dmg &> /dev/null; then
    echo "Installing create-dmg..."
    brew install create-dmg || { echo "Please install Homebrew: https://brew.sh/"; exit 1; }
fi

# Build with PyInstaller
pyinstaller --name="Web Cloner" \
            --windowed \
            --icon=icon.icns \
            --add-data="icon.icns:." \
            --collect-all customtkinter \
            --osx-bundle-identifier="com.webcloner.app" \
            web-cloner.py

echo "Build completed. The application is located in the dist/ folder"

# Create DMG
echo "Creating DMG file..."

# Clean DMG folder
mkdir -p dist/dmg
rm -rf dist/dmg/*
cp -r "dist/Web Cloner.app" dist/dmg/

# If a DMG already exists, delete it
test -f "dist/Web Cloner.dmg" && rm "dist/Web Cloner.dmg"

# Create the DMG
create-dmg \
  --volname "Web Cloner" \
  --volicon "icon.icns" \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon "Web Cloner.app" 175 120 \
  --hide-extension "Web Cloner.app" \
  --app-drop-link 425 120 \
  "dist/Web Cloner.dmg" \
  "dist/dmg/"

echo "DMG build completed! The installer is in dist/Web Cloner.dmg" 