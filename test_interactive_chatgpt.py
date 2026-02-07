#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive Test untuk ChatGPT Fallback Integration
Test berbagai jenis pertanyaan untuk verifikasi ChatGPT working
"""

from robot_with_vocabulary import EnhancedRobotBrain

def print_header():
    print("\n" + "=" * 80)
    print("🤖 INTERACTIVE CHATGPT FALLBACK TEST")
    print("=" * 80)
    print("\n📝 Instruksi:")
    print("  1. Program akan menunjukkan 3 kategori pertanyaan")
    print("  2. Kategori 1: Local Pattern (instant, NO API)")
    print("  3. Kategori 2: Vocabulary (local, NO API)")
    print("  4. Kategori 3: ChatGPT Fallback (USES API - YOUR TEST)")
    print("\n💡 Cara identifikasi ChatGPT response:")
    print("  - Respons yang panjang & detail = ChatGPT")
    print("  - Respons yang singkat dari pattern = Local")
    print("\n" + "=" * 80)

def test_local_patterns(robot):
    """Test 1: Local Patterns (Instant, No API)"""
    print("\n\n[TEST 1] 🎯 LOCAL PATTERNS (Instant - No API Call)")
    print("-" * 80)
    print("Status: Pertanyaan ini TIDAK akan call ChatGPT (match local pattern)")
    print()
    
    patterns = [
        "Halo",
        "Pagi",
        "nama saya Agus",
    ]
    
    for query in patterns:
        print(f"🧑 Input: {query}")
        response = robot.process_input(query)
        print(f"🤖 Response: {response}")
        print()

def test_vocabulary_search(robot):
    """Test 2: Vocabulary Search (Local, No API)"""
    print("\n[TEST 2] 📚 VOCABULARY SEARCH (Local Cache - No API Call)")
    print("-" * 80)
    print("Status: Pertanyaan ini TIDAK akan call ChatGPT (match vocab pattern)")
    print()
    
    vocab_queries = [
        "cari arti algoritma",
        "cari vocab computer",
    ]
    
    for query in vocab_queries:
        print(f"🧑 Input: {query}")
        response = robot.process_input(query)
        # Print limited preview
        preview = response[:100] if len(response) > 100 else response
        print(f"🤖 Response: {preview}...")
        print()

def test_chatgpt_fallback(robot):
    """Test 3: ChatGPT Fallback (This WILL use API)"""
    print("\n[TEST 3] 🚀 CHATGPT FALLBACK (WILL USE API - MAIN TEST)")
    print("-" * 80)
    print("Status: Pertanyaan ini AKAN call ChatGPT fallback")
    print("⏳ Tunggu beberapa detik untuk API response...\n")
    
    # Test queries yang pasti tidak cocok dengan local pattern
    chatgpt_queries = [
        "Apa itu machine learning?",
        "Bagaimana cara menjadi programmer terbaik?",
        "Apa pendapatmu tentang AI?",
    ]
    
    for i, query in enumerate(chatgpt_queries, 1):
        print(f"\n📌 Test {i}/{len(chatgpt_queries)}")
        print(f"🧑 Input: {query}")
        print("⏳ Waiting for ChatGPT response...")
        
        response = robot.process_input(query)
        
        # Check if response is from ChatGPT
        is_chatgpt = (
            "Saya akan cari" not in response and
            "belum pernah" not in response and
            "tidak mengerti" not in response and
            len(response) > 80  # ChatGPT responses are longer
        )
        
        indicator = "✅ ChatGPT" if is_chatgpt else "❌ Local"
        print(f"{indicator} | Response: {response[:150]}...")
        print()

def show_chatgpt_status(robot):
    """Tampilkan status ChatGPT"""
    print("\n[STATUS] 📊 CHATGPT CONFIGURATION")
    print("-" * 80)
    stats = robot._handle_chatgpt_stats()
    print(stats)

def interactive_mode(robot):
    """Mode interaktif untuk test manual"""
    print("\n[INTERACTIVE MODE] 💬 Free Test")
    print("-" * 80)
    print("Ketik pertanyaan apapun untuk test ChatGPT fallback")
    print("Ketik 'quit' atau 'exit' untuk keluar\n")
    
    while True:
        try:
            user_input = input("🧑 Anda: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'keluar']:
                print("Terima kasih! Sampai jumpa! 👋")
                break
            
            if not user_input:
                continue
            
            print("⏳ Waiting for response...")
            response = robot.process_input(user_input)
            
            # Check yang mana
            is_chatgpt = (
                "Saya akan cari" not in response and
                "belum pernah" not in response and
                "tidak mengerti" not in response and
                len(response) > 80
            )
            
            indicator = "✅ [ChatGPT]" if is_chatgpt else "❓ [Local Pattern]"
            print(f"\n🤖 {indicator}\n{response}\n")
            
        except KeyboardInterrupt:
            print("\n\nBerhenti. Sampai jumpa! 👋")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            continue

def main():
    print("🔄 Initializing robot dengan ChatGPT fallback...")
    
    # Initialize robot
    robot = EnhancedRobotBrain(
        enable_online_vocab=True,
        enable_wikipedia=False,  # Disable untuk clear test
        sync_on_startup=False
    )
    
    print("✓ Robot initialized\n")
    
    # Show header
    print_header()
    
    # Show status
    show_chatgpt_status(robot)
    
    # Run tests
    print("\n\n🧪 RUNNING TESTS...")
    
    test_local_patterns(robot)
    input("Press Enter untuk lanjut ke TEST 2...")
    
    test_vocabulary_search(robot)
    input("Press Enter untuk lanjut ke TEST 3 (ChatGPT Fallback)...")
    
    test_chatgpt_fallback(robot)
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    final_stats = robot.chatgpt_fallback.get_stats()
    print(f"\n✅ ChatGPT Status: {('Enabled' if final_stats['enabled'] else 'Disabled')}")
    print(f"✅ API Key: {('Configured' if final_stats['api_key_set'] else 'Not Found')}")
    print(f"✅ Conversation History: {final_stats['history_length']} messages")
    
    # Offer interactive mode
    print("\n" + "=" * 80)
    choice = input("\nApakah Anda ingin test lebih lanjut secara interactive? (y/n): ").strip().lower()
    
    if choice == 'y':
        interactive_mode(robot)
    
    print("\n✨ Test selesai! ChatGPT fallback sudah siap digunakan.")

if __name__ == "__main__":
    main()
