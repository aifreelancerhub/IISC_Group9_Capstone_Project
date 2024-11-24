import PyPDF2
import os
from typing import Dict, List
import json

class PDFService:
    def __init__(self):
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.data_dir = os.path.join(current_dir, "Data")
        self.cache_file = os.path.join(current_dir, "BackEnd", "cache", "pdf_cache.json")
        self.processed_data = self._load_cache() or self._process_pdfs()
    
    def _load_cache(self) -> Dict:
        """Load processed data from cache if it exists"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return None

    def _save_cache(self):
        """Save processed data to cache"""
        os.makedirs(os.path.dirname(self.cache_file), exist_ok=True)
        with open(self.cache_file, 'w') as f:
            json.dump(self.processed_data, f)

    def _process_pdfs(self) -> Dict:
        """Process all PDFs and extract relevant information"""
        data = {}
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.pdf'):
                filepath = os.path.join(self.data_dir, filename)
                company_name = filename.split('.')[0]
                with open(filepath, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text()
                data[company_name] = {
                    'text': text,
                    'filename': filename,
                    'is_fundamental': '_fundamentals' in filename
                }
        
        self.processed_data = data  # Ensure processed_data is set
        self._save_cache()  # Save to cache
        return data

    def get_company_data(self, company_name: str) -> Dict:
        """Get data for a specific company"""
        return self.processed_data.get(company_name, {})

    def get_all_companies(self) -> List[str]:
        """Get list of all companies"""
        companies = set()
        for company in self.processed_data.keys():
            base_name = company.replace('_fundamentals', '')
            companies.add(base_name)
        return list(companies)

    def get_fundamental_analysis(self, company_name: str) -> str:
        """Get fundamental analysis for a company"""
        fundamental_name = f"{company_name}_fundamentals"
        if fundamental_name in self.processed_data:
            return self.processed_data[fundamental_name].get('text', '')
        return ''

    def search_company_data(self, query: str) -> List[Dict]:
        """Search across all company data"""
        results = []
        for company, data in self.processed_data.items():
            if query.lower() in data['text'].lower():
                results.append({
                    'company': company,
                    'filename': data['filename'],
                    'is_fundamental': data['is_fundamental']
                })
        return results
