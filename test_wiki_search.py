#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test ekstraksi keyword dari pertanyaan Wikipedia"""

from robot_with_vocabulary import EnhancedRobotBrain

# Initialize robot
robot = EnhancedRobotBrain(
    enable_online_vocab=False,
    enable_wikipedia=True,
    sync_on_startup=False
)

print("=" * 70)
print("🔍 TEST: EKSTRAKSI KEYWORD UNTUK WIKIPEDIA SEARCH")
print("=" * 70)

# Test cases
test_questions = [
    "apa itu intel Processor?",
    "apa itu Processor?",
    "siapa itu Mahatma Gandhi?",
    "bagaimana cara memasak nasi?",
    "apa yang dimaksud dengan algoritma?",
    "siapa sih Albert Einstein?",
    "apa nama ibu kota Indonesia?",
]

print("\n📝 Test Ekstraksi Keyword:\n")
for question in test_questions:
    extracted = robot._extract_wiki_search_query(question)
    print(f"Input:   '{question}'")
    print(f"Extract: '{extracted}'")
    print()

print("=" * 70)
print("\n🌐 Test Actual Wikipedia Search:\n")
print("(Requests akan dikirim ke Wikipedia API)")

actual_search_tests = [
    "apa itu intel Processor?",
    "siapa itu Albert Einstein?",
]

for question in actual_search_tests:
    print(f"\n🧑 Pertanyaan: {question}")
    response = robot._handle_wiki_search(question)
    # Print first 200 chars of response
    preview = response[:200] if len(response) > 200 else response
    print(f"🤖 Response preview: {preview}...")
    if len(response) > 200:
        print(f"   (Total: {len(response)} chars)")

print("\n" + "=" * 70)
print("✓ Test selesai!")
print("=" * 70)
