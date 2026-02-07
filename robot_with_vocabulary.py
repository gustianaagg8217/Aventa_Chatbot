"""
Integration module untuk menghubungkan Online Vocabulary Manager & Wikipedia dengan robot_core
"""

from robot_core import RobotBrain
from online_vocabulary import OnlineVocabularyManager, IntegrationHelper
from wikipedia_integration import WikipediaSearcher, QuestionAnswerer, KnowledgeBase
from pathlib import Path
from datetime import datetime
from typing import Optional


class EnhancedRobotBrain(RobotBrain):
    """Robot Brain yang diperkaya dengan online vocabulary & Wikipedia"""
    
    def __init__(self, enable_online_vocab: bool = True, enable_wikipedia: bool = True, 
                 sync_on_startup: bool = False):
        """
        Inisialisasi Robot dengan vocabulary online & Wikipedia
        
        Args:
            enable_online_vocab: Aktifkan fitur vocabulary online
            enable_wikipedia: Aktifkan fitur Wikipedia
            sync_on_startup: Sinkronisasi dengan online saat startup
        """
        super().__init__()
        
        self.vocab_manager = None
        self.wiki_searcher = None
        self.knowledge_base = None
        self.enable_online_vocab = enable_online_vocab
        self.enable_wikipedia = enable_wikipedia
        # conversation state for teaching flow
        self._awaiting_teach = None
        
        if enable_online_vocab:
            self.vocab_manager = OnlineVocabularyManager()
            IntegrationHelper.integrate_with_pattern_matcher(
                self.vocab_manager, 
                self.pattern_matcher
            )
            
            # Add online vocabulary commands
            self._add_vocab_commands()
            
            if sync_on_startup:
                print("\n🔄 Sinkronisasi vocabulary dengan online...")
                self.vocab_manager.sync_with_online(cache_hours=24)
        
        if enable_wikipedia:
            self.wiki_searcher = WikipediaSearcher(language="id")
            self.answerer = QuestionAnswerer(self.wiki_searcher)
            self._add_wikipedia_commands()
            
            # Create knowledge base jika both enabled
            if enable_online_vocab:
                self.knowledge_base = KnowledgeBase(self.vocab_manager, self.wiki_searcher)
    
    def _add_vocab_commands(self):
        """Tambah pattern untuk perintah vocabulary"""
        self.pattern_matcher.add_pattern(
            "vocab_search",
            ["cari vocab", "cari arti", "arti dari", "apa arti"],
            ["Saya akan cari vocabulary tersebut untuk Anda"]
        )
        
        self.pattern_matcher.add_pattern(
            "vocab_sync",
            ["sinkron vocab", "update vocab", "fetch vocab", "download vocab"],
            ["Saya sedang sinkronisasi vocabulary dari online"]
        )
        
        self.pattern_matcher.add_pattern(
            "vocab_stats",
            ["jumlah vocab", "berapa vocab", "statistik vocab"],
            ["Saya akan tunjukkan statistik vocabulary"]
        )
    
    def _add_wikipedia_commands(self):
        """Tambah pattern untuk perintah Wikipedia"""
        self.pattern_matcher.add_pattern(
            "wiki_search",
            ["cari wikipedia", "wikipedia", "apa itu", "siapa itu", "bagaimana cara"],
            ["Saya akan cari informasi di Wikipedia untuk Anda"]
        )
        
        self.pattern_matcher.add_pattern(
            "wiki_cache",
            ["cache wikipedia", "wikipedia cache", "cache wiki"],
            ["Saya akan tunjukkan informasi cache Wikipedia"]
        )
        # Command to save the last response as a lesson
        self.pattern_matcher.add_pattern(
            "save_lesson",
            ["masukan dalam pelajaran", "masukkan dalam pelajaran"],
            ["Saya akan menyimpan informasi terakhir ke pelajaran lokal"]
        )
        # Commands to list and remove lessons
        self.pattern_matcher.add_pattern(
            "list_lessons",
            ["daftar pelajaran", "lihat pelajaran", "list pelajaran"],
            ["Saya akan menampilkan daftar pelajaran lokal"]
        )

        self.pattern_matcher.add_pattern(
            "remove_lesson",
            ["hapus pelajaran"],
            ["Saya akan menghapus pelajaran lokal yang dipilih"]
        )
    
    def process_input(self, user_input: str) -> str:
        """Override process_input dengan fitur vocabulary & Wikipedia"""
        user_input = user_input.strip()
        
        if not user_input:
            return "Maaf, bisa tolong ulangi?"

        # Precompute lowercase for common checks
        lower = user_input.lower()

        # Detect user self-introduction to remember their name
        try:
            name_phrases = ["nama aku", "nama saya", "saya bernama", "nama ku", "aku bernama", "namaku"]
            for ph in name_phrases:
                if lower.startswith(ph):
                    # extract remainder as name
                    raw = user_input[len(ph):].strip(' :,-')
                    if not raw:
                        # if nothing after phrase, try splitting last token
                        parts = user_input.split()
                        if len(parts) >= 2:
                            raw = parts[-1]
                    if raw:
                        # Capitalize name properly (simple)
                        saved = raw.strip().split()[0].capitalize()
                        try:
                            # set in base RobotBrain
                            self.set_user_name(saved)
                        except Exception:
                            try:
                                super().set_user_name(saved)
                            except Exception:
                                pass
                        return f"Hai {saved}, saya adalah {self.name}, asisten chatbot offline Anda."
        except Exception:
            pass
        # If base RobotBrain is in a rename flow, delegate to base to handle confirmation/new name
        try:
            if (
                getattr(self, '_awaiting_new_name', False)
                or getattr(self, '_awaiting_rename_confirmation', False)
                or getattr(self, '_awaiting_user_new_name', False)
                or getattr(self, '_awaiting_user_rename_confirmation', False)
            ):
                return super().process_input(user_input)
        except Exception:
            pass

        # If the user requests to change their name, delegate to base RobotBrain handler
        if any(kw in lower for kw in ("ubah namaku", "ganti namaku", "ubah nama saya", "ganti nama saya")):
            return super().process_input(user_input)

        # Quick 'siapa aku' check to avoid being caught by wiki patterns
        if any(kw in lower for kw in ("siapa aku", "siapa saya", "siapakah aku", "siapakah saya")):
            if self.user_name:
                return f"Kamu adalah {self.user_name}."
            else:
                return "Saya belum tahu nama Anda. Kamu bisa bilang 'Nama aku Agus' untuk memperkenalkan diri."

        # Check learned patterns SEBELUM greeting check untuk prioritas
        try:
            learned_response = self._check_learned_patterns(user_input)
            if learned_response:
                return learned_response
        except Exception:
            pass

        # Personalize simple greetings if we know the user's name
        greetings = ("halo", "hai", "hei", "pagi", "siang", "malam")
        if any(lower.startswith(g) or f" {g} " in f" {lower} " for g in greetings):
            if self.user_name:
                return f"Halo {self.user_name}!"

        # If we are awaiting a teaching definition, capture this input as the definition
        if getattr(self, '_awaiting_teach', None):
            word = self._awaiting_teach
            definition = user_input.strip()
            # Try to remove leading 'word adalah/ialah' phrases
            try:
                lw = word.lower()
                ld = definition.lower()
                # remove leading word if repeated
                if ld.startswith(lw):
                    # remove word itself
                    definition = definition[len(word):].strip()
                    # remove common connectors
                    for prefix in [":", "-", "adalah", "ialah"]:
                        if definition.lower().startswith(prefix):
                            definition = definition[len(prefix):].strip()
                # final fallback trim
                definition = definition.strip()
                if not definition:
                    definition = user_input.strip()
            except Exception:
                definition = user_input.strip()

            # Save into vocabulary
            try:
                self.vocab_manager.add_vocabulary(word, definition)
                # also add into knowledge base if present
                if self.knowledge_base:
                    self.knowledge_base.add_knowledge(word.lower().strip(), {
                        'source': 'local',
                        'word': word,
                        'definition': definition,
                        'examples': []
                    })
                self._awaiting_teach = None
                return f"✓ Vocabulary '{word}' berhasil ditambahkan ke lokal cache"
            except Exception as e:
                self._awaiting_teach = None
                return f"Gagal menyimpan vocabulary: {e}"
        
        # Check untuk perintah Wikipedia
        if self.enable_wikipedia:
            lower = user_input.lower()
            if "cache wikipedia" in lower or "wikipedia cache" in lower:
                return self._handle_wiki_cache()

            # Detect wiki-style questions more robustly. Match phrases like:
            # 'apa itu ...', 'siapa itu ...', 'siapa ...', 'bagaimana cara ...' or 'bagaimana ...?'
            if (
                lower.startswith("apa itu") or
                lower.startswith("siapa itu") or
                lower.startswith("siapa ") or
                lower.startswith("bagaimana cara") or
                (lower.startswith("bagaimana") and "?" in user_input) or
                "apa itu" in lower or
                "siapa itu" in lower
            ):
                return self._handle_wiki_search(user_input)

        # If a knowledge base exists, try offline lookup for short/keyword queries
        if self.knowledge_base:
            try:
                # Only attempt for short queries (1-4 words) to avoid intercepting full sentences
                if 1 <= len(user_input.split()) <= 4:
                    kb_resp = self.knowledge_base.get_formatted(user_input)
                    if kb_resp:
                        return kb_resp
            except Exception:
                pass

        # Handle explicit lesson save command before other flows
        if self.knowledge_base:
            if lower in ("masukan dalam pelajaran", "masukkan dalam pelajaran", "masukan pelajaran", "simpan pelajaran"):
                return self._handle_insert_lesson()

        # If user typed a short single-word query and we have a vocab manager, offer teach flow
        try:
            if self.vocab_manager and 1 <= len(user_input.split()) <= 3:
                # normalize word
                candidate = user_input.strip().split()[0].strip().strip('?:,.').lower()
                if candidate and candidate not in self.vocab_manager.vocabulary and candidate not in self.vocab_manager.online_vocabulary:
                    # set awaiting state and ask user to teach
                    self._awaiting_teach = candidate
                    return f"Aku belum pernah belajar tentang itu. Mau mengajari saya? Ketik penjelasan untuk '{candidate}'"
        except Exception:
            pass

        # Merge last response into a keyword: phrases like 'tambahkan informasi ini ke [kata]'
        try:
            lower = user_input.lower()
            if 'tambahkan informasi ini ke ' in lower or 'tambahkan informasi ini ke dalam ' in lower or lower.startswith('tambahkan informasi ini ke') or lower.startswith('tambahkan informasi ini'):
                return self._handle_merge_info(user_input)
            if lower.startswith('tambahkan ini ke ') or lower.startswith('tambahkan ini ke dalam '):
                return self._handle_merge_info(user_input)
        except Exception:
            pass

        # Lesson management commands
        if self.knowledge_base:
            lower = user_input.lower()
            if lower in ("daftar pelajaran", "lihat pelajaran", "list pelajaran"):
                return self._handle_list_lessons()

            if lower.startswith("hapus pelajaran"):
                return self._handle_remove_lesson(user_input)
        
        # Check untuk perintah vocab khusus
        if "cari vocab" in user_input.lower() or "cari arti" in user_input.lower():
            return self._handle_vocab_search(user_input)
        
        elif "sinkron vocab" in user_input.lower() or "update vocab" in user_input.lower():
            return self._handle_vocab_sync()
        
        elif "statistik vocab" in user_input.lower() or "jumlah vocab" in user_input.lower():
            return self._handle_vocab_stats()
        
        # Check untuk pembelajaran pola percakapan: "Kalau ada yang bilang [X], jawab nya [Y]"
        try:
            if "kalau ada yang bilang" in lower and "jawab" in lower:
                result = self._learn_response_pattern(user_input)
                if result:
                    return result
        except Exception:
            pass
        
        # Default process seperti sebelumnya
        return super().process_input(user_input)
    
    def _handle_vocab_search(self, user_input: str) -> str:
        """Handle pencarian vocabulary"""
        if not self.vocab_manager:
            return "Fitur vocabulary tidak diaktifkan. Silakan aktifkan terlebih dahulu."
        
        # Extract kata yang dicari
        keywords = ["cari vocab", "cari arti", "arti dari", "apa arti"]
        query = user_input.lower()
        
        for keyword in keywords:
            if keyword in query:
                search_term = query.replace(keyword, "").strip()
                break
        else:
            search_term = query.strip()
        
        if not search_term:
            return "Kata apa yang ingin kamu cari artinya? Contoh: 'cari arti algoritma'"
        
        results = self.vocab_manager.search_vocabulary(search_term, limit=5)
        
        if not results:
            # Try fuzzy suggestions from vocab manager
            try:
                suggestions = self.vocab_manager.suggest_closest(search_term, n=3, cutoff=0.6)
            except Exception:
                suggestions = []

            if suggestions:
                # If one strong suggestion, show it and its definition if available
                if len(suggestions) == 1:
                    s = suggestions[0]
                    info = self.vocab_manager.vocabulary.get(s) or self.vocab_manager.online_vocabulary.get(s)
                    if info:
                        resp = f"Maaf, tidak menemukan '{search_term}'. Mungkin maksud '{info.get('word', s)}'?\n\n"
                        resp += f"🔤 {info.get('word', s).upper()}\n"
                        resp += f"   Definition: {info.get('definition', 'N/A')}\n"
                        if info.get('examples'):
                            resp += f"   Examples:\n"
                            for ex in info.get('examples', [])[:2]:
                                resp += f"      • {ex}\n"
                        return resp
                # Multiple suggestions: list them as possible corrections
                items = '\n'.join([f"- {s}" for s in suggestions])
                return f"Maaf, tidak menemukan '{search_term}'. Mungkin maksud salah satu dari:\n{items}\n\nCoba: 'cari arti [kata]'"

            return f"Maaf, saya tidak menemukan '{search_term}' di vocabulary saya. Mungkin kamu bisa mengajari saya?"
        
        response = f"📚 Hasil pencarian untuk '{search_term}':\n"
        response += "=" * 50 + "\n"
        
        for result in results:
            response += f"\n🔤 {result['word'].upper()}\n"
            response += f"   Definition: {result.get('definition', 'N/A')}\n"
            if result.get('part_of_speech'):
                response += f"   Part of Speech: {result.get('part_of_speech')}\n"
            if result.get('examples'):
                response += f"   Examples:\n"
                for ex in result.get('examples', [])[:2]:
                    response += f"      • {ex}\n"
            # include merged wikipedia/notes if present
            extra = result.get('wikipedia') or result.get('notes') or ''
            if extra:
                short_extra = extra.strip()
                if len(short_extra) > 800:
                    short_extra = short_extra[:800].rsplit('.', 1)[0] + '...'
                response += f"\n   Additional info:\n   {short_extra}\n"
        
        return response

    def _handle_insert_lesson(self) -> str:
        """Save the last bot response as a lesson in the KnowledgeBase/lessons.json"""
        if not self.knowledge_base:
            return "Fitur pelajaran tidak tersedia. Aktifkan Wikipedia dan vocabulary terlebih dahulu."

        # Get last bot response captured by the main loop
        last = getattr(self, '_last_response', None)
        if not last:
            return "Tidak ada respon terakhir untuk dimasukkan ke pelajaran. Coba tanyakan sesuatu terlebih dahulu."

        # Try to extract a title and content from common response formats
        title = None
        content = last
        # If wiki formatted (we prefix with '📚 Title')
        if last.startswith('📚'):
            # first line after the icon is the title
            try:
                first_line = last.splitlines()[0]
                title = first_line.lstrip('📚 ').strip()
                # content is the rest
                content = '\n'.join(last.splitlines()[1:]).strip()
            except Exception:
                title = None

        # If vocab formatted (starts with '🔤 WORD') use that as title
        if not title and last.startswith('🔤'):
            try:
                first_line = last.splitlines()[0]
                title = first_line.lstrip('🔤 ').strip()
                content = '\n'.join(last.splitlines()[1:]).strip()
            except Exception:
                title = None

        # If still no title, prompt user to provide one interactively
        if not title:
            try:
                prompt = "Response tidak memiliki judul otomatis. Masukkan judul pelajaran yang ingin disimpan (atau kosong untuk batal): "
                user_title = input(prompt).strip()
                if not user_title:
                    return "Batal menyimpan pelajaran."
                title = user_title
            except Exception:
                return "Response tidak memiliki judul otomatis. Mohon ulangi perintah dengan konteks atau gunakan format 'Apa itu [topik]?' sebelumnya."

        # Save into knowledge base under lowercase title
        data = {
            'source': 'lesson',
            'title': title,
            'content': content,
            'saved_at': __import__('datetime').datetime.now().isoformat()
        }

        try:
            self.knowledge_base.add_knowledge(title.lower().strip(), data)
            return f"✓ Berhasil menyimpan '{title}' ke pelajaran lokal."
        except Exception as e:
            return f"Gagal menyimpan pelajaran: {e}"

    def _handle_list_lessons(self) -> str:
        """Return a formatted list of saved lessons."""
        if not self.knowledge_base:
            return "Fitur pelajaran tidak tersedia."

        lessons = self.knowledge_base.list_lessons()
        if not lessons:
            return "Belum ada pelajaran yang disimpan."

        resp = "📚 DAFTAR PELAJARAN LOKAL:\n"
        resp += "═════════════════════════════════════\n"
        # lessons may be a dict of title -> data
        for title in sorted(lessons.keys()):
            # show title and a short preview
            entry = lessons.get(title)
            preview = ''
            if isinstance(entry, dict):
                preview = entry.get('title') or entry.get('word') or entry.get('content', '')
            resp += f"- {title}: {str(preview)[:80]}\n"

        return resp

    def _handle_remove_lesson(self, user_input: str) -> str:
        """Remove a lesson by title. Usage: 'hapus pelajaran [judul]'."""
        if not self.knowledge_base:
            return "Fitur pelajaran tidak tersedia."

        parts = user_input.split(None, 2)
        # Expected forms: 'hapus pelajaran Judul' or 'hapus pelajaran "Judul"'
        if len(parts) < 3:
            return "Gunakan: 'hapus pelajaran [judul]'. Contoh: hapus pelajaran Forex"

        title = parts[2].strip().strip('"')
        if not title:
            return "Judul pelajaran kosong. Batalkan."

        ok = self.knowledge_base.remove_lesson(title)
        if ok:
            return f"✓ Pelajaran '{title}' telah dihapus."
        else:
            return f"Tidak menemukan pelajaran berjudul '{title}'."

    def _handle_merge_info(self, user_input: str) -> str:
        """Merge the last bot response (e.g., a Wikipedia extract) into a vocabulary keyword.

        Expected forms:
          'tambahkan informasi ini ke forex'
          'tambahkan informasi ini ke dalam forex'
          'tambahkan ini ke forex'
        """
        # extract target keyword from the user_input
        try:
            lower = user_input.lower()
            # find the ' ke ' or ' ke dalam '
            target = None
            if ' ke dalam ' in lower:
                target = user_input.lower().split(' ke dalam ', 1)[1]
            elif ' ke ' in lower:
                target = user_input.lower().split(' ke ', 1)[1]
            else:
                # fallback: last token
                parts = user_input.split()
                if len(parts) > 1:
                    target = parts[-1]

            if not target:
                return "Tentukan kata kunci target. Contoh: 'tambahkan informasi ini ke Forex'"

            # clean target
            target = target.strip().strip('"').strip("'").strip().strip('?:.,')
            # if user wrote 'ke dalam forex' target may include 'dalah' typo; normalize
            target = target.replace('dalah', '').strip()
            if not target:
                return "Judul target tidak ditemukan. Gunakan: 'tambahkan informasi ini ke Forex'"

            key = target.lower()

            last = getattr(self, '_last_response', None)
            if not last:
                return "Tidak ada informasi terakhir yang bisa ditambahkan. Coba lakukan pencarian Wikipedia terlebih dahulu."

            # extract useful content from last response
            content = last
            # if it's a wiki formatted response '📚 Title\n\n<extract>\n\nSumber: ...'
            if last.startswith('📚'):
                lines = last.splitlines()
                # drop first line (title) and last line if 'Sumber:' present
                body_lines = []
                for ln in lines[1:]:
                    if ln.strip().lower().startswith('sumber:'):
                        break
                    body_lines.append(ln)
                content = '\n'.join(body_lines).strip()

            # if it's vocab formatted '🔤 WORD' use the details block
            if last.startswith('🔤'):
                lines = last.splitlines()
                content = '\n'.join(lines[1:]).strip()

            if not content:
                return "Tidak menemukan konten yang dapat ditambahkan dari respon terakhir."

            # Merge into vocabulary manager
            try:
                existing = None
                if self.vocab_manager:
                    existing = self.vocab_manager.vocabulary.get(key) or self.vocab_manager.online_vocabulary.get(key)

                if existing:
                    # add a wikipedia/notes field
                    try:
                        existing_notes = existing.get('wikipedia', '') or existing.get('notes', '')
                        if existing_notes:
                            merged_notes = existing_notes + '\n\n' + content
                        else:
                            merged_notes = content
                        existing['wikipedia'] = merged_notes
                        # persist change to local vocabulary if it's local
                        if key in self.vocab_manager.vocabulary:
                            self.vocab_manager.vocabulary[key] = existing
                            try:
                                self.vocab_manager._save_vocabulary()
                            except Exception:
                                pass
                        else:
                            # add to local as well
                            self.vocab_manager.vocabulary[key] = existing
                            try:
                                self.vocab_manager._save_vocabulary()
                            except Exception:
                                pass
                    except Exception:
                        pass
                else:
                    # create a new local vocab entry with the content as definition
                    if self.vocab_manager:
                        try:
                            self.vocab_manager.add_vocabulary(target, content, examples=None, part_of_speech=None)
                        except Exception:
                            # fallback: write directly
                            self.vocab_manager.vocabulary[key] = {
                                'word': target,
                                'definition': content,
                                'examples': [],
                                'part_of_speech': None,
                                'source': 'local'
                            }
                            try:
                                self.vocab_manager._save_vocabulary()
                            except Exception:
                                pass

                # update knowledge base as well
                try:
                    if self.knowledge_base:
                        kb_entry = self.knowledge_base.get_knowledge(key)
                        # If KB returned a dict, merge content into kb
                        if isinstance(kb_entry, dict):
                            kb_entry['notes'] = kb_entry.get('notes', '') + '\n\n' + content if kb_entry.get('notes') else content
                            self.knowledge_base.add_knowledge(key, kb_entry)
                        else:
                            # simply add as lesson
                            self.knowledge_base.add_knowledge(key, {'source': 'lesson', 'title': target, 'content': content})
                except Exception:
                    pass

                return f"✓ Informasi berhasil ditambahkan ke '{target}'."
            except Exception as e:
                return f"Gagal menambahkan informasi: {e}"

        except Exception:
            return "Gagal memproses perintah penambahan informasi. Gunakan: 'tambahkan informasi ini ke Forex'"
    
    def _check_learned_patterns(self, user_input: str) -> Optional[str]:
        """
        Check apakah user input cocok dengan learned patterns
        
        Args:
            user_input: Input user
            
        Returns:
            Response dari learned pattern atau None jika tidak cocok
        """
        try:
            # Iterate through patterns untuk cari yang prefix 'learned_'
            for intent, pattern_data in self.pattern_matcher.patterns.items():
                if intent.startswith('learned_'):
                    # Check setiap keyword di pattern
                    for keyword in pattern_data.get('keywords', []):
                        if keyword.lower() == user_input.lower():
                            # Found exact match, return response
                            responses = pattern_data.get('responses', [])
                            if responses:
                                import random
                                return random.choice(responses)
                            break
        except Exception:
            pass
        
        return None
    
    def _learn_response_pattern(self, user_input: str) -> Optional[str]:
        """
        Handle pembelajaran pola percakapan
        Format: "Kalau ada yang bilang [X], jawab nya [Y]"
        
        Args:
            user_input: Input user dengan pola pembelajaran
            
        Returns:
            Status pesan pembelajaran atau None jika pattern tidak cocok
        """
        import re
        
        # Pattern untuk menangkap pola pembelajaran
        # Menangani variasi: "kalau ada yang bilang X, jawab Y" atau "jawab nya Y"
        pattern = r"kalau ada yang bilang\s+(.+?),?\s+(?:jawab(?:\s+nya)?)\s+(.+?)$"
        
        match = re.search(pattern, user_input.lower(), re.IGNORECASE)
        if not match:
            return None
        
        try:
            trigger_phrase = match.group(1).strip()
            response_phrase = match.group(2).strip()
            
            if not trigger_phrase or not response_phrase:
                return None
            
            # Generate intent name dari trigger phrase
            intent_name = f"learned_{trigger_phrase.replace(' ', '_')[:20]}"
            
            # Tambahkan pattern ke pattern matcher
            try:
                self.pattern_matcher.add_pattern(
                    intent_name,
                    [trigger_phrase],
                    [response_phrase]
                )
                
                # Juga simpan ke knowledge base jika tersedia
                if self.knowledge_base:
                    self.knowledge_base.add_knowledge(
                        intent_name,
                        {
                            'source': 'learned_pattern',
                            'trigger': trigger_phrase,
                            'response': response_phrase,
                            'created_at': str(datetime.now())
                        }
                    )
                
                return f"✓ Pola pembelajaran berhasil ditambahkan!\n" \
                       f"Trigger: '{trigger_phrase}'\n" \
                       f"Response: '{response_phrase}'"
            
            except Exception as e:
                return f"⚠ Gagal menyimpan pola: {e}"
        
        except Exception as e:
            return None
    
    def _handle_vocab_sync(self) -> str:
        """Handle sinkronisasi vocabulary online"""
        if not self.vocab_manager:
            return "Fitur vocabulary tidak diaktifkan."
        
        print("\n⏳ Sinkronisasi vocabulary dari online...")
        success = self.vocab_manager.sync_with_online(force=True)
        
        if success:
            stats = self.vocab_manager.get_vocabulary_stats()
            return f"✓ Vocabulary berhasil diperbarui!\n" \
                   f"📊 Total: {stats['total_vocabulary']} kata\n" \
                   f"   Online: {stats['online_vocabulary']}\n" \
                   f"   Local: {stats['local_vocabulary']}\n" \
                   f"   Last Sync: {stats['last_updated']}"
        else:
            return "⚠ Tidak bisa sinkronisasi online, menggunakan cache lokal"
    
    def _handle_vocab_stats(self) -> str:
        """Handle tampilan statistik vocabulary"""
        if not self.vocab_manager:
            return "Fitur vocabulary tidak diaktifkan."
        
        stats = self.vocab_manager.get_vocabulary_stats()
        
        return f"""
📊 VOCABULARY STATISTICS
═════════════════════════════════════
• Total Vocabulary: {stats['total_vocabulary']}
• Online Vocabulary: {stats['online_vocabulary']}
• Local Vocabulary: {stats['local_vocabulary']}
• Last Updated: {stats['last_updated']}
• Cache Size: {stats['cache_size_mb']:.2f} MB
═════════════════════════════════════
"""
    
    def add_local_vocabulary(self, word: str, definition: str, 
                            examples: list = None, part_of_speech: str = None) -> str:
        """
        Tambah vocabulary lokal
        
        Args:
            word: Kata
            definition: Definisi
            examples: Contoh penggunaan
            part_of_speech: Jenis kata
        
        Returns:
            Status message
        """
        if not self.vocab_manager:
            return "Fitur vocabulary tidak diaktifkan."
        
        self.vocab_manager.add_vocabulary(word, definition, examples, part_of_speech)
        return f"✓ Vocabulary '{word}' berhasil ditambahkan ke lokal cache"
    
    def export_vocabulary(self, format: str = "json", output_path: str = None) -> str:
        """
        Export vocabulary
        
        Args:
            format: Format export (json, csv, txt)
            output_path: Path output
        
        Returns:
            Path file yang di-export
        """
        if not self.vocab_manager:
            return "Fitur vocabulary tidak diaktifkan."
        
        return self.vocab_manager.export_vocabulary(format, output_path)
    
    def _handle_wiki_search(self, question: str) -> str:
        """Handle pencarian di Wikipedia"""
        if not self.enable_wikipedia:
            return "Fitur Wikipedia tidak diaktifkan."
        
        print(f"\n🔍 Searching Wikipedia...")
        answer = self.answerer.answer_question(question)
        return answer
    
    def _handle_wiki_cache(self) -> str:
        """Handle tampilan Wikipedia cache stats"""
        if not self.wiki_searcher:
            return "Fitur Wikipedia tidak diaktifkan."
        
        stats = self.wiki_searcher.get_cache_stats()
        
        response = f"""
📖 WIKIPEDIA CACHE STATISTICS
═════════════════════════════════════
• Total Cached Pages: {stats['total_cached_pages']}
• Cache File Size: {stats['cache_file_size_kb']:.2f} KB
• Language: {stats['language']}
• Cache Location: {stats['cache_location']}
═════════════════════════════════════
"""
        return response


