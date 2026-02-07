import requests
import time
import json
from pathlib import Path

class WikipediaSearcher:
    def __init__(self, language='en', user_agent=None):
        self.language = language
        self.user_agent = user_agent if user_agent else 'Mozilla/5.0'

        # cache structure: {'search': {query: data}, 'pages': {title: extract}}
        self.cache = {'search': {}, 'pages': {}}

        # Persisted cache directory and file
        self.cache_dir = Path('wiki_cache')
        try:
            self.cache_dir.mkdir(exist_ok=True)
        except Exception:
            pass
        self.cache_file = self.cache_dir / 'wiki_cache.json'

        # Load persisted cache if available
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        # merge with default structure
                        self.cache.get('search', {}).update(data.get('search', {}))
                        self.cache.get('pages', {}).update(data.get('pages', {}))
        except Exception:
            # ignore load errors
            pass

    def search(self, query):
        # Check persisted search cache first
        if query in self.cache.get('search', {}):
            return self.cache['search'][query]
        
        headers = {'User-Agent': self.user_agent}
        url = f'https://{self.language}.wikipedia.org/w/api.php'
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json'
        }
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            try:
                self.cache['search'][query] = data
                # persist cache
                with open(self.cache_file, 'w', encoding='utf-8') as f:
                    json.dump(self.cache, f, ensure_ascii=False)
            except Exception:
                pass
            return data
        else:
            return {'error': 'Failed to fetch data from Wikipedia'}

    def get_cache_stats(self):
        """Return simple statistics about the in-memory cache."""
        try:
            total_search = len(self.cache.get('search', {}))
            total_pages = len(self.cache.get('pages', {}))
            total_cached = total_search + total_pages

            # If cache file exists, use its size for a more accurate on-disk size
            if self.cache_file.exists():
                try:
                    size_bytes = self.cache_file.stat().st_size
                    size_kb = size_bytes / 1024.0
                except Exception:
                    size_kb = 0.0
                cache_location = str(self.cache_file)
            else:
                # Fallback estimate from in-memory serialization
                try:
                    size_bytes = len(json.dumps(self.cache).encode('utf-8'))
                    size_kb = size_bytes / 1024.0
                except Exception:
                    size_kb = 0.0
                cache_location = 'in-memory'

            return {
                'total_cached_pages': total_cached,
                'cache_file_size_kb': size_kb,
                'language': self.language,
                'cache_location': cache_location
            }
        except Exception:
            return {
                'total_cached_pages': 0,
                'cache_file_size_kb': 0.0,
                'language': getattr(self, 'language', 'unknown'),
                'cache_location': 'in-memory'
            }

    def get_page_extract(self, title: str):
        """Fetch a plain-text extract (intro) for a given page title."""
        # Check persisted pages cache first
        try:
            if title in self.cache.get('pages', {}):
                return self.cache['pages'][title]

            headers = {'User-Agent': self.user_agent}
            url = f'https://{self.language}.wikipedia.org/w/api.php'
            params = {
                'action': 'query',
                'prop': 'extracts',
                'exintro': True,
                'explaintext': True,
                'titles': title,
                'format': 'json'
            }

            resp = requests.get(url, headers=headers, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                pages = data.get('query', {}).get('pages', {})
                # pages keyed by pageid
                for pid, p in pages.items():
                    extract = p.get('extract')
                    if extract:
                        # Cache the extract under the title for quick reuse
                        try:
                            self.cache['pages'][title] = extract
                            with open(self.cache_file, 'w', encoding='utf-8') as f:
                                json.dump(self.cache, f, ensure_ascii=False)
                        except Exception:
                            pass
                        return extract
            return None
        except Exception:
            return None

    def suggest_titles(self, query: str, limit: int = 5):
        """Use the opensearch API to get title suggestions for a query."""
        try:
            headers = {'User-Agent': self.user_agent}
            url = f'https://{self.language}.wikipedia.org/w/api.php'
            params = {
                'action': 'opensearch',
                'search': query,
                'limit': limit,
                'namespace': 0,
                'format': 'json'
            }
            resp = requests.get(url, headers=headers, params=params, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                # opensearch returns [query, titles[], descriptions[], urls[]]
                if isinstance(data, list) and len(data) >= 2:
                    return data[1]
            return []
        except Exception:
            return []

class QuestionAnswerer:
    def __init__(self, searcher):
        self.searcher = searcher
    
    def answer_question(self, question):
        """Return a clean, human-readable answer for a question using
        the searcher. Picks the top search result and returns the
        page extract (plain text) with a source link.
        """
        try:
            search_results = self.searcher.search(question)

            # If API returned a search list, use the first hit
            if isinstance(search_results, dict) and 'query' in search_results:
                hits = search_results.get('query', {}).get('search', [])
                if len(hits) > 0:
                    title = hits[0].get('title')
                    summary = self.searcher.get_page_extract(title)
                    if summary:
                        # Truncate long summaries to a reasonable length
                        max_len = 1200
                        short = summary.strip()
                        if len(short) > max_len:
                            short = short[:max_len].rsplit('.', 1)[0] + '.'

                        source_url = f"https://{self.searcher.language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
                        return f"📚 {title}\n\n{short}\n\nSumber: {source_url}"

            # Fallback: if search returned a snippet-like structure, try to show concise info
            if isinstance(search_results, dict) and 'search' in search_results:
                snippets = []
                for s in search_results.get('search', [])[:3]:
                    snippets.append(f"- {s.get('title')}: {s.get('snippet')}")
                return "Hasil pencarian:\n" + "\n".join(snippets)

            # If nothing useful found, try opensearch suggestions
            suggestions = self.searcher.suggest_titles(question, limit=3)
            if suggestions:
                # Try first suggestion for a short extract
                candidate = suggestions[0]
                extract = self.searcher.get_page_extract(candidate)
                if extract:
                    short = extract.strip()
                    if len(short) > 1000:
                        short = short[:1000].rsplit('.', 1)[0] + '.'
                    source_url = f"https://{self.searcher.language}.wikipedia.org/wiki/{candidate.replace(' ', '_')}"
                    return f"Mungkin maksud: {candidate}\n\n{short}\n\nSumber: {source_url}"
                else:
                    # Just list suggestions
                    items = '\n'.join([f"- {s}" for s in suggestions])
                    return f"Saya tidak menemukan hasil langsung. Mungkin maksud: \n{items}"

            # Last-resort: return stringified result
            return str(search_results)

        except Exception as e:
            return f"Maaf, terjadi kesalahan saat mencari: {e}"

class KnowledgeBase:
    def __init__(self, vocab_manager=None, wiki_searcher=None):
        """Simple knowledge base that can optionally integrate
        an OnlineVocabularyManager and a WikipediaSearcher.

        Args:
            vocab_manager: Optional OnlineVocabularyManager instance
            wiki_searcher: Optional WikipediaSearcher instance
        """
        self.knowledge = {}
        self.vocab_manager = vocab_manager
        self.wiki_searcher = wiki_searcher

        # Preload vocabulary entries into knowledge for quick lookup
        try:
            if self.vocab_manager is not None:
                # vocab_manager stores words keyed by lowercase
                for key, data in getattr(self.vocab_manager, 'vocabulary', {}).items():
                    self.knowledge[key] = {
                        'source': data.get('source', 'local'),
                        'word': data.get('word', key),
                        'definition': data.get('definition'),
                        'examples': data.get('examples', []),
                        'part_of_speech': data.get('part_of_speech')
                    }
        except Exception:
            # Be tolerant to any unexpected structure in vocab_manager
            pass

        # Preload any cached Wikipedia page extracts into knowledge
        try:
            if self.wiki_searcher is not None:
                pages = getattr(self.wiki_searcher, 'cache', {}).get('pages', {})
                for title, extract in pages.items():
                    key = title.lower().strip()
                    if key not in self.knowledge:
                        self.knowledge[key] = {
                            'source': 'wikipedia',
                            'title': title,
                            'extract': extract
                        }
        except Exception:
            pass

        # Load persisted lessons if available
        try:
            lessons_file = None
            if self.wiki_searcher is not None and getattr(self.wiki_searcher, 'cache_dir', None):
                lessons_file = Path(self.wiki_searcher.cache_dir) / 'lessons.json'
            else:
                lessons_file = Path('lessons.json')

            if lessons_file.exists():
                try:
                    with open(lessons_file, 'r', encoding='utf-8') as f:
                        lessons = json.load(f)
                        if isinstance(lessons, dict):
                            for k, v in lessons.items():
                                key = k.lower().strip()
                                if key not in self.knowledge:
                                    self.knowledge[key] = v
                except Exception:
                    pass
        except Exception:
            pass

    def get_formatted(self, topic: str):
        """Return a nicely formatted string for a topic if present in the knowledge base.

        Returns None when no knowledge is available for the given topic.
        """
        key = topic.lower().strip()
        if key in self.knowledge:
            entry = self.knowledge[key]
            src = entry.get('source')
            # treat lesson entries like wiki extracts
            if src in ('wikipedia', 'lesson'):
                title = entry.get('title', topic)
                # support either 'extract' or 'content' fields
                extract = entry.get('extract') or entry.get('content') or entry.get('notes') or ''
                if extract:
                    short = extract.strip()
                    if len(short) > 1200:
                        short = short[:1200].rsplit('.', 1)[0] + '.'
                    source_url = ''
                    if src == 'wikipedia' and self.wiki_searcher:
                        source_url = f"https://{self.wiki_searcher.language}.wikipedia.org/wiki/{title.replace(' ', '_')}"
                    return f"📚 {title}\n\n{short}\n\nSumber: {source_url}" if source_url else f"📚 {title}\n\n{short}"
                else:
                    return f"📚 {title} (tidak ada ringkasan tersimpan)"

            # local vocabulary entry format
            if src == 'local':
                word = entry.get('word', topic)
                resp = f"🔤 {word.upper()}\n"
                resp += f"   Definition: {entry.get('definition', 'N/A')}\n"
                if entry.get('examples'):
                    resp += "   Examples:\n"
                    for ex in entry.get('examples', [])[:2]:
                        resp += f"      • {ex}\n"
                # include any merged notes or wikipedia content
                notes = entry.get('notes') or entry.get('wikipedia') or ''
                if notes:
                    short_notes = notes.strip()
                    if len(short_notes) > 800:
                        short_notes = short_notes[:800].rsplit('.', 1)[0] + '...'
                    resp += f"\n   Additional info:\n   {short_notes}\n"
                return resp

        return None

    def add_knowledge(self, topic, data):
        self.knowledge[topic] = data
        # Persist lessons to a simple lessons.json alongside wiki cache if possible
        try:
            lessons_file = None
            if hasattr(self, 'wiki_searcher') and getattr(self.wiki_searcher, 'cache_dir', None):
                lessons_file = Path(self.wiki_searcher.cache_dir) / 'lessons.json'
            else:
                lessons_file = Path('lessons.json')

            # Load existing lessons
            existing = {}
            if lessons_file.exists():
                try:
                    with open(lessons_file, 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                except Exception:
                    existing = {}

            existing[topic] = data
            try:
                with open(lessons_file, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
        except Exception:
            pass

    def get_knowledge(self, topic):
        key = topic.lower().strip()
        if key in self.knowledge:
            return self.knowledge[key]

        # If not found locally, try wikipedia_searcher if available
        if self.wiki_searcher is not None:
            try:
                wiki_result = self.wiki_searcher.search(topic)
                if wiki_result:
                    # Cache into knowledge for future
                    self.knowledge[key] = {
                        'source': 'wikipedia',
                        'data': wiki_result
                    }
                    return self.knowledge[key]
            except Exception:
                pass

        return 'No knowledge available on that topic.'

    def list_lessons(self):
        """Return a dict of saved lessons (title -> data)."""
        try:
            lessons_file = None
            if self.wiki_searcher is not None and getattr(self.wiki_searcher, 'cache_dir', None):
                lessons_file = Path(self.wiki_searcher.cache_dir) / 'lessons.json'
            else:
                lessons_file = Path('lessons.json')

            if lessons_file.exists():
                with open(lessons_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        return data
            # Fallback: return lessons known in memory
            lessons = {k: v for k, v in self.knowledge.items() if v.get('source') in ('lesson', 'wikipedia', 'local')}
            return lessons
        except Exception:
            return {}

    def remove_lesson(self, title: str) -> bool:
        """Remove a saved lesson by title; returns True if removed."""
        try:
            lessons_file = None
            if self.wiki_searcher is not None and getattr(self.wiki_searcher, 'cache_dir', None):
                lessons_file = Path(self.wiki_searcher.cache_dir) / 'lessons.json'
            else:
                lessons_file = Path('lessons.json')

            if lessons_file.exists():
                try:
                    with open(lessons_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                except Exception:
                    data = {}

                key = title.lower().strip()
                # Try exact key removal
                if key in data:
                    data.pop(key, None)
                    try:
                        with open(lessons_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                    except Exception:
                        pass
                    # also remove from in-memory knowledge
                    self.knowledge.pop(key, None)
                    return True

            # fallback: try removing from in-memory knowledge
            k = title.lower().strip()
            if k in self.knowledge:
                self.knowledge.pop(k, None)
                return True

            return False
        except Exception:
            return False

# Example usage
if __name__ == '__main__':
    searcher = WikipediaSearcher()
    answerer = QuestionAnswerer(searcher)
    
    question = "What is machine learning?"
    answer = answerer.answer_question(question)
    print(answer)
