#!/usr/bin/env python3
"""
Setup script untuk Online Vocabulary System
Memudahkan instalasi dan konfigurasi awal
"""

import os
import sys
import subprocess
from pathlib import Path
import json
from datetime import datetime


class VocabularySetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.data_dir = self.project_root / "data"
        self.cache_dir = self.data_dir / "vocabulary_cache"
    
    def print_header(self, text: str):
        """Print formatted header"""
        print("\n" + "="*60)
        print(f"  {text}")
        print("="*60)
    
    def print_step(self, step: int, text: str):
        """Print step"""
        print(f"\n[STEP {step}] {text}")
    
    def create_directories(self):
        """Create required directories"""
        self.print_step(1, "Creating directories...")
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"✓ Created: {self.data_dir}")
        print(f"✓ Created: {self.cache_dir}")
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.print_step(2, "Installing Python dependencies...")
        
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("❌ requirements.txt not found!")
            return False
        
        try:
            # Show what we're installing
            print("\nDependencies to install:")
            with open(requirements_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        print(f"  • {line}")
            
            print("\nInstalling...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✓ All dependencies installed successfully")
                return True
            else:
                print("❌ Installation failed!")
                print(result.stderr)
                return False
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def initialize_vocabulary_cache(self):
        """Initialize vocabulary cache with metadata"""
        self.print_step(3, "Initializing vocabulary cache...")
        
        metadata_file = self.cache_dir / "cache_metadata.json"
        
        metadata = {
            "created_date": datetime.now().isoformat(),
            "last_updated": None,
            "vocab_count": 0,
            "cache_version": "1.0",
            "status": "initialized"
        }
        
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Initialized cache metadata: {metadata_file}")
            return True
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def test_online_connection(self):
        """Test connection to online sources"""
        self.print_step(4, "Testing online connection...")
        
        try:
            import requests
            
            sources = [
                "https://www.github.com",
                "https://www.google.com"
            ]
            
            for source in sources:
                try:
                    response = requests.head(source, timeout=5)
                    print(f"✓ {source} - OK")
                except:
                    print(f"⚠ {source} - UNREACHABLE (but vocabulary cache will still work)")
            
            return True
        
        except ImportError:
            print("⚠ requests library not available - skipping online test")
            return True
        except Exception as e:
            print(f"⚠ Error testing connection: {e}")
            return True
    
    def create_example_vocabulary(self):
        """Create example vocabulary"""
        self.print_step(5, "Creating example vocabulary...")
        
        vocab_file = self.cache_dir / "vocabulary_cache.json"
        
        example_vocab = {
            "artificial_intelligence": {
                "definition": "Simulasi proses intelijen manusia oleh komputer",
                "examples": [
                    "AI digunakan untuk autonomous vehicles",
                    "Machine learning adalah bagian dari AI"
                ],
                "part_of_speech": "noun",
                "added_date": datetime.now().isoformat(),
                "source": "online"
            },
            "vocabulary": {
                "definition": "Seluruh kumpulan kata yang digunakan dalam bahasa",
                "examples": [
                    "Kosakata bahasa Inggris terdiri dari jutaan kata",
                    "Memperluas vocabulary meningkatkan komunikasi"
                ],
                "part_of_speech": "noun",
                "added_date": datetime.now().isoformat(),
                "source": "online"
            },
            "cache": {
                "definition": "Penyimpanan data cepat untuk akses yang lebih efisien",
                "examples": [
                    "Browser cache mempercepat loading halaman",
                    "CPU cache meningkatkan performa komputasi"
                ],
                "part_of_speech": "noun",
                "added_date": datetime.now().isoformat(),
                "source": "online"
            },
            "algorithm": {
                "definition": "Prosedur langkah demi langkah untuk menyelesaikan masalah",
                "examples": [
                    "Algoritma sorting digunakan untuk mengurutkan data",
                    "Algoritma pencarian biner lebih efisien untuk dataset besar"
                ],
                "part_of_speech": "noun",
                "added_date": datetime.now().isoformat(),
                "source": "online"
            }
        }
        
        try:
            # Load existing jika ada
            if vocab_file.exists():
                with open(vocab_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
                    example_vocab.update(existing)
            
            with open(vocab_file, 'w', encoding='utf-8') as f:
                json.dump(example_vocab, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Created example vocabulary with {len(example_vocab)} words")
            print(f"  File: {vocab_file}")
            return True
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def verify_installation(self):
        """Verify installation"""
        self.print_step(6, "Verifying installation...")
        
        checks = {
            "Directory data/": self.data_dir.exists(),
            "Directory data/vocabulary_cache/": self.cache_dir.exists(),
            "File cache_metadata.json": (self.cache_dir / "cache_metadata.json").exists(),
            "File vocabulary_cache.json": (self.cache_dir / "vocabulary_cache.json").exists(),
            "Module online_vocabulary.py": (self.project_root / "online_vocabulary.py").exists(),
            "Module robot_with_vocabulary.py": (self.project_root / "robot_with_vocabulary.py").exists(),
            "File requirements.txt": (self.project_root / "requirements.txt").exists(),
        }
        
        all_ok = True
        for check, result in checks.items():
            status = "✓" if result else "❌"
            print(f"{status} {check}")
            if not result:
                all_ok = False
        
        return all_ok
    
    def show_next_steps(self):
        """Show next steps"""
        self.print_header("🎉 SETUP COMPLETE!")
        
        print("\n📚 Next Steps:")
        print("\n1. Run the chatbot dengan vocabulary online:")
        print("   python robot_with_vocabulary.py")
        
        print("\n2. Atau gunakan original chatbot tanpa online:")
        print("   python robot_core.py")
        
        print("\n3. Perintah vocabulary yang tersedia:")
        print("   • 'cari arti [kata]' - Cari vocabulary")
        print("   • 'sinkron vocab' - Update dari online")
        print("   • 'statistik vocab' - Lihat statistik")
        print("   • 'export vocab' - Export ke file")
        
        print("\n4. Baca dokumentasi lengkap:")
        print("   ONLINE_VOCABULARY_GUIDE.md")
        
        print("\n5. Custom configuration:")
        print("   Edit online_vocabulary.py → _get_default_sources()")
        
        print("\n" + "="*60)
    
    def run_setup(self):
        """Run full setup"""
        self.print_header("⚙️  ONLINE VOCABULARY SYSTEM SETUP")
        
        print("\nThis setup will:")
        print("✓ Create necessary directories")
        print("✓ Install Python dependencies")
        print("✓ Initialize vocabulary cache")
        print("✓ Test online connection")
        print("✓ Create example vocabulary")
        print("✓ Verify installation")
        
        input("\nPress ENTER to continue...")
        
        # Run setup steps
        self.create_directories()
        
        if not self.install_dependencies():
            print("\n⚠️ Dependency installation had issues, but continuing...")
        
        self.initialize_vocabulary_cache()
        self.test_online_connection()
        self.create_example_vocabulary()
        
        if self.verify_installation():
            self.show_next_steps()
            return True
        else:
            print("\n❌ Some checks failed. Please review the output above.")
            return False


def main():
    """Main function"""
    setup = VocabularySetup()
    
    try:
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
