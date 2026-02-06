"""
Integration module untuk menghubungkan Online Vocabulary Manager & Wikipedia dengan robot_core
"""

from robot_core import RobotBrain
from online_vocabulary import OnlineVocabularyManager, IntegrationHelper
from wikipedia_integration import WikipediaSearcher, QuestionAnswerer, KnowledgeBase
from pathlib import Path


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
    
    def process_input(self, user_input: str) -> str:
        """Override process_input dengan fitur vocabulary & Wikipedia"""
        user_input = user_input.strip()
        
        if not user_input:
            return "Maaf, bisa tolong ulangi?"
        
        # Check untuk perintah Wikipedia
        if self.enable_wikipedia:
            if "cache wikipedia" in user_input.lower() or "wikipedia cache" in user_input.lower():
                return self._handle_wiki_cache()
            elif "apa itu" in user_input.lower() or "siapa itu" in user_input.lower() or \
                 "bagaimana" in user_input.lower() and "?" in user_input:
                return self._handle_wiki_search(user_input)
        
        # Check untuk perintah vocab khusus
        if "cari vocab" in user_input.lower() or "cari arti" in user_input.lower():
            return self._handle_vocab_search(user_input)
        
        elif "sinkron vocab" in user_input.lower() or "update vocab" in user_input.lower():
            return self._handle_vocab_sync()
        
        elif "statistik vocab" in user_input.lower() or "jumlah vocab" in user_input.lower():
            return self._handle_vocab_stats()
        
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
        
        return response
    
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
                   f"   Local: {stats['local_vocabulary']}"
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
        
        except KeyboardInterrupt:
            print("\n\n🤖 Project Robot: Sampai jumpa! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main_with_vocabulary()
