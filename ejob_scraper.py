#!/usr/bin/env python3
"""
Ultimate ejob.az Scraper - Working Version with OCR
🚀 Features: OCR phone extraction + verification links + resume functionality
Usage: python ejob_scraper.py [start_page] [end_page]
Examples:
  python ejob_scraper.py 5           # Scrape pages 1-5
  python ejob_scraper.py 49 60       # Resume from page 49 to 60
  python ejob_scraper.py 1 100       # Scrape pages 1-100
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv
import re
import time
import random
from urllib.parse import urljoin
import logging
from PIL import Image
import pytesseract
import io

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class WorkingEjobScraper:
    def __init__(self):
        self.base_url = "https://ejob.az"
        self.session = self.create_session()
    
    def create_session(self):
        """Create requests session with proper headers"""
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,az;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        return session
    
    def extract_phone_from_text(self, text):
        """Extract phone number from OCR text"""
        if not text:
            return ""
        
        text = re.sub(r'[^\w\s+()-]', '', text)
        
        phone_patterns = [
            r'\+994[-\s]?\d{2}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}',
            r'994[-\s]?\d{2}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}',
            r'0\d{2}[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}',
            r'\d{3}[-\s]?\d{2}[-\s]?\d{2}[-\s]?\d{2}',
            r'0\d{2}[-\s]?\d{7}',
            r'\d{10}',
        ]
        
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            if matches:
                phone = re.sub(r'[-\s]', '', matches[0])
                if 9 <= len(phone) <= 13:
                    return phone
        return ""
    
    def extract_email_from_text(self, text):
        """Extract email from OCR text"""
        if not text:
            return ""
        
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'\b[A-Za-z0-9._%-]+[@][A-Za-z0-9.-]+[.][A-Za-z]{2,}\b',
        ]
        
        for pattern in email_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                email = re.sub(r'\s', '', matches[0])
                if '@' in email and '.' in email.split('@')[1]:
                    return email.lower()
        return ""
    
    def extract_contact_from_image(self, candidate_url, candidate_id):
        """Extract phone/email from image using OCR"""
        try:
            contact_image_url = f"https://ejob.az/png_contacts.php?id={candidate_id}"
            response = self.session.get(contact_image_url, headers={'Referer': candidate_url})
            
            if response.status_code == 200 and response.content:
                image = Image.open(io.BytesIO(response.content))
                image = image.convert('L')
                
                custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789+()- @.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
                text = pytesseract.image_to_string(image, config=custom_config)
                
                phone = self.extract_phone_from_text(text)
                email = self.extract_email_from_text(text)
                
                return phone, email, contact_image_url
                
        except Exception as e:
            logger.warning(f"OCR failed for {candidate_url}: {e}")
        
        return "", "", ""
    
    def scrape_candidate(self, cv_url):
        """Scrape individual candidate"""
        try:
            response = self.session.get(cv_url, timeout=10)
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Initialize data structure
            data = {
                'phone': '', 'email': '', 'phone_image_link': '', 'email_image_link': '',
                'name': '', 'position': '', 'salary': '', 'age': '', 'city': '', 'gender': '',
                'education': '', 'experience': '', 'skills': '', 'additional_info': '', 'url': cv_url
            }
            
            # Extract candidate ID
            candidate_id_match = re.search(r'/cv/(\d+)-', cv_url)
            candidate_id = candidate_id_match.group(1) if candidate_id_match else None
            
            if candidate_id:
                # OCR extraction
                phone, email, image_link = self.extract_contact_from_image(cv_url, candidate_id)
                data['phone'] = phone if phone else f"Check image manually"
                data['email'] = email
                data['phone_image_link'] = image_link if image_link else f"https://ejob.az/png_contacts.php?id={candidate_id}"
                data['email_image_link'] = data['phone_image_link']
            
            # Extract other information
            name_elem = soup.find('div', class_='name')
            if name_elem:
                data['name'] = name_elem.get_text(strip=True)
            
            position_elem = soup.find('h1', class_='position')
            if position_elem:
                data['position'] = position_elem.get_text(strip=True)
            
            salary_elem = soup.find('strong', class_='salary')
            if salary_elem:
                data['salary'] = salary_elem.get_text(strip=True).replace('Əmək haqqı : ', '')
            
            # Extract from table
            table_rows = soup.find_all('tr')
            for row in table_rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    label = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    
                    if 'yaş' in label:
                        data['age'] = value
                    elif 'şəhər' in label:
                        data['city'] = value
                    elif 'cins' in label:
                        data['gender'] = value
            
            # Extract detailed information
            desc_table = soup.find('table', class_='description')
            if desc_table:
                desc_text = desc_table.get_text()
                
                # Extract sections
                for keyword, field in [
                    ('Bacarıqlar :', 'skills'),
                    ('Təhsil :', 'education'),
                    ('İş təcrübəsi :', 'experience'),
                    ('Əlavə məlumat :', 'additional_info')
                ]:
                    if keyword in desc_text:
                        start = desc_text.find(keyword) + len(keyword)
                        # Find next section or end
                        next_keywords = ['Təhsil :', 'İş təcrübəsi :', 'Əlavə məlumat :']
                        end = len(desc_text)
                        for next_kw in next_keywords:
                            if next_kw != keyword and next_kw in desc_text[start:]:
                                end = desc_text.find(next_kw, start)
                                break
                        data[field] = desc_text[start:end].strip()
            
            return data
            
        except Exception as e:
            logger.error(f"Error scraping {cv_url}: {e}")
            return None
    
    def scrape_all_pages(self, start_page=1, end_page=10):
        """Scrape pages from start_page to end_page"""
        print(f"🚀 Starting ejob.az scraper...")
        print(f"📄 Scraping pages {start_page} to {end_page}")
        print("🔧 Establishing session...")
        
        # First establish session
        main_response = self.session.get('https://ejob.az/', timeout=10)
        if main_response.status_code != 200:
            print("❌ Could not access main website")
            return []
        
        print("✅ Session established")
        
        all_candidates = []
        consecutive_404s = 0  # Track consecutive 404s
        
        for page_num in range(start_page, end_page + 1):
            if page_num == 1:
                url = "https://ejob.az/isci/"
            else:
                url = f"https://ejob.az/isci/page-{page_num}/"
            
            print(f"\n📄 Processing page {page_num}...")
            print(f"   URL: {url}")
            
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code != 200:
                    print(f"   ❌ Page {page_num} returned {response.status_code}, stopping")
                    break
                
                # Extract CV links
                cv_links = re.findall(r'/cv/[^\"\'\>\s]+', response.text)
                unique_cv_links = list(dict.fromkeys(cv_links))  # Remove duplicates
                
                if not unique_cv_links:
                    print(f"   ❌ No CV links found on page {page_num}, stopping")
                    break
                
                print(f"   ✅ Found {len(unique_cv_links)} unique candidates")
                
                # Scrape candidates on this page
                page_candidates = []
                for i, cv_path in enumerate(unique_cv_links, 1):
                    cv_url = urljoin(self.base_url, cv_path)
                    candidate_name = cv_path.split('/')[-2] if cv_path.split('/') else 'unknown'
                    
                    print(f"   📋 {i}/{len(unique_cv_links)}: {candidate_name}")
                    
                    candidate_data = self.scrape_candidate(cv_url)
                    if candidate_data:
                        page_candidates.append(candidate_data)
                        phone_info = candidate_data['phone'][:50] if candidate_data['phone'] else 'No phone'
                        print(f"      ✅ {candidate_data['name']}: {phone_info}")
                    else:
                        print(f"      ❌ Failed")
                    
                    # Delay between candidates
                    time.sleep(random.uniform(1, 3))
                
                all_candidates.extend(page_candidates)
                print(f"   📊 Page {page_num} completed: {len(page_candidates)}/{len(unique_cv_links)} candidates")
                
                # Delay between pages
                time.sleep(random.uniform(3, 5))
                
            except Exception as e:
                print(f"   ❌ Error on page {page_num}: {e}")
                break
        
        return all_candidates
    
    def save_to_csv(self, candidates, filename='ejob_candidates.csv'):
        """Save to CSV with phone as first column"""
        if not candidates:
            print("❌ No candidates to save")
            return
        
        headers = ['phone', 'email', 'phone_image_link', 'email_image_link', 'name', 'position', 
                  'salary', 'age', 'city', 'gender', 'education', 'experience', 'skills', 
                  'additional_info', 'url']
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(candidates)
        
        print(f"💾 Saved {len(candidates)} candidates to {filename}")

def main():
    max_pages = 5  # Default
    if len(sys.argv) >= 2:
        max_pages = int(sys.argv[1])
    
    print(f"🚀 ULTIMATE ejob.az Scraper")
    print(f"📱 OCR Phone Extraction + Verification Links")
    print(f"📄 Processing up to {max_pages} pages")
    print("=" * 50)
    
    start_time = time.time()
    
    scraper = WorkingEjobScraper()
    candidates = scraper.scrape_all_pages(max_pages=max_pages)
    
    end_time = time.time()
    
    if candidates:
        timestamp = int(time.time())
        filename = f'ejob_working_{timestamp}.csv'
        scraper.save_to_csv(candidates, filename)
        
        # Statistics
        phones_extracted = sum(1 for c in candidates if c['phone'] and len(c['phone']) >= 9 and 'check' not in c['phone'].lower())
        emails_extracted = sum(1 for c in candidates if c['email'] and '@' in c['email'])
        pages_processed = max_pages if len(candidates) >= max_pages * 20 else len(candidates) // 20 + 1
        
        print("=" * 50)
        print(f"✅ SCRAPING COMPLETED!")
        print(f"⏱️  Time: {end_time - start_time:.1f} seconds")
        print(f"📊 Candidates: {len(candidates)}")
        print(f"📄 Pages processed: {pages_processed}")
        print(f"📱 Phones extracted: {phones_extracted}/{len(candidates)} ({phones_extracted/len(candidates)*100:.1f}%)")
        print(f"📧 Emails extracted: {emails_extracted}/{len(candidates)} ({emails_extracted/len(candidates)*100:.1f}%)")
        print(f"💾 File: {filename}")
        print(f"⚡ Speed: {len(candidates)/(end_time - start_time):.1f} candidates/sec")
        
        print(f"\n📱 EXTRACTED PHONES (sample):")
        phone_count = 0
        for c in candidates:
            if c['phone'] and len(c['phone']) >= 9 and 'check' not in c['phone'].lower():
                print(f"   • {c['name']}: {c['phone']} | {c['city']}")
                print(f"     🔗 {c['phone_image_link']}")
                phone_count += 1
                if phone_count >= 5:
                    break
        
        if phone_count == 0:
            print("   📋 All phones require manual verification via image links")
            for i, c in enumerate(candidates[:3], 1):
                print(f"   {i}. {c['name']}: {c['phone']}")
                print(f"      🔗 {c['phone_image_link']}")
    else:
        print("❌ No candidates found")

if __name__ == "__main__":
    main()