#!/usr/bin/env python3

import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig
from trl import SFTTrainer

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3"

TRAIN_FILE = "data/training/mrpl_sft_train.jsonl"
VAL_FILE = "data/training/mrpl_sft_val.jsonl"

OUTPUT_DIR = "mistral_mrpl_qlora"

print("=" * 80)
print("MRPL MISTRAL-7B QLoRA FINE-TUNING")
print("=" * 80)

print("\n[1/5] Loading MRPL datasets...")

train_dataset = load_dataset(
    "json",
    data_files=TRAIN_FILE,
    split="train",
)

val_dataset = load_dataset(
    "json",
    data_files=VAL_FILE,
    split="train",
)

print(f"Train examples: {len(train_dataset)}")
print(f"Validation examples: {len(val_dataset)}")

print("\n[2/5] Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

print("Tokenizer loaded.")

print("\n[3/5] Loading Mistral in 4-bit QLoRA mode...")

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto",
    torch_dtype=torch.bfloat16,
)

model.config.use_cache = False

print("Mistral loaded in 4-bit mode.")

print("\n[4/5] Configuring LoRA...")

peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
    ],
)

print("LoRA configured.")

print("\n[5/5] Starting training configuration...")

training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,

    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,

    gradient_accumulation_steps=4,

    learning_rate=2e-4,
    num_train_epochs=3,

    logging_steps=5,

    eval_strategy="steps",
    eval_steps=20,

    save_strategy="steps",
    save_steps=20,
    save_total_limit=2,

    bf16=True,

    gradient_checkpointing=True,

    optim="paged_adamw_8bit",

    report_to="none",

    remove_unused_columns=False,
)

trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    peft_config=peft_config,
)

print("\n" + "=" * 80)
print("TRAINING STARTING")
print("=" * 80)

trainer.train()

print("\n" + "=" * 80)
print("SAVING ADAPTER")
print("=" * 80)

trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"\nTraining complete.")
print(f"LoRA adapter saved to: {OUTPUT_DIR}")
