#!/usr/bin/env python3
"""Test MRPL-trained Mistral"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel

print("\n" + "="*80)
print("TESTING MISTRAL-7B TRAINED FOR MRPL")
print("="*80 + "\n")

print("[1/3] Loading trained model...")
try:
    base_model = AutoModelForCausalLM.from_pretrained("mistral.ai/Mistral-7B-Instruct-v0.2", torch_dtype=torch.float16, device_map="auto")
    model = PeftModel.from_pretrained(base_model, "./mistral_mrpl_trained")
    tokenizer = AutoTokenizer.from_pretrained("mistral.ai/Mistral-7B-Instruct-v0.2")
    print("✓ Model loaded\n")
except Exception as e:
    print(f"❌ Error: {e}\n")
    exit(1)

# Test queries
tests = [
    {"id": 1, "name": "APPROVAL", "query": "Draft approval note for pump that has corrosion"},
    {"id": 2, "name": "INSPECTION", "query": "Summarize: Pressure 50 PSI (normal), vibration 0.12 (normal), no leaks"},
    {"id": 3, "name": "BOARD", "query": "Executive summary: Production +15%, downtime -10%, zero incidents"},
    {"id": 4, "name": "MAINTENANCE", "query": "Maintenance plan for 6-year-old distillation column"},
]

print("[2/3] Generating responses...\n" + "="*80)

for test in tests:
    print(f"\n[TEST {test['id']}] {test['name']}")
    print("-"*80)
    print(f"Query: {test['query']}\n")
    
    inputs = tokenizer(test['query'], return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=400, temperature=0.7, top_p=0.9, do_sample=True)
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).replace(test['query'], "").strip()
    print(f"Response:\n{response}")
    print("-"*80)

print("\n" + "="*80)
print("✅ TESTING COMPLETE")
print("="*80)
print("\nQuality Check:")
print("✓ Professional tone?")
print("✓ Relevant to MRPL?")
print("✓ Well-structured?")
print("✓ Industry knowledge?")
print("\nIf YES → Model is ready!")
print("="*80 + "\n")
