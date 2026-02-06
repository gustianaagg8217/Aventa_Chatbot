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
        
        return best_match if best_score > 0.3 else None
    
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
        self.initialize_default_patterns()
    
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
        
        # Find matching intent
        intent = self.pattern_matcher.find_intent(user_input)
        
        if intent:
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
