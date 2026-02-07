"""
Project Robot - Offline Conversational AI Core Engine
Chatbot yang dapat diajarkan untuk ngobrol secara offline
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
import random
from typing import List, Dict, Tuple, Optional
from difflib import SequenceMatcher, get_close_matches


class PatternMatcher:
    """Pattern matching untuk pengenalan intent user"""
    
    def __init__(self):
        self.patterns = {}
        self.load_patterns()
    
    def load_patterns(self):
        """Load pattern dari file"""
        patterns_file = Path(__file__).parent / "data" / "patterns.json"
        if patterns_file.exists():
            with open(patterns_file, 'r', encoding='utf-8') as f:
                self.patterns = json.load(f)
    
    def save_patterns(self):
        """Save pattern ke file"""
        data_dir = Path(__file__).parent / "data"
        data_dir.mkdir(exist_ok=True)
        patterns_file = data_dir / "patterns.json"
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(self.patterns, f, ensure_ascii=False, indent=2)
    
    def add_pattern(self, intent: str, keywords: List[str], responses: List[str]):
        """Tambah pattern baru"""
        if intent not in self.patterns:
            self.patterns[intent] = {
                "keywords": [],
                "responses": []
            }
        self.patterns[intent]["keywords"].extend(keywords)
        self.patterns[intent]["responses"].extend(responses)
        self.patterns[intent]["keywords"] = list(set(self.patterns[intent]["keywords"]))
        self.save_patterns()
    
    def find_intent(self, text: str) -> Optional[str]:
        """Cari intent yang cocok dengan input user"""
        text_lower = text.lower()
        
        # Exact match dulu
        for intent, data in self.patterns.items():
            for keyword in data["keywords"]:
                if keyword.lower() in text_lower:
                    return intent
        
        # Partial match
        words = text_lower.split()
        best_match = None
        best_score = 0
        
        for intent, data in self.patterns.items():
            for keyword in data["keywords"]:
                keyword_words = keyword.lower().split()
                matches = sum(1 for w in keyword_words if w in words)
                score = matches / len(keyword_words) if keyword_words else 0
                if score > best_score:
                    best_score = score
                    best_match = intent
        
        if best_score > 0.3:
            return best_match

        # Fallback: fuzzy match using SequenceMatcher for short inputs or single-word typos
        try:
            # Only run fuzzy fallback for short inputs to avoid false positives on long sentences
            if len(text_lower.split()) <= 4:
                best_fuzzy = None
                best_ratio = 0.0
                for intent, data in self.patterns.items():
                    for keyword in data.get('keywords', []):
                        # compare keyword vs the whole input
                        ratio = SequenceMatcher(None, keyword.lower(), text_lower).ratio()
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_fuzzy = intent

                # threshold tuned to accept clear typos
                if best_ratio >= 0.65:
                    return best_fuzzy
        except Exception:
            pass

        return None
    
    def get_response(self, intent: str) -> str:
        """Dapatkan response random untuk intent"""
        if intent in self.patterns and self.patterns[intent]["responses"]:
            return random.choice(self.patterns[intent]["responses"])
        return None


class ConversationMemory:
    """Menyimpan memory percakapan"""
    
    def __init__(self, max_history: int = 50):
        self.history = []
        self.max_history = max_history
        self.memory_file = Path(__file__).parent / "data" / "conversation_memory.json"
        self.load_memory()
    
    def load_memory(self):
        """Load memory dari file"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
    
    def save_memory(self):
        """Save memory ke file"""
        self.memory_file.parent.mkdir(exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.history[-self.max_history:], f, ensure_ascii=False, indent=2)
    
    def add(self, user_text: str, bot_response: str):
        """Tambah percakapan ke memory"""
        self.history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_text,
            "bot": bot_response
        })
        self.save_memory()
    
    def get_context(self, last_n: int = 5) -> List[Dict]:
        """Dapatkan konteks percakapan terakhir"""
        return self.history[-last_n:]
    
    def clear_memory(self):
        """Hapus semua memory"""
        self.history = []
        if self.memory_file.exists():
            self.memory_file.unlink()


