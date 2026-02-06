"""
Online Vocabulary Manager dengan Local Caching
Menyinkronkan vocabulary dari online dan menyimpan lokal untuk penggunaan offline
"""

import json
import os
import requests
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import time

class OnlineVocabularyManager:
    """Manager untuk vocabulary online dengan local cache"""
    
    def __init__(self, cache_dir: str = None, online_sources: List[str] = None):
        """
        Inisialisasi vocabulary manager
        
        Args:
            cache_dir: Direktori untuk menyimpan cache
            online_sources: List URL untuk fetch vocabulary
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent / "data" / "vocabulary_cache"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.vocabulary = {}
        self.cache_metadata = {}
        self.online_sources = online_sources or self._get_default_sources()
        
        self.cache_file = self.cache_dir / "vocabulary_cache.json"
        self.metadata_file = self.cache_dir / "cache_metadata.json"
        
        self.load_cache()
    
    def _get_default_sources(self) -> List[str]:
        """Sumber vocabulary online default"""
        return [
            "https://raw.githubusercontent.com/wisnu4138/id-vocab/main/vocab.json",
            "https://api.github.com/repos/wisnu4138/id-vocab/contents/vocab.json"
        ]
    
    def load_cache(self):
        """Load vocabulary dari cache lokal"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.vocabulary = json.load(f)
                print(f"✓ Loaded {len(self.vocabulary)} vocabulary dari cache lokal")
            
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    self.cache_metadata = json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
            self.vocabulary = {}
            self.cache_metadata = {}
    
    def save_cache(self):
        """Simpan vocabulary ke cache lokal"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)
            
            self.cache_metadata['last_updated'] = datetime.now().isoformat()
            self.cache_metadata['vocab_count'] = len(self.vocabulary)
            
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_metadata, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Cache disimpan: {len(self.vocabulary)} vocabulary")
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def fetch_online(self, timeout: int = 10) -> bool:
        """
        Fetch vocabulary dari sumber online
        
        Args:
            timeout: Timeout untuk request dalam detik
        
        Returns:
            True jika sukses, False jika gagal
        """
        print("\n📡 Mencoba fetch vocabulary dari online...")
        
        for source in self.online_sources:
            try:
                print(f"  → Mencoba: {source}")
                response = requests.get(source, timeout=timeout)
                response.raise_for_status()
                
                data = response.json()
                
                # Handle GitHub API response
                if isinstance(data, dict) and 'content' in data:
                    import base64
                    content = base64.b64decode(data['content']).decode('utf-8')
                    data = json.loads(content)
                
                self.vocabulary.update(data)
                self.save_cache()
                print(f"  ✓ Berhasil fetch dari: {source}")
                print(f"  → Total vocabulary sekarang: {len(self.vocabulary)}")
                return True
            
            except requests.exceptions.Timeout:
                print(f"  ✗ Timeout (cache lokal masih digunakan)")
            except requests.exceptions.ConnectionError:
                print(f"  ✗ Koneksi gagal (cache lokal masih digunakan)")
            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
        
        print("\n⚠ Tidak bisa fetch dari online, menggunakan cache lokal")
        return False
    
    def merge_vocabulary(self, new_vocab: Dict):
        """Merge vocabulary baru dengan yang ada"""
        self.vocabulary.update(new_vocab)
        self.save_cache()
    
    def add_vocabulary(self, word: str, definition: str, examples: List[str] = None, 
                       part_of_speech: str = None):
        """
        Tambah vocabulary baru
        
        Args:
            word: Kata yang ditambah
            definition: Definisi
            examples: Contoh penggunaan
            part_of_speech: Jenis kata (noun, verb, dll)
        """
        self.vocabulary[word.lower()] = {
            "definition": definition,
            "examples": examples or [],
            "part_of_speech": part_of_speech,
            "added_date": datetime.now().isoformat(),
            "source": "local"
        }
        self.save_cache()
    
    def search_vocabulary(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Cari vocabulary yang sesuai dengan query
        
        Args:
            query: Kata yang dicari
            limit: Jumlah hasil maksimal
        
        Returns:
            List hasil pencarian
        """
        query_lower = query.lower()
        results = []
        
        # Exact match
        if query_lower in self.vocabulary:
            results.append({
                "word": query_lower,
                "match_type": "exact",
                **self.vocabulary[query_lower]
            })
        
        # Partial match
        for word, data in self.vocabulary.items():
            if query_lower in word and word != query_lower:
                results.append({
                    "word": word,
                    "match_type": "partial",
                    **data
                })
            
            if len(results) >= limit:
                break
        
        return results
    
    def get_vocabulary_stats(self) -> Dict:
        """Dapatkan statistik vocabulary"""
        total = len(self.vocabulary)
        local_vocab = sum(1 for v in self.vocabulary.values() if v.get("source") == "local")
        
        return {
            "total_vocabulary": total,
            "local_vocabulary": local_vocab,
            "online_vocabulary": total - local_vocab,
            "last_updated": self.cache_metadata.get("last_updated", "Belum pernah"),
            "cache_size_mb": os.path.getsize(self.cache_file) / 1024 / 1024 if self.cache_file.exists() else 0
        }
    
    def sync_with_online(self, force: bool = False, cache_hours: int = 24) -> bool:
        """
        Sinkronisasi dengan online jika diperlukan
        
        Args:
            force: Force sync meskipun ada cache
            cache_hours: Jam sebelum cache dianggap kadaluarsa
        
        Returns:
            True jika berhasil
        """
        last_updated = self.cache_metadata.get("last_updated")
        
        if not force and last_updated:
            try:
                last_time = datetime.fromisoformat(last_updated)
                if datetime.now() - last_time < timedelta(hours=cache_hours):
                    print(f"✓ Cache masih fresh (updated {(datetime.now() - last_time).seconds} seconds ago)")
                    return True
            except:
                pass
        
        return self.fetch_online()
    
    def export_vocabulary(self, format: str = "json", output_path: str = None) -> str:
        """
        Export vocabulary ke berbagai format
        
        Args:
            format: Format export (json, csv, txt)
            output_path: Path untuk file output
        
        Returns:
            Path file yang di-export
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.cache_dir / f"vocabulary_export_{timestamp}.{format}"
        else:
            output_path = Path(output_path)
        
        if format == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)
        
        elif format == "csv":
            import csv
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Word", "Definition", "Part of Speech", "Examples"])
                for word, data in self.vocabulary.items():
                    examples = " | ".join(data.get("examples", []))
                    writer.writerow([
                        word,
                        data.get("definition", ""),
                        data.get("part_of_speech", ""),
                        examples
                    ])
        
        elif format == "txt":
            with open(output_path, 'w', encoding='utf-8') as f:
                for word, data in sorted(self.vocabulary.items()):
                    f.write(f"\n{'='*50}\n")
                    f.write(f"WORD: {word.upper()}\n")
                    f.write(f"{'='*50}\n")
                    f.write(f"Definition: {data.get('definition', 'N/A')}\n")
                    if data.get('part_of_speech'):
                        f.write(f"Part of Speech: {data.get('part_of_speech')}\n")
                    if data.get('examples'):
                        f.write(f"Examples:\n")
                        for ex in data.get('examples', []):
                            f.write(f"  • {ex}\n")
        
        print(f"✓ Vocabulary di-export ke: {output_path}")
        return str(output_path)


class IntegrationHelper:
    """Helper untuk integrasi dengan robot_core.py"""
    
    @staticmethod
    def integrate_with_pattern_matcher(vocab_manager: OnlineVocabularyManager, 
                                       pattern_matcher_obj) -> None:
        """
        Integrasikan vocabulary manager dengan PatternMatcher
        
        Args:
            vocab_manager: Instansi OnlineVocabularyManager
            pattern_matcher_obj: Instansi PatternMatcher dari robot_core
        """
        # Tambahkan method baru ke PatternMatcher
        def search_vocabulary(query: str, limit: int = 5):
            results = vocab_manager.search_vocabulary(query, limit)
            return results
        
        # Attach method ke object
        pattern_matcher_obj.search_vocabulary = search_vocabulary
        pattern_matcher_obj.vocab_manager = vocab_manager


if __name__ == "__main__":
    # Test dan demo
    print("=" * 60)
    print("ONLINE VOCABULARY MANAGER - Demo")
    print("=" * 60)
    
    # Inisialisasi
    vocab_manager = OnlineVocabularyManager()
    
    # Sinkronisasi dengan online
    vocab_manager.sync_with_online(force=True)
    
    # Tambah vocabulary lokal
    vocab_manager.add_vocabulary(
        word="chatbot",
        definition="Program komputer yang dirancang untuk mensimulasikan percakapan",
        examples=[
            "Chatbot ini dapat membantu menjawab pertanyaan pelanggan",
            "Kami menggunakan chatbot untuk customer service"
        ],
        part_of_speech="noun"
    )
    
    # Cari vocabulary
    print("\n🔍 Mencari 'chat':")
    results = vocab_manager.search_vocabulary("chat", limit=3)
    for result in results:
        print(f"  • {result['word']}: {result.get('definition', 'N/A')}")
    
    # Statistik
    print("\n📊 Statistik Vocabulary:")
    stats = vocab_manager.get_vocabulary_stats()
    for key, value in stats.items():
        print(f"  • {key}: {value}")
    
    # Export
    print("\n💾 Export vocabulary...")
    vocab_manager.export_vocabulary("json")
    vocab_manager.export_vocabulary("csv")
