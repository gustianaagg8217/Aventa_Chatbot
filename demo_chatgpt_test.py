#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Demo: ChatGPT Fallback Testing
Cara mudah untuk test apakah ChatGPT sudah integrated
"""

from robot_with_vocabulary import EnhancedRobotBrain

def main():
    print("\n" + "=" * 80)
    print("🤖 SIMPLE CHATGPT FALLBACK TEST")
    print("=" * 80)
    
    # Initialize robot
    print("\n🔄 Initializing robot...")
    robot = EnhancedRobotBrain(
        enable_online_vocab=True,
        enable_wikipedia=False,
        sync_on_startup=False
    )
    print("✓ Robot ready\n")
    
    # Show status
    print("📊 ChatGPT Status:")
    stats = robot._handle_chatgpt_stats()
    print(stats)
    
    # Test kategorisasi
    print("\n" + "=" * 80)
    print("📝 TEST CATEGORIES EXPLANATION")
    print("=" * 80)
    
    categories = {
        "LOCAL PATTERN": {
            "example": "Halo",
            "description": "Match dengan greeting pattern lokal",
            "api_used": "❌ NO"
        },
        "VOCABULARY": {
            "example": "cari arti algoritma",
            "description": "Search di local vocabulary",
            "api_used": "❌ NO"
        },
        "CHATGPT FALLBACK": {
            "example": "Apa itu machine learning?",
            "description": "Tidak cocok pattern/vocab → triggered ChatGPT",
            "api_used": "✅ YES - API CALL"
        }
    }
    
    for category, info in categories.items():
        print(f"\n[{category}]")
        print(f"  Example: \"{info['example']}\"")
        print(f"  Description: {info['description']}")
        print(f"  API Used: {info['api_used']}")
    
    # Run actual tests
    print("\n" + "=" * 80)
    print("🧪 NOW RUNNING ACTUAL TESTS...")
    print("=" * 80)
    
    test_cases = [
        ("Halo", "LOCAL PATTERN", "❌ No API"),
        ("cari arti computer", "VOCABULARY", "❌ No API"),
        ("Apa itu artificial intelligence?", "CHATGPT FALLBACK", "✅ API CALL"),
        ("Bagaimana cara sukses?", "CHATGPT FALLBACK", "✅ API CALL"),
    ]
    
    for i, (query, category, api_info) in enumerate(test_cases, 1):
        print(f"\n[Test {i}] {category}")
        print(f"         {api_info}")
        print(f"-" * 80)
        print(f"🧑 Input: {query}")
        print("⏳ Processing...")
        
        response = robot.process_input(query)
        
        # Determine source
        is_chatgpt = (
            "Saya akan cari" not in response and
            "belum pernah" not in response and
            "tidak mengerti" not in response and
            len(response) > 80
        )
        
        source = "✅ ChatGPT Response" if is_chatgpt else "📌 Local Pattern/Vocab"
        print(f"🤖 [{source}]")
        print(f"   {response[:200]}{'...' if len(response) > 200 else ''}")
    
    # Final summary
    print("\n" + "=" * 80)
    print("✨ TEST COMPLETE")
    print("=" * 80)
    
    final_stats = robot.chatgpt_fallback.get_stats()
    
    print(f"\n✅ ChatGPT Enabled: {final_stats['enabled']}")
    print(f"✅ API Key Set: {final_stats['api_key_set']}")
    print(f"✅ Conversation History: {final_stats['history_length']} messages")
    
    print("\n📌 KESIMPULAN:")
    print("   Jika ada response yang panjang & detail untuk test 3-4,")
    print("   itu berasal dari ChatGPT ✓")
    print("\n   Jika semua response singkat = ChatGPT belum triggered")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
