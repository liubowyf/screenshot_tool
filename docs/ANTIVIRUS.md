# Antivirus False Positives

## Why False Positives Occur

Screenshot capture and network upload functionalities can

 trigger antivirus heuristics designed to detect spyware behavior.

## Solutions

### 1. Code Signing Certificate (Most Effective)

Digital signatures prove software authenticity and integrity.

**Providers:**
- DigiCert: ~$200-500/year
- Sectigo: ~$100-300/year
- Local providers: varies by region

**Sign the executable:**
```cmd
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com /fd SHA256 ScreenCapture.exe
```

**Expected reduction:** 80-95% fewer false positives

### 2. Add File Metadata (Free)

Include version information in the executable.

The project already includes `version_info.txt` which is used during build. Customize company name and description as needed.

### 3. Optimize Build Parameters (Free)

Current build already implements:
- `--noupx` - Disables UPX compression (reduces false positives)
- `--strip` - Removes debug symbols
- Version metadata inclusion

### 4. Whitelist Submission (Free, Time-Consuming)

Submit false positive reports to AV vendors:

- **Windows Defender:** https://www.microsoft.com/en-us/wdsi/filesubmission
- **Kaspersky:** https://opentip.kaspersky.com/
- **Other vendors:** Check respective vendor websites

Response time: 1-7 days typically

### 5. Alternative: Nuitka (Free, Better Results)

Nuitka compiles Python to C code instead of packaging it.

```bash
pip install nuitka
nuitka --standalone --onefile --windows-disable-console screenshot_tool.py
```

**Expected reduction:** 30-50% fewer false positives vs PyInstaller

## Recommended Approach

**For production use:**
1. Code signing certificate
2. Keep current optimized build parameters
3. Submit to AV whitelists if needed

**For testing/personal use:**
1. Add to AV whitelist manually
2. Use current optimized build

## Testing

Upload to VirusTotal (https://www.virustotal.com/) to check detection rates.

**Note:** VirusTotal shares samples with AV vendors, which may increase future detections. Test locally first when possible.

## Legal Reminder

These techniques are for legitimate software distribution only. Ensure all usage complies with applicable laws and regulations.
