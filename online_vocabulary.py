"""
Online Vocabulary Manager with local caching and API support
Improved version with reliable data sources
"""

import json
import os
from pathlib import Path
from datetime import datetime, timedelta
import requests
from typing import List, Dict, Optional


class OnlineVocabularyManager:
    """Manager untuk online vocabulary dengan local cache"""
    
    def __init__(self, cache_dir: str = "vocabulary_cache"):
        """
        Inisialisasi vocabulary manager
        
        Args:
            cache_dir: Direktori untuk menyimpan cache vocabulary
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        self.local_vocab_file = self.cache_dir / "local_vocabulary.json"
        self.online_vocab_file = self.cache_dir / "online_vocabulary.json"
        self.sync_info_file = self.cache_dir / "sync_info.json"
        
        self.vocabulary = {}
        self.online_vocabulary = {}
        self.last_sync = None
        
        # API endpoint yang reliable
        self.api_base_url = "https://api.dictionaryapi.dev/api/v2/entries/english/"
        
        # Load vocabulary dari cache
        self._load_vocabulary()
        print(f"✓ Loaded {len(self.vocabulary)} vocabulary dari cache lokal")
    
    def _load_vocabulary(self) -> None:
        """Load vocabulary dari local cache"""
        # Load local vocabulary
        if self.local_vocab_file.exists():
            try:
                with open(self.local_vocab_file, 'r', encoding='utf-8') as f:
                    self.vocabulary = json.load(f)
            except json.JSONDecodeError:
                self.vocabulary = {}
        
        # Load online vocabulary
        if self.online_vocab_file.exists():
            try:
                with open(self.online_vocab_file, 'r', encoding='utf-8') as f:
                    self.online_vocabulary = json.load(f)
            except json.JSONDecodeError:
                self.online_vocabulary = {}
        
        # Load sync info
        if self.sync_info_file.exists():
            try:
                with open(self.sync_info_file, 'r', encoding='utf-8') as f:
                    sync_info = json.load(f)
                    self.last_sync = sync_info.get('last_sync')
            except json.JSONDecodeError:
                self.last_sync = None
    
    def _save_vocabulary(self) -> None:
        """Save vocabulary ke cache"""
        with open(self.local_vocab_file, 'w', encoding='utf-8') as f:
            json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)
    
    def _save_online_vocabulary(self) -> None:
        """Save online vocabulary ke cache"""
        with open(self.online_vocab_file, 'w', encoding='utf-8') as f:
            json.dump(self.online_vocabulary, f, ensure_ascii=False, indent=2)
    
    def _save_sync_info(self) -> None:
        """Save sync information"""
        sync_info = {
            'last_sync': self.last_sync,
            'timestamp': datetime.now().isoformat()
        }
        with open(self.sync_info_file, 'w', encoding='utf-8') as f:
            json.dump(sync_info, f, indent=2)
    
    def add_vocabulary(self, word: str, definition: str, 
                      examples: List[str] = None, 
                      part_of_speech: str = None) -> None:
        """
        Tambah vocabulary ke local storage
        
        Args:
            word: Kata yang ditambahkan
            definition: Definisi kata
            examples: Contoh penggunaan
            part_of_speech: Jenis kata (noun, verb, dll)
        """
        word_lower = word.lower().strip()
        
        self.vocabulary[word_lower] = {
            'word': word,
            'definition': definition,
            'examples': examples or [],
            'part_of_speech': part_of_speech,
            'added_date': datetime.now().isoformat(),
            'source': 'local'
        }
        
        self._save_vocabulary()
    
    def search_vocabulary(self, search_term: str, limit: int = 5) -> List[Dict]:
        """ 
        Cari vocabulary dari cache (local + online) 
        
        Args:
            search_term: Kata yang dicari
            limit: Jumlah hasil maksimal 
        
        Returns:
            List dari vocabulary results
        """ 
        search_term_lower = search_term.lower().strip()
        results = []
        
        # Cari di local vocabulary
        for word_key, word_data in self.vocabulary.items():
            if search_term_lower in word_key or search_term_lower in word_data.get('definition', '').lower():
                results.append(word_data)
        
        # Cari di online vocabulary
        for word_key, word_data in self.online_vocabulary.items():
            if search_term_lower in word_key or search_term_lower in str(word_data).lower():
                if word_data not in results:
                    results.append(word_data)
        
        return results[:limit]
    
    def fetch_from_api(self, word: str) -> Optional[Dict]:
        """ 
        Fetch vocabulary dari Dictionary API 
        
        Args:
            word: Kata yang dicari 
        
        Returns:
            Dictionary dengan data vocabulary atau None jika gagal 
        """ 
        word_lower = word.lower().strip()
        
        # Cek apakah sudah ada di cache
        if word_lower in self.online_vocabulary:
            return self.online_vocabulary[word_lower]
        
        try:
            full_url = self.api_base_url + word_lower
            response = requests.get(full_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list) and len(data) > 0:
                    word_data = data[0]
                    
                    vocab_entry = {
                        'word': word_data.get('word', word),
                        'definition': self._extract_definition(word_data),
                        'examples': self._extract_examples(word_data),
                        'part_of_speech': self._extract_part_of_speech(word_data),
                        'pronunciation': word_data.get('phonetic', ''),
                        'source': 'api',
                        'fetched_date': datetime.now().isoformat()
                    }
                    
                    # Cache the result
                    self.online_vocabulary[word_lower] = vocab_entry
                    self._save_online_vocabulary()
                    
                    return vocab_entry
            
            elif response.status_code == 404:
                return None
        
        except requests.Timeout:
            print(f"⏱ Timeout fetching '{word}'")
            return None
        except requests.RequestException as e:
            print(f"❌ Error fetching '{word}': {str(e)}")
            return None
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response for '{word}'")
            return None
        
        return None
    
    def _extract_definition(self, word_data: Dict) -> str:
        """Extract definition dari Dictionary API response""" 
        if 'meanings' in word_data and len(word_data['meanings']) > 0:
            meanings = word_data['meanings']
            if 'definitions' in meanings[0] and len(meanings[0]['definitions']) > 0:
                return meanings[0]['definitions'][0].get('definition', 'N/A')
        return 'N/A' 
    
    def _extract_examples(self, word_data: Dict) -> List[str]:
        """Extract examples dari Dictionary API response""" 
        examples = []
        if 'meanings' in word_data:
            for meaning in word_data['meanings']:
                if 'definitions' in meaning:
                    for definition in meaning['definitions']:
                        if 'example' in definition:
                            examples.append(definition['example'])
                            if len(examples) >= 2:
                                return examples
        return examples
    
    def _extract_part_of_speech(self, word_data: Dict) -> str:
        """Extract part of speech dari Dictionary API response""" 
        if 'meanings' in word_data and len(word_data['meanings']) > 0:
            return word_data['meanings'][0].get('partOfSpeech', 'N/A')
        return 'N/A'
    
    def sync_with_online(self, force: bool = False, cache_hours: int = 24) -> bool:
        """ 
        Sinkronisasi vocabulary dengan online sources 
        
        Args:
            force: Force sync meskipun baru saja di-sync 
            cache_hours: Jam sebelum sync lagi 
        
        Returns:
            True jika sync berhasil, False jika gagal 
        """ 
        if not force and self.last_sync:
            last_sync_time = datetime.fromisoformat(self.last_sync)
            if datetime.now() - last_sync_time < timedelta(hours=cache_hours):
                return True
        
        print("\n🔄 Sinkronisasi vocabulary dengan online...")
        print("⏳ Fetching vocabulary dari API...\n")
        
        popular_words = [
            'hello', 'world', 'algorithm', 'programming', 'computer',
            'technology', 'function', 'variable', 'data', 'structure',
            'learning', 'development', 'software', 'hardware', 'network',
            'internet', 'database', 'server', 'client', 'request'
        ]
        
        synced_count = 0
        failed_count = 0
        
        for word in popular_words:
            try:
                result = self.fetch_from_api(word)
                if result:
                    synced_count += 1
                    print(f"  ✓ '{word}' - synced")
                else:
                    failed_count += 1
            except Exception as e:
                failed_count += 1
        
        self.last_sync = datetime.now().isoformat()
        self._save_sync_info()
        
        print(f"\n✓ Sync selesai: {synced_count} berhasil, {failed_count} gagal")
        return synced_count > 0
    
    def get_vocabulary_stats(self) -> Dict:
        """Get statistik vocabulary"""
        return {
            'total_vocabulary': len(self.vocabulary) + len(self.online_vocabulary),
            'local_vocabulary': len(self.vocabulary),
            'online_vocabulary': len(self.online_vocabulary),
            'last_updated': self.last_sync or 'Never',
            'cache_size_mb': self._get_cache_size(),
            'cache_location': str(self.cache_dir)
        }
    
    def _get_cache_size(self) -> float:
        """Hitung ukuran cache dalam MB"""
        total_size = 0
        if self.cache_dir.exists():
            for file in self.cache_dir.glob('*.json'):
                total_size += file.stat().st_size
        return total_size / (1024 * 1024)
    
    def export_vocabulary(self, format: str = "json", output_path: str = None) -> str:
        """ 
        Export vocabulary ke file 
        
        Args:
            format: Format export (json, csv, txt) 
            output_path: Path output file 
        
        Returns:
            Path file yang di-export 
        """ 
        all_vocab = {**self.vocabulary, **self.online_vocabulary}
        
        if output_path is None:
            output_path = f"vocabulary_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if format == "json":
            output_file = f"{output_path}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_vocab, f, ensure_ascii=False, indent=2)
        
        elif format == "csv":
            output_file = f"{output_path}.csv"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Word,Definition,Part of Speech,Source,Examples\n")
                for word, data in all_vocab.items():
                    examples = '; '.join(data.get('examples', []))
                    f.write(f"{data.get('word', word)},\"{data.get('definition', '')}\",")
                    f.write(f"{data.get('part_of_speech', '')},{data.get('source', '')},\"{examples}\"\n")
        
        elif format == "txt":
            output_file = f"{output_path}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                for word, data in all_vocab.items():
                    f.write(f"\n{'='*50}\n")
                    f.write(f"WORD: {data.get('word', word)}\n")
                    f.write(f"DEFINITION: {data.get('definition', 'N/A')}\n")
                    f.write(f"PART OF SPEECH: {data.get('part_of_speech', 'N/A')}\n")
                    if data.get('examples'):
                        f.write(f"EXAMPLES:\n")
                        for example in data['examples']:
                            f.write(f"  - {example}\n")
        
        return output_file


class IntegrationHelper:
    """Helper class untuk integrasi vocabulary dengan pattern matcher""" 
    
    @staticmethod
    def integrate_with_pattern_matcher(vocab_manager: OnlineVocabularyManager, 
                                      pattern_matcher) -> None:
        """ 
        Integrate vocabulary manager dengan pattern matcher robot 
        
        Args:
            vocab_manager: Instance dari OnlineVocabularyManager
            pattern_matcher: Pattern matcher dari robot 
        """ 
        pattern_matcher.vocab_manager = vocab_manager