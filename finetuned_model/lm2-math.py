from transformers import AutoModelForCausalLM, AutoTokenizer


query="Find the sum of all integer bases $b>9$ for which $17_{b}$ is a divisor of $97_{b}$."
fewshots = ["Lorem "*1000, "Lorem ipsum "*1000]
fewshot_text = "\n\n".join(fewshots)

combined = f"Help to solve the user's query:\n{query}\n\nSome additional context that might help you\n{fewshot_text}"
combined = f"Some additional context that might help you\n{fewshot_text}\n\nHelp to solve the user's query:\n{query}"
print(combined)

# Load model and tokenizer
model_id = "LiquidAI/LFM2-350M-Math"
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    dtype="float32",
    # attn_implementation="flash_attention_2"
)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Create message
message = [
  {"role": "user", "content": combined},
]

# Generate answer
input_ids = tokenizer.apply_chat_template(
    message,
    add_generation_prompt=True,
    return_tensors="pt",
    tokenize=True,
).to(model.device)

output = model.generate(
    input_ids,
    do_sample=True,
    temperature=0.6,
    top_p=0.95,
    min_p=0.1,
    repetition_penalty=1.05,
    max_new_tokens=512,
)

print(tokenizer.decode(output[0], skip_special_tokens=False))