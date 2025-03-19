# Guide to Create a Web Cloner Release

This document provides detailed instructions for generating executables for different platforms and creating a GitHub release.

## Preparation

Before starting, make sure you have:

1. Updated code in your main branch (main/master)
2. All dependencies correctly listed in `requirements.txt`
3. Icon files:
   - Windows: `icon.ico`
   - Linux: `icon.png`
   - macOS: `icon.icns`

## Generating Executables

### For Windows

1. On a Windows system, open PowerShell or CMD
2. Navigate to the project directory
3. Run the build script:
   ```
   .\build_windows.bat
   ```
4. The executable will be generated in the `dist\Web Cloner\` folder
5. Compress the folder for distribution:
   ```
   Compress-Archive -Path "dist\Web Cloner" -DestinationPath "Web-Cloner-Windows.zip"
   ```

### For Linux

1. On a Linux system, open a terminal
2. Navigate to the project directory
3. Make sure the script has execution permissions:
   ```
   chmod +x build_linux.sh
   ```
4. Run the build script:
   ```
   ./build_linux.sh
   ```
5. The AppImage will be generated in the root directory of the project with the name `Web-Cloner-x86_64.AppImage`

### For macOS

1. On a macOS system, open Terminal
2. Navigate to the project directory
3. Make sure you have Homebrew installed:
   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
4. Install create-dmg if you don't have it yet:
   ```
   brew install create-dmg
   ```
5. Make sure the script has execution permissions:
   ```
   chmod +x build_macos.sh
   ```
6. Run the build script:
   ```
   ./build_macos.sh
   ```
7. The DMG will be generated in `dist/Web Cloner.dmg`

## Creating a GitHub Release

1. Go to your repository on GitHub
2. Click on "Releases" on the right side
3. Click on "Draft a new release"
4. Complete the release information:
   - **Tag version**: Choose a version number following SemVer (e.g., v1.0.0)
   - **Release title**: A descriptive title (e.g., "Web Cloner v1.0.0")
   - **Description**: Include release notes, features, and bug fixes
   
   Example of release description:
   ```
   ## Web Cloner v1.0.0
   
   First stable version with cross-platform support.
   
   ### Features
   - Complete website cloning
   - Modern graphical interface with dark and light themes
   - Support for English and Spanish
   - Options to include/exclude images
   - Creation of ZIP files or folders
   
   ### Instructions
   - Windows: Download the ZIP, extract and run Web Cloner.exe
   - Linux: Download the AppImage, make it executable with "chmod +x Web-Cloner-x86_64.AppImage" and run it
   - macOS: Download the DMG, open it and drag the application to your Applications folder
   ```

5. Upload the executable files for each platform:
   - `Web-Cloner-Windows.zip`
   - `Web-Cloner-x86_64.AppImage`
   - `Web Cloner.dmg`

6. If it's a preview/beta version, check "This is a pre-release"
7. Finally click on "Publish release"

## Post-Release Verification

Once the release is published, it's recommended to:

1. Download each executable from the release
2. Test that they work correctly on each operating system
3. Verify all main functionalities
4. Check localization and themes

## Troubleshooting

### Common Windows issues
- If PyInstaller doesn't find modules, try using `--hidden-import=module_name`
- Permission problems: Run as administrator

### Common Linux issues
- Missing dependencies: Install dependencies with `apt install libgtk-3-0`
- Permissions: Make sure the AppImage is executable with `chmod +x`

### Common macOS issues
- Unsigned application: Users will need to authorize the application in System Preferences > Security & Privacy
- Issues with create-dmg: Make sure you have Xcode Command Line Tools installed 