class RobotBrain:
    """Main chatbot brain"""
    
    def __init__(self):
        self.pattern_matcher = PatternMatcher()
        self.memory = ConversationMemory()
        self.name = "Project Robot"
        # configuration persistence
        self.config_file = Path(__file__).parent / 'data' / 'config.json'
        self._awaiting_new_name = False
        self._rename_proposed = None
        self._awaiting_rename_confirmation = False
        self.load_config()
        self.initialize_default_patterns()

        # user profile (remember conversation partner)
        self.user_profile_file = Path(__file__).parent / 'data' / 'user_profile.json'
        self.user_name = None
        self.load_user_profile()
        # user rename state
        self._awaiting_user_new_name = False
        self._proposed_user_name = None
        self._awaiting_user_rename_confirmation = False

    def load_config(self):
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and data.get('name'):
                        self.name = data.get('name')
        except Exception:
            pass

    def save_config(self):
        try:
            self.config_file.parent.mkdir(exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'name': self.name}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def load_user_profile(self):
        try:
            if self.user_profile_file.exists():
                with open(self.user_profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and data.get('user_name'):
                        self.user_name = data.get('user_name')
        except Exception:
            pass

    def save_user_profile(self):
        try:
            self.user_profile_file.parent.mkdir(exist_ok=True)
            with open(self.user_profile_file, 'w', encoding='utf-8') as f:
                json.dump({'user_name': self.user_name}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def set_user_name(self, name: str) -> None:
        try:
            self.user_name = name.strip()
            self.save_user_profile()
        except Exception:
            pass
    
    def initialize_default_patterns(self):
        """Inisialisasi pattern default"""
        default_patterns = {
            "greeting": {
                "keywords": ["halo", "hai", "hello", "assalamualaikum", "pagi", "siang", "malam"],
                "responses": [
                    "Halo! Apa kabar? Nama saya Project Robot 🤖",
                    "Hai! Senang bertemu denganmu!",
                    "Waalaikumassalam! Apa yang bisa saya bantu?",
                    "Helo! Ada yang bisa dibantu?"
                ]
            },
            "name": {
                "keywords": ["siapa nama kamu", "nama kamu siapa", "kamu siapa", "namamu"],
                "responses": [
                    "Nama saya Project Robot, senang berkenalan dengan Anda!",
                    "Saya adalah Project Robot, asisten chatbot offline Anda.",
                    "Project Robot adalah nama saya. Apa nama Anda?"
                ]
            },
            "goodbye": {
                "keywords": ["bye", "goodbye", "sampai jumpa", "dada", "selamat tinggal", "selamat"],
                "responses": [
                    "Sampai jumpa lagi! Senang berbincang denganmu 👋",
                    "Bye bye! Jumpa lagi nanti!",
                    "Selamat tinggal! Semoga harimu menyenangkan!",
                    "Dada! Senang berbincang denganmu!"
                ]
            },
            "how_are_you": {
                "keywords": ["apa kabar", "gimana kabar", "bagaimana keadaan", "kondisi kamu"],
                "responses": [
                    "Kabar saya baik! Terima kasih sudah bertanya 😊",
                    "Saya sangat baik, terimakasih! Bagaimana denganmu?",
                    "Sempurna! Siap membantu apapun kebutuhanmu!",
                    "Baik-baik saja! Semoga kamu juga sehat!"
                ]
            },
            "help": {
                "keywords": ["bantuan", "help", "bisa apa", "apa yang bisa", "fitur"],
                "responses": [
                    "Saya bisa diajari percakapan baru! Gunakan perintah 'ajar' untuk melatih saya.",
                    "Aku bisa obrolan santai, dan kamu bisa mengajari saya hal-hal baru!",
                    "Gunakan 'lihat pattern' untuk melihat apa yang sudah aku pelajari, dan 'ajar' untuk mengajari saya yang baru!"
                ]
            }
        }
        
        patterns_file = Path(__file__).parent / "data" / "patterns.json"
        if not patterns_file.exists():
            patterns_file.parent.mkdir(exist_ok=True)
            with open(patterns_file, 'w', encoding='utf-8') as f:
                json.dump(default_patterns, f, ensure_ascii=False, indent=2)
            self.pattern_matcher.load_patterns()
    
    def process_input(self, user_input: str) -> str:
        """Process input dan return response"""
        user_input = user_input.strip()
        
        if not user_input:
            return "Maaf, bisa tolong ulangi?"
        
        # Handle rename flow first if awaiting
        lower = user_input.lower()
        # If we are awaiting a new name value
        if getattr(self, '_awaiting_new_name', False):
            new_name = user_input.strip()
            if not new_name:
                self._awaiting_new_name = False
                return "Batal mengganti nama."
            # propose and ask for confirmation
            self._rename_proposed = new_name
            self._awaiting_new_name = False
            self._awaiting_rename_confirmation = True
            return f"Kamu ingin mengganti nama saya menjadi '{new_name}'? (yes/no)"

        # If awaiting confirmation
        if getattr(self, '_awaiting_rename_confirmation', False):
            ans = lower.strip()
            if ans in ('yes', 'y', 'iya', 'ya'):
                old = self.name
                self.name = self._rename_proposed or self.name
                self._rename_proposed = None
                self._awaiting_rename_confirmation = False
                try:
                    self.save_config()
                except Exception:
                    pass
                return f"✓ Nama saya berhasil diganti dari '{old}' menjadi '{self.name}'."
            else:
                # cancel
                self._rename_proposed = None
                self._awaiting_rename_confirmation = False
                return "OK, pembaruan nama dibatalkan."

        # Detect user rename requests (change user's name) — check before bot rename to avoid substring collisions
        if any(kw in lower for kw in ("ubah namaku", "ganti namaku", "ubah nama saya", "ganti nama saya")):
            self._awaiting_user_new_name = True
            return "Oke, kamu mau ganti nama menjadi apa?"

        # Detect direct rename requests for the bot
        if any(kw in lower for kw in ("ganti nama", "ganti namamu", "aku ganti nama kamu", "ubah nama")):
            # prompt for new name
            self._awaiting_new_name = True
            return "Oke, nama saya mau diganti jadi apa?"

        # If we are awaiting a user new name value
        if getattr(self, '_awaiting_user_new_name', False):
            new_name = user_input.strip()
            if not new_name:
                self._awaiting_user_new_name = False
                return "Batal mengganti nama Anda."
            # propose and ask for confirmation
            self._proposed_user_name = new_name
            self._awaiting_user_new_name = False
            self._awaiting_user_rename_confirmation = True
            return f"Kamu ingin saya menyimpan nama kamu sebagai '{new_name}'? (yes/no)"

        if getattr(self, '_awaiting_user_rename_confirmation', False):
            ans = lower.strip()
            if ans in ('yes', 'y', 'iya', 'ya'):
                old = self.user_name
                self.user_name = self._proposed_user_name or self.user_name
                self._proposed_user_name = None
                self._awaiting_user_rename_confirmation = False
                try:
                    self.save_user_profile()
                except Exception:
                    pass
                return f"✓ Nama Anda berhasil disimpan sebagai '{self.user_name}'."
            else:
                self._proposed_user_name = None
                self._awaiting_user_rename_confirmation = False
                return "OK, perubahan nama dibatalkan."

        # If user asks who they are, respond with stored user name
        if any(kw in lower for kw in ("siapa aku", "siapa saya", "siapakah aku", "siapakah saya")):
            if self.user_name:
                return f"Kamu adalah {self.user_name}."
            else:
                return "Saya belum tahu nama Anda. Kamu bisa bilang 'Nama aku Agus' untuk memperkenalkan diri."

        # Find matching intent
        intent = self.pattern_matcher.find_intent(user_input)

        if intent:
            # If the user asks for the bot's name, return the stored name
            if intent == 'name':
                return f"Saya adalah {self.name}, asisten chatbot offline Anda."

            # If greeting and we know user's name, personalize
            if intent == 'greeting' and self.user_name:
                return f"Halo {self.user_name}! Saya adalah {self.name}, senang bertemu denganmu."

            response = self.pattern_matcher.get_response(intent)
        else:
            response = random.choice([
                "Hmm, aku belum paham maksudmu. Bisa jelaskan lebih lanjut?",
                "Aku belum pernah belajar tentang itu. Mau mengajari saya?",
                "Maaf, aku masih belajar. Coba ajari saya dengan perintah 'ajar'!",
                "Itu menarik! Tapi aku belum tahu cara meresponnya. 🤔"
            ])
        
        # Save to memory
        self.memory.add(user_input, response)
        
        return response
    
    def teach(self, intent: str, keywords: List[str], responses: List[str]) -> str:
        """Ajar robot pattern baru"""
        if not intent or not keywords or not responses:
            return "❌ Format: intent='nama_intent', keywords=['kata1','kata2'], responses=['respon1','respon2']"
        
        try:
            self.pattern_matcher.add_pattern(intent, keywords, responses)
            return f"✓ Berhasil mengajari saya intent '{intent}' dengan {len(keywords)} keywords dan {len(responses)} responses!"
        except Exception as e:
            return f"❌ Terjadi error: {str(e)}"
    
    def list_patterns(self) -> str:
        """Tampilkan semua pattern yang sudah dipelajari"""
        if not self.pattern_matcher.patterns:
            return "Belum ada pattern yang dipelajari."
        
        result = "📚 Pattern yang sudah saya pelajari:\n"
        result += "=" * 50 + "\n"
        
        for i, (intent, data) in enumerate(self.pattern_matcher.patterns.items(), 1):
            result += f"\n{i}. Intent: {intent.upper()}\n"
            result += f"   Keywords ({len(data['keywords'])}): {', '.join(data['keywords'][:5])}"
            if len(data['keywords']) > 5:
                result += f" ... +{len(data['keywords'])-5} lagi"
            result += f"\n   Responses ({len(data['responses'])}): {data['responses'][0][:50]}...\n"
        
        return result
    
    def get_stats(self) -> str:
        """Dapatkan statistik robot"""
        stats = f"""
📊 STATISTIK PROJECT ROBOT
═════════════════════════════════════
• Total percakapan: {len(self.memory.history)}
• Total intent yang dipelajari: {len(self.pattern_matcher.patterns)}
• Total keywords: {sum(len(p['keywords']) for p in self.pattern_matcher.patterns.values())}
• Total responses: {sum(len(p['responses']) for p in self.pattern_matcher.patterns.values())}
═════════════════════════════════════
"""
        return stats
    
    def clear_all_memory(self) -> str:
        """Hapus semua memory"""
        self.memory.clear_memory()
        return "✓ Semua memory telah dihapus!"


def main():
    """Main function"""
    robot = RobotBrain()
    
    print("\n" + "="*60)
    print("🤖 PROJECT ROBOT - CHATBOT OFFLINE YANG BISA DIAJARKAN")
    print("="*60)
    print("\nPerintah khusus:")
    print("  'ajar' - Ajari saya percakapan baru")
    print("  'lihat pattern' - Lihat semua yang sudah saya pelajari")
    print("  'stats' - Lihat statistik saya")
    print("  'history' - Lihat riwayat percakapan")
    print("  'clear' - Hapus memory")
    print("  'exit' - Keluar dari program")
    print("="*60 + "\n")
    
    while True:
        try:
            user_input = input("\n🧑 Anda: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'exit':
                print("🤖 Project Robot: Sampai jumpa! Terima kasih sudah mengajari saya! 👋")
                break
            
            elif user_input.lower() == 'lihat pattern':
                print("\n" + robot.list_patterns())
                continue
            
            elif user_input.lower() == 'stats':
                print(robot.get_stats())
                continue
            
            elif user_input.lower() == 'history':
                recent = robot.memory.get_context(10)
                if recent:
                    print("\n📜 Riwayat 10 percakapan terakhir:")
                    for i, conv in enumerate(recent, 1):
                        print(f"  {i}. Anda: {conv['user']}")
                        print(f"     Bot: {conv['bot']}\n")
                else:
                    print("Belum ada history percakapan")
                continue
            
            elif user_input.lower() == 'clear':
                confirm = input("Yakin ingin menghapus semua memory? (yes/no): ")
                if confirm.lower() == 'yes':
                    print(robot.clear_all_memory())
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
    main()
