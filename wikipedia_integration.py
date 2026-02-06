"""
Wikipedia Integration Module
Menghubungkan chatbot dengan Wikipedia untuk mendapatkan informasi real-time
"""

import requests
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import quote


class WikipediaSearcher:
    """Searcher untuk Wikipedia dengan local caching"""
    
    def __init__(self, cache_dir: str = None, language: str = "id"):
        """
        Inisialisasi Wikipedia searcher
        
        Args:
            cache_dir: Direktori untuk cache Wikipedia
            language: Bahasa Wikipedia (id, en, dll)
        """
        if cache_dir is None:
            cache_dir = Path(__file__).parent / "data" / "wikipedia_cache"
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.language = language
        self.api_url = f"https://{language}.wikipedia.org/w/api.php"
        self.search_cache = {}
        self.cache_file = self.cache_dir / "wiki_search_cache.json"
        
        self.load_cache()
    
    def load_cache(self):
        """Load cache dari file"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.search_cache = json.load(f)
                print(f"✓ Loaded Wikipedia cache dengan {len(self.search_cache)} entries")
        except Exception as e:
            print(f"⚠ Error loading Wikipedia cache: {e}")
            self.search_cache = {}
    
    def save_cache(self):
        """Simpan cache ke file"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.search_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠ Error saving Wikipedia cache: {e}")
    
    def search_wikipedia(self, query: str, timeout: int = 10, use_cache: bool = True) -> Optional[Dict]:
        """
        Cari informasi di Wikipedia
        
        Args:
            query: Query pencarian
            timeout: Timeout dalam detik
            use_cache: Gunakan cache jika ada
        
        Returns:
            Dict dengan informasi atau None
        """
        query_lower = query.lower().strip()
        
        # Check cache dulu
        if use_cache and query_lower in self.search_cache:
            print(f"✓ Using cached Wikipedia data untuk '{query}'")
            return self.search_cache[query_lower]
        
        try:
            print(f"📖 Searching Wikipedia untuk '{query}'...")
            
            # Step 1: Search untuk page
            search_params = {
                'action': 'query',
                'list': 'search',
                'srsearch': query,
                'format': 'json',
                'srlimit': 3
            }
            
            response = requests.get(self.api_url, params=search_params, timeout=timeout)
            response.raise_for_status()
            search_results = response.json()
            
            if not search_results.get('query', {}).get('search'):
                print(f"⚠ Tidak ada hasil untuk '{query}' di Wikipedia")
                return None
            
            # Get first result title
            page_title = search_results['query']['search'][0]['title']
            
            # Step 2: Get page content
            content_params = {
                'action': 'query',
                'titles': page_title,
                'prop': 'extracts|pageprops',
                'explaintext': True,
                'exintro': True,
                'format': 'json'
            }
            
            content_response = requests.get(self.api_url, params=content_params, timeout=timeout)
            content_response.raise_for_status()
            content_data = content_response.json()
            
            # Extract page data
            pages = content_data.get('query', {}).get('pages', {})
            page_data = list(pages.values())[0] if pages else {}
            
            if 'extract' not in page_data:
                print(f"⚠ Tidak bisa mendapatkan konten dari '{page_title}'")
                return None
            
            # Build result
            result = {
                'title': page_title,
                'summary': page_data['extract'][:500],  # First 500 chars
                'full_content': page_data['extract'],
                'url': f"https://{self.language}.wikipedia.org/wiki/{quote(page_title)}",
                'cached_at': datetime.now().isoformat(),
                'source': 'wikipedia'
            }
            
            # Cache result
            self.search_cache[query_lower] = result
            self.save_cache()
            
            print(f"✓ Found: {page_title}")
            return result
        
        except requests.exceptions.Timeout:
            print(f"⚠ Wikipedia timeout - coba offline atau check internet")
            return None
        except requests.exceptions.ConnectionError:
            print(f"⚠ Wikipedia tidak terhubung - gunakan cache atau offline mode")
            return None
        except Exception as e:
            print(f"⚠ Error searching Wikipedia: {e}")
            return None
    
    def get_summary(self, query: str) -> str:
        """
        Dapatkan ringkasan singkat dari Wikipedia
        
        Args:
            query: Topik yang dicari
        
        Returns:
            Ringkasan dalam bentuk string
        """
        result = self.search_wikipedia(query)
        
        if not result:
            return f"Maaf, saya tidak bisa menemukan informasi tentang '{query}' di Wikipedia"
        
        summary = result['summary']
        url = result['url']
        
        return f"""
📖 {result['title']}
{'='*50}
{summary}

Sumber: Wikipedia
Baca lebih lanjut: {url}
"""
    
    def search_multiple(self, queries: List[str]) -> Dict[str, Optional[Dict]]:
        """
        Cari multiple queries sekaligus
        
        Args:
            queries: List of queries
        
        Returns:
            Dict dengan results untuk setiap query
        """
        results = {}
        for query in queries:
            results[query] = self.search_wikipedia(query)
        return results
    
    def get_cache_stats(self) -> Dict:
        """Dapatkan statistik cache Wikipedia"""
        return {
            'total_cached_pages': len(self.search_cache),
            'cache_file_size_kb': self.cache_file.stat().st_size / 1024 if self.cache_file.exists() else 0,
            'language': self.language,
            'cache_location': str(self.cache_file)
        }
    
    def clear_cache(self):
        """Hapus semua cache Wikipedia"""
        self.search_cache = {}
        if self.cache_file.exists():
            self.cache_file.unlink()
        print("✓ Wikipedia cache cleared")
    
    def export_cache(self, output_path: str = None) -> str:
        """
        Export cache ke file
        
        Args:
            output_path: Path untuk export
        
        Returns:
            Path file yang di-export
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.cache_dir / f"wikipedia_cache_export_{timestamp}.json"
        else:
            output_path = Path(output_path)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.search_cache, f, ensure_ascii=False, indent=2)
            print(f"✓ Wikipedia cache exported to: {output_path}")
            return str(output_path)
        except Exception as e:
            print(f"✗ Error exporting cache: {e}")
            return None


class QuestionAnswerer:
    """AI Question Answerer dengan Wikipedia backend"""
    
    def __init__(self, wikipedia_searcher: WikipediaSearcher = None):
        """
        Inisialisasi Question Answerer
        
        Args:
            wikipedia_searcher: Instance WikipediaSearcher
        """
        self.wiki = wikipedia_searcher or WikipediaSearcher()
        self.question_history = []
    
    def answer_question(self, question: str) -> str:
        """
        Jawab pertanyaan dengan informasi dari Wikipedia
        
        Args:
            question: Pertanyaan yang diajukan
        
        Returns:
            Jawaban berdasarkan Wikipedia
        """
        # Save history
        self.question_history.append({
            'question': question,
            'timestamp': datetime.now().isoformat()
        })
        
        # Extract topic dari question
        # Simple extraction: ambil kata-kata penting
        stop_words = ['apa', 'siapa', 'bagaimana', 'mengapa', 'kapan', 'di mana', 'yang', 'itu', 'adalah', 'ada']
        words = question.lower().split()
        topic_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        if not topic_words:
            return "Maaf, pertanyaanmu terlalu umum. Coba tanya tentang topik spesifik."
        
        # Search di Wikipedia
        topic = ' '.join(topic_words[:3])  # Ambil 3 kata pertama
        wiki_result = self.wiki.search_wikipedia(topic)
        
        if not wiki_result:
            return f"Maaf, saya tidak bisa menemukan informasi tentang '{topic}' di Wikipedia. Coba pertanyaan lain."
        
        # Format answer
        answer = f"""
