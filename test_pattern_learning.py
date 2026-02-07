#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test script untuk fitur pembelajaran pola percakapan dengan quoted strings"""

from robot_with_vocabulary import EnhancedRobotBrain

# Initialize robot
robot = EnhancedRobotBrain(
    enable_online_vocab=False,  # Disable untuk test cepat
    enable_wikipedia=False,
    sync_on_startup=False
)

print("=" * 60)
print("🤖 TEST: PEMBELAJARAN POLA PERCAKAPAN (QUOTED FORMAT)")
print("=" * 60)

# Test cases dengan quoted strings
test_inputs = [
    'Kalau ada yang bilang "Assalamualaikum", jawab nya "Waalaikumsalam"',
    'Kalau ada yang nanya "Ibu Kota Jawa Barat?" jawab nya "Bandung"',
    'Kalau ada yang bilang "Terima kasih", jawab nya "Sama-sama"',
]

for test_input in test_inputs:
    print(f"\n🧑 Input: {test_input}")
    response = robot.process_input(test_input)
    print(f"🤖 Response: {response}")

# Test if learned patterns work
print("\n" + "=" * 60)
print("🧪 Testing learned patterns...")
print("=" * 60)

test_triggers = [
    "Assalamualaikum",
    "Ibu Kota Jawa Barat?",
    "Terima kasih",
]

for trigger in test_triggers:
    print(f"\n🧑 Input: {trigger}")
    response = robot.process_input(trigger)
    print(f"🤖 Response: {response}")

print("\n" + "=" * 60)
print("✓ Test selesai!")
print("=" * 60)
