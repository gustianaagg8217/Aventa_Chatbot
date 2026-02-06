#!/usr/bin/env python3
"""
Test script untuk memverifikasi Online Vocabulary System
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def test_imports():
    """Test 1: Verify imports"""
    print_header("TEST 1: Verify Imports")
    
    try:
        print("Importing online_vocabulary...", end=" ")
        from online_vocabulary import OnlineVocabularyManager, IntegrationHelper
        print("✓")
        
        print("Importing robot_core...", end=" ")
        from robot_core import RobotBrain, PatternMatcher, ConversationMemory
        print("✓")
        
        print("Importing robot_with_vocabulary...", end=" ")
        from robot_with_vocabulary import EnhancedRobotBrain
        print("✓")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_vocab_manager():
    """Test 2: OnlineVocabularyManager"""
    print_header("TEST 2: OnlineVocabularyManager")
    
    try:
        from online_vocabulary import OnlineVocabularyManager
        
        print("Creating OnlineVocabularyManager...", end=" ")
        vocab_mgr = OnlineVocabularyManager()
        print("✓")
        
        print("Testing add_vocabulary...", end=" ")
        vocab_mgr.add_vocabulary(
            word="test_word",
            definition="A test definition",
            examples=["Example 1", "Example 2"]
        )
        print("✓")
        
        print("Testing search_vocabulary...", end=" ")
        results = vocab_mgr.search_vocabulary("test")
        assert len(results) > 0, "No search results"
        print(f"✓ (Found {len(results)} results)")
        
        print("Testing get_vocabulary_stats...", end=" ")
        stats = vocab_mgr.get_vocabulary_stats()
        assert stats['total_vocabulary'] > 0, "No vocabulary loaded"
        print(f"✓ (Total: {stats['total_vocabulary']})")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_robot_brain():
    """Test 3: RobotBrain"""
    print_header("TEST 3: RobotBrain")
    
    try:
        from robot_core import RobotBrain
        
        print("Creating RobotBrain...", end=" ")
        robot = RobotBrain()
        print("✓")
        
        print("Testing process_input...", end=" ")
        response = robot.process_input("Halo!")
        assert response, "No response generated"
        print(f"✓ (Response: '{response[:50]}...')")
        
        print("Testing teach...", end=" ")
        result = robot.teach(
            "test_intent",
            ["test keyword"],
            ["test response"]
        )
        assert "✓" in result, "Teach failed"
        print("✓")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_enhanced_robot():
    """Test 4: EnhancedRobotBrain"""
    print_header("TEST 4: EnhancedRobotBrain")
    
    try:
        from robot_with_vocabulary import EnhancedRobotBrain
        
        print("Creating EnhancedRobotBrain (no online sync)...", end=" ")
        robot = EnhancedRobotBrain(enable_online_vocab=True, sync_on_startup=False)
        print("✓")
        
        print("Testing vocab manager...", end=" ")
        assert robot.vocab_manager is not None, "Vocab manager is None"
        print("✓")
        
        print("Testing vocabulary search method...", end=" ")
        response = robot._handle_vocab_search("cari arti algoritma")
        assert response, "No search response"
        print(f"✓ (Response length: {len(response)} chars)")
        
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_file_structure():
    """Test 5: File Structure"""
    print_header("TEST 5: File Structure")
    
    try:
        project_root = Path(__file__).parent
        data_dir = project_root / "data"
        cache_dir = data_dir / "vocabulary_cache"
        
        checks = {
            "data/ directory": data_dir.exists(),
            "vocabulary_cache/ directory": cache_dir.exists(),
            "online_vocabulary.py": (project_root / "online_vocabulary.py").exists(),
            "robot_with_vocabulary.py": (project_root / "robot_with_vocabulary.py").exists(),
            "robot_core.py": (project_root / "robot_core.py").exists(),
            "requirements.txt": (project_root / "requirements.txt").exists(),
            "vocabulary_config.json": (project_root / "vocabulary_config.json").exists(),
            "ONLINE_VOCABULARY_GUIDE.md": (project_root / "ONLINE_VOCABULARY_GUIDE.md").exists(),
        }
        
        all_ok = True
        for check, exists in checks.items():
            status = "✓" if exists else "✗"
            print(f"{status} {check}")
            if not exists:
                all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_cache_operations():
    """Test 6: Cache Operations"""
    print_header("TEST 6: Cache Operations")
    
    try:
        from online_vocabulary import OnlineVocabularyManager
        import tempfile
        
        print("Creating temp cache directory...", end=" ")
        with tempfile.TemporaryDirectory() as tmpdir:
            print("✓")
            
            print("Creating OnlineVocabularyManager with temp cache...", end=" ")
            vocab_mgr = OnlineVocabularyManager(cache_dir=tmpdir)
            print("✓")
            
            print("Adding test vocabulary...", end=" ")
            vocab_mgr.add_vocabulary("cache_test", "Test definition")
            print("✓")
            
            print("Loading cache...", end=" ")
            vocab_mgr.load_cache()
            assert "cache_test" in vocab_mgr.vocabulary, "Cache not loaded"
            print("✓")
            
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_export_functionality():
    """Test 7: Export Functionality"""
    print_header("TEST 7: Export Functionality")
    
    try:
        from online_vocabulary import OnlineVocabularyManager
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmpdir:
            print("Creating OnlineVocabularyManager...", end=" ")
            vocab_mgr = OnlineVocabularyManager(cache_dir=tmpdir)
            vocab_mgr.add_vocabulary("export_test", "Test word")
            print("✓")
            
            print("Testing JSON export...", end=" ")
            json_path = vocab_mgr.export_vocabulary("json")
            assert Path(json_path).exists(), "JSON export failed"
            print(f"✓ ({json_path})")
            
            print("Testing CSV export...", end=" ")
            csv_path = vocab_mgr.export_vocabulary("csv")
            assert Path(csv_path).exists(), "CSV export failed"
            print(f"✓ ({csv_path})")
            
            print("Testing TXT export...", end=" ")
            txt_path = vocab_mgr.export_vocabulary("txt")
            assert Path(txt_path).exists(), "TXT export failed"
            print(f"✓ ({txt_path})")
            
            return True
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  ONLINE VOCABULARY SYSTEM - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Imports", test_imports),
        ("Vocabulary Manager", test_vocab_manager),
        ("Robot Brain", test_robot_brain),
        ("Enhanced Robot", test_enhanced_robot),
        ("File Structure", test_file_structure),
        ("Cache Operations", test_cache_operations),
        ("Export Functionality", test_export_functionality),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ Test '{test_name}' failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready to use.")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