📚 Pertanyaan: {question}
{'='*50}

{wiki_result['summary']}

📖 Dari: Wikipedia - {wiki_result['title']}
🔗 Baca lebih lanjut: {wiki_result['url']}
"""
        
        return answer
    
    def get_question_history(self, limit: int = 10) -> List[Dict]:
        """Dapatkan history pertanyaan"""
        return self.question_history[-limit:]
    
    def clear_history(self):
        """Hapus history pertanyaan"""
        self.question_history = []


class KnowledgeBase:
    """Combined Knowledge Base: Vocabulary + Wikipedia"""
    
    def __init__(self, vocab_manager=None, wiki_searcher: WikipediaSearcher = None):
        """
        Inisialisasi Knowledge Base
        
        Args:
            vocab_manager: OnlineVocabularyManager instance
            wiki_searcher: WikipediaSearcher instance
        """
        self.vocab_manager = vocab_manager
        self.wiki = wiki_searcher or WikipediaSearcher()
        self.answerer = QuestionAnswerer(self.wiki)
    
    def search_all(self, query: str) -> Dict:
        """
        Cari di semua knowledge source (vocab + wiki)
        
        Args:
            query: Query untuk dicari
        
        Returns:
            Combined results
        """
        results = {
            'query': query,
            'vocabulary_results': [],
            'wikipedia_results': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Search vocabulary
        if self.vocab_manager:
            vocab_results = self.vocab_manager.search_vocabulary(query, limit=3)
            results['vocabulary_results'] = vocab_results
        
        # Search Wikipedia
        wiki_result = self.wiki.search_wikipedia(query)
        if wiki_result:
            results['wikipedia_results'] = wiki_result
        
        return results
    
    def get_comprehensive_answer(self, question: str) -> str:
        """
        Jawab pertanyaan dengan kombinasi vocabulary + Wikipedia
        
        Args:
            question: Pertanyaan
        
        Returns:
            Comprehensive answer
        """
        answer = f"🤖 Jawaban untuk: {question}\n"
        answer += "="*50 + "\n\n"
        
        # Try Wikipedia first
        wiki_answer = self.answerer.answer_question(question)
        if "Maaf" not in wiki_answer:
            answer += wiki_answer
            return answer
        
        # Fallback ke vocabulary
        if self.vocab_manager:
            topic_words = question.lower().split()
            stop_words = ['apa', 'siapa', 'bagaimana', 'mengapa', 'kapan', 'di mana']
            keywords = [w for w in topic_words if w not in stop_words]
            
            if keywords:
                vocab_results = self.vocab_manager.search_vocabulary(' '.join(keywords[:2]), limit=5)
                if vocab_results:
                    answer += "📚 Dari Vocabulary:\n"
                    for result in vocab_results:
                        answer += f"\n• {result['word'].upper()}\n"
                        answer += f"  Definition: {result.get('definition', 'N/A')}\n"
                    return answer
        
        return wiki_answer


# Demo dan testing
if __name__ == "__main__":
    print("="*60)
    print("WIKIPEDIA INTEGRATION - Demo")
    print("="*60)
    
    # Test Wikipedia Searcher
    print("\n1️⃣ Testing Wikipedia Searcher...")
    wiki = WikipediaSearcher(language="id")
    
    # Search test
    result = wiki.search_wikipedia("Algoritma", timeout=10)
    if result:
        print(f"\nFound: {result['title']}")
        print(f"Summary: {result['summary'][:200]}...")
    
    # Question Answerer
    print("\n2️⃣ Testing Question Answerer...")
    answerer = QuestionAnswerer(wiki)
    answer = answerer.answer_question("Apa itu algoritma?")
    print(answer)
    
    # Cache stats
    print("\n3️⃣ Cache Statistics...")
    stats = wiki.get_cache_stats()
    for key, value in stats.items():
        print(f"  • {key}: {value}")
