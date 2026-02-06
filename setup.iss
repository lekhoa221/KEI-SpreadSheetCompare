#define MyAppName "DocCompare AI"
#include "installer\\version.iss"
#ifndef MyAppVersion
#define MyAppVersion "1.0.1"
#endif
#define MyAppPublisher "Personal Project"
#define MyAppExeName "DocCompareAI.exe"
; Generate a stable unique AppId once and keep it the same across versions.
; You can regenerate with Tools -> Generate GUID in Inno Setup IDE.
#define MyAppId "{{F2C4F682-20F6-4D56-9C3C-3A8E2D6A7B59}}"

[Setup]
; Basic Application Information
AppId={#MyAppId}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
; Where to save the installer file
OutputDir=installer
OutputBaseFilename=DocCompareAI_Setup_v{#MyAppVersion}
; Icon for the installer (optional, using the app icon if available)
SetupIconFile=app_icon.ico
; Compression settings for smaller file size
Compression=lzma2/ultra64
SolidCompression=yes
; Ensure 64-bit install if the app is 64-bit
ArchitecturesInstallIn64BitMode=x64
; UI Settings
DisableProgramGroupPage=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; IMPORTANT: This assumes you have run build_app.bat successfully first!
; copy the main executable
Source: "dist\DocCompareAI\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; copy all other files (dependencies, assets, etc.)
Source: "dist\DocCompareAI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Start Menu Shortcut
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
; Uninstall Shortcut
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
; Desktop Shortcut
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Option to launch the app after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#MyAppName}}"; Flags: nowait postinstall skipifsilent
