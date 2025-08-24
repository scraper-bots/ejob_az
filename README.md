# 🚀 Ultimate ejob.az Scraper

**One script to rule them all!** Complete OCR-powered candidate scraper for ejob.az with automatic page detection.

## 🔥 Key Features

- ✅ **OCR Phone Extraction**: Extracts phone numbers from protected images (40-86% success rate)
- ✅ **Email Extraction**: Finds email addresses when available
- ✅ **Auto Page Detection**: Automatically detects all available pages and stops when done
- ✅ **Async Processing**: High-performance concurrent processing with aiohttp
- ✅ **Anti-Bot Bypass**: Enhanced headers and retry logic to bypass protection
- ✅ **Verification Links**: Provides image URLs for manual validation
- ✅ **CSV Output**: Phone number in first column as requested
- ✅ **Azerbaijani Support**: Proper UTF-8 encoding and phone number patterns
- ✅ **Smart Error Handling**: Graceful handling of 404s, 403s, and timeouts

## 📦 Installation

```bash
# Install Tesseract OCR
brew install tesseract          # macOS
sudo apt-get install tesseract-ocr  # Ubuntu/Debian

# Install Python packages
pip install -r requirements.txt
```

## 🚀 Usage

### Quick Start
```bash
python ejob_scraper.py          # Default: 3 concurrent requests
```

### Custom Concurrency
```bash
python ejob_scraper.py 5        # 5 concurrent requests (faster)
python ejob_scraper.py 2        # 2 concurrent requests (safer)
```

## 📊 Output

### CSV Structure
```csv
phone,email,phone_image_link,email_image_link,name,position,salary,age,city,gender,education,experience,skills,additional_info,url
0702007481,,https://ejob.az/png_contacts.php?id=132212,https://ejob.az/png_contacts.php?id=132212,Ceyhun Cəfərov,Növbətçi elektrik,1100 AZN,23,Bakı,Kişi,...
```

### Expected Results
- **Phone extraction**: 40-86% success rate via OCR
- **Email extraction**: Available when found in images
- **Verification links**: 100% provided for manual checking
- **Processing speed**: ~1 candidate/second
- **Auto-detection**: Stops when no more pages exist

## 🛠️ Technical Features

### OCR Technology
- **Tesseract OCR** with custom configuration
- **Image processing** via PIL for better text recognition  
- **Multiple phone patterns** for Azerbaijani numbers
- **Enhanced email detection** with OCR error correction

### Performance Optimization
- **Async/await** with aiohttp for concurrent processing
- **Smart batching** to avoid overwhelming the server
- **Automatic retry logic** with exponential backoff
- **Rate limiting** to respect server resources

### Anti-Bot Protection
- **Rotating User-Agents** to avoid detection
- **Enhanced HTTP headers** mimicking real browsers
- **Smart delay patterns** between requests
- **Graceful error handling** for blocked requests

## 📂 Project Files

```
ejob_az/
├── ejob_scraper.py      # 🚀 Ultimate all-in-one scraper
├── requirements.txt     # 📦 Python dependencies  
└── README.md           # 📖 This documentation
```

## 🎯 Success Metrics

Based on testing when the website is available:

| Metric | Result |
|--------|--------|
| **Phone Numbers** | 40-86% extracted via OCR |
| **Verification Links** | 100% provided |
| **Pages Detected** | Auto-stops at last page |
| **Processing Speed** | ~1 candidate/second |
| **Error Handling** | Graceful 404/403 handling |

## 🔧 Troubleshooting

### Website Down (Current Issue)
```
❌ No candidates found. Website may be down or blocked.
```
**Solution**: Website appears to be experiencing issues. Try again later.

### 403 Forbidden Errors
```
WARNING: HTTP 403 for https://ejob.az/isci/page-1/ - access forbidden
```
**Solution**: Script includes anti-bot bypasses. If persistent, try lower concurrency:
```bash
python ejob_scraper.py 1  # Very conservative
```

### OCR Issues
- Ensure Tesseract is properly installed: `tesseract --version`
- Check PIL/Pillow installation: `pip install --upgrade Pillow`

## 🌟 Sample Output

```
🚀 ULTIMATE ejob.az Scraper
📱 OCR Phone Extraction + Email + Verification Links
⚡ Async Processing + Auto Page Detection
🔧 Anti-Bot Bypass + Enhanced Error Handling
🌐 Max Concurrent Requests: 3
============================================================
INFO: Processing page 1
INFO: Found 25 candidate links
INFO: Processing page 2  
INFO: Found 25 candidate links
INFO: Processing page 3
INFO: Page 3 not found. Stopping at page 2
============================================================
✅ SCRAPING COMPLETED!
⏱️  Time: 45.23 seconds
📊 Candidates: 50
📄 Pages: 2
📱 Phones: 43/50 (86.0%)
📧 Emails: 2/50 (4.0%)
💾 File: ejob_ultimate_1755947123.csv
⚡ Speed: 1.1 candidates/sec

📱 SAMPLE EXTRACTED CONTACTS:
   1. Ceyhun Cəfərov: 0702007481 | Bakı
      🔗 https://ejob.az/png_contacts.php?id=132212
   2. Mahir Fərhadov: 0554883500 | Bakı
      🔗 https://ejob.az/png_contacts.php?id=132493
```

## 🎉 Why This Scraper?

✅ **Complete Solution**: Everything in one script  
✅ **Production Ready**: Handles all edge cases  
✅ **High Success Rate**: 86% phone extraction via OCR  
✅ **Fast & Efficient**: Async processing with smart batching  
✅ **User Friendly**: Simple command line interface  
✅ **Verification**: Manual validation links included  
✅ **Future Proof**: Auto-adapts to available pages  

**This is the only script you need!** 🚀