def main_with_vocabulary():
    """Main function dengan Online Vocabulary"""
    robot = EnhancedRobotBrain(
        enable_online_vocab=True, 
        enable_wikipedia=True,
        sync_on_startup=True
    )
    
    print("\n" + "="*60)
    print("🤖 PROJECT ROBOT - ONLINE VOCABULARY + WIKIPEDIA")
    print("="*60)
    print("\nPerintah standar:")
    print("  'ajar' - Ajari saya percakapan baru")
    print("  'lihat pattern' - Lihat semua pattern")
    print("  'stats' - Lihat statistik robot")
    print("\n💡 Perintah vocabulary:")
    print("  'cari arti [kata]' - Cari arti kata di vocabulary")
    print("  'sinkron vocab' - Update vocabulary dari online")
    print("  'statistik vocab' - Lihat statistik vocabulary")
    print("  'export vocab' - Export vocabulary ke file")
    print("\n📖 Perintah Wikipedia:")
    print("  'apa itu [topik]' - Cari informasi di Wikipedia")
    print("  'siapa itu [orang]' - Cari tentang orang di Wikipedia")
    print("  'bagaimana cara [sesuatu]' - Cari cara di Wikipedia")
    print("  'cache wikipedia' - Lihat cache Wikipedia")
    print("\nPerintah lainnya:")
    print("  'exit' - Keluar")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("\n🧑 Anda: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                print("🤖 Project Robot: Sampai jumpa! 👋")
                break
            
            elif user_input.lower() == 'export vocab':
                format_choice = input("Format? (json/csv/txt) [default: json]: ").strip() or "json"
                filepath = robot.export_vocabulary(format_choice)
                print(f"🤖 Project Robot: {filepath}")
                continue
            
            elif user_input.lower() == 'lihat pattern':
                print("\n" + robot.list_patterns())
                continue
            
            elif user_input.lower() == 'stats':
                print(robot.get_stats())
                continue
            
            elif user_input.lower() == 'ajar':
                print("\n📝 AJARKAN SAYA PERCAKAPAN BARU")
                print("-" * 40)
                intent = input("Intent (nama kategori): ").strip()
                
                keywords_input = input("Keywords (pisahkan dengan koma): ").strip()
                keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
                
                responses_input = input("Responses (pisahkan dengan |): ").strip()
                responses = [r.strip() for r in responses_input.split('|') if r.strip()]
                
                result = robot.teach(intent, keywords, responses)
                print(f"🤖 Project Robot: {result}")
                continue
            
            # Normal conversation
            response = robot.process_input(user_input)
            print(f"\n🤖 Project Robot: {response}")
            # store last bot response for lesson-saving and other context features
            try:
                robot._last_response = response
            except Exception:
                pass
        
        except KeyboardInterrupt:
            print("\n\n🤖 Project Robot: Sampai jumpa! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main_with_vocabulary()
