#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test ChatGPT Fallback Integration"""

from robot_with_vocabulary import EnhancedRobotBrain

# Initialize robot
robot = EnhancedRobotBrain(
    enable_online_vocab=False,
    enable_wikipedia=False,  # Disable Wikipedia agar ChatGPT fallback bisa tested
    sync_on_startup=False
)

print("=" * 70)
print("🤖 TEST: CHATGPT FALLBACK INTEGRATION")
print("=" * 70)

# Test 1: Check ChatGPT status
print("\n✓ ChatGPT Status:")
stats_response = robot._handle_chatgpt_stats()
print(stats_response)

# Test 2: Simple fallback test (input yang tidak cocok dengan pattern)
print("\nTest Queries (yang tidak cocok dengan pattern lokal):\n")

test_queries = [
    "Apa pendapatmu tentang teknologi AI?",
    "Bagaimana cara menjadi programmer yang sukses?",
    "Saya mau belajar Python, mulai dari mana?",
    "Apa yang membuat kamu tertarik?",
]

for query in test_queries:
    print(f"🧑 Input: {query}")
    response = robot.process_input(query)
    # Print preview
    preview = response[:150] if len(response) > 150 else response
    print(f"🤖 Response: {preview}")
    if len(response) > 150:
        print(f"   (... total {len(response)} chars)")
    print()

# Test 3: Show conversation history
print("\nConversation History:")
history_stats = robot.chatgpt_fallback.get_stats()
print(f"Messages saved: {history_stats['history_length']}")

print("\n" + "=" * 70)
print("✓ Test selesai!")
print("=" * 70)
