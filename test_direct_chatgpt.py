#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct ChatGPT Test - Bypass all local patterns
Tests ChatGPT integration by calling it directly
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from chatgpt_integration import ChatGPTFallback
import time

def test_direct_chatgpt():
    """Test ChatGPT directly"""
    print("=" * 80)
    print("🤖 DIRECT CHATGPT TEST (No Local Patterns)")
    print("=" * 80)
    print()
    
    # Initialize ChatGPT
    print("🔄 Initializing ChatGPT...")
    chatgpt = ChatGPTFallback(enable=True)
    
    print("\n📊 Status:")
    print(f"  • Enabled: {'✓' if chatgpt.enable else '✗'}")
    print(f"  • Model: {chatgpt.model}")
    print(f"  • API Key Set: {'✓' if chatgpt.api_key else '✗'}")
    print(f"  • Client Ready: {'✓' if chatgpt.client else '✗'}")
    print()
    
    if not chatgpt.enable:
        print("❌ ChatGPT tidak aktif!")
        return
    
    # Test queries yang pasti tidak akan match local patterns
    test_queries = [
        "Tell me an interesting fact about the universe",
        "Apa yang membuat Python menjadi bahasa pemrograman yang populer?",
        "Bagaimana cara meningkatkan produktivitas dalam pekerjaan?",
    ]
    
    print("=" * 80)
    print("🧪 RUNNING DIRECT CHATGPT TESTS")
    print("=" * 80)
    print()
    
    for i, query in enumerate(test_queries, 1):
        print(f"[Test {i}] ChatGPT Direct Call")
        print(f"  Query: {query}")
        print(f"  ⏳ Calling ChatGPT API...")
        
        start_time = time.time()
        response = chatgpt.get_response(query, user_name="Tester")
        elapsed = time.time() - start_time
        
        if response:
            print(f"  ✓ Response received in {elapsed:.2f}s")
            print(f"  Response: {response[:200]}{'...' if len(response) > 200 else ''}")
            print()
        else:
            print(f"  ❌ No response (error or timeout)")
            print()
    
    print("=" * 80)
    print("✨ TEST COMPLETE")
    print("=" * 80)
    print()
    print("📊 Final Status:")
    print(f"  • Conversation History: {len(chatgpt.conversation_history)} messages")
    print(f"  • History saved to: {chatgpt.history_file}")
    print()

if __name__ == "__main__":
    test_direct_chatgpt()
