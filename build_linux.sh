#!/bin/bash
echo "Building Web Cloner for Linux..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build with PyInstaller
pyinstaller --name="Web-Cloner" \
            --windowed \
            --icon=icon.ico \
            --add-data="icon.ico:." \
            --collect-all customtkinter \
            web-cloner.py

echo "Build completed. The executable is located in the dist/ folder"

# Create AppDir structure for AppImage
mkdir -p WebCloner.AppDir/usr/bin
mkdir -p WebCloner.AppDir/usr/share/applications
mkdir -p WebCloner.AppDir/usr/share/icons/hicolor/256x256/apps

# Copy files
cp -r dist/Web-Cloner/* WebCloner.AppDir/usr/bin/
cp icon.png WebCloner.AppDir/usr/share/icons/hicolor/256x256/apps/web-cloner.png
cp icon.png WebCloner.AppDir/web-cloner.png

# Create .desktop file
cat > WebCloner.AppDir/web-cloner.desktop << EOF
[Desktop Entry]
Name=Web Cloner
Exec=web-cloner
Icon=web-cloner
Type=Application
Categories=Network;WebDevelopment;
Comment=Web cloning tool
EOF

cp WebCloner.AppDir/web-cloner.desktop WebCloner.AppDir/usr/share/applications/

# Create AppRun file
cat > WebCloner.AppDir/AppRun << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
export PATH="\$PATH:\$APPDIR/usr/bin"
export LD_LIBRARY_PATH="\$LD_LIBRARY_PATH:\$APPDIR/usr/lib"
exec "\$APPDIR/usr/bin/Web-Cloner" "\$@"
EOF

chmod +x WebCloner.AppDir/AppRun

echo "AppDir structure created. Now you can use appimagetool to create the AppImage."
echo "Example: ./appimagetool-x86_64.AppImage WebCloner.AppDir"

# Download appimagetool if it doesn't exist
if [ ! -f appimagetool-x86_64.AppImage ]; then
    echo "Downloading appimagetool..."
    wget "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
    chmod +x appimagetool-x86_64.AppImage
fi

# Create AppImage
echo "Creating AppImage..."
./appimagetool-x86_64.AppImage WebCloner.AppDir

echo "AppImage build finished!" 