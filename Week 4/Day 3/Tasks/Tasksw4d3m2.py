from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "gpt2"

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model

def generate_text(prompt, tokenizer, model, max_new_tokens=40):
    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.8,
            pad_token_id=tokenizer.eos_token_id,
        )

    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return generated_text

if __name__ == "__main__":
    tokenizer, model = load_model()

    sample_prompts = [
        "The future of artificial intelligence is",
        "Once upon a time in a quiet village,",
        "The best way to learn programming is to",
    ]

    print("\n--- Text Generation Results ---")
    for prompt in sample_prompts:
        result = generate_text(prompt, tokenizer, model)
        print(f"Prompt: {prompt}")
        print(f"  -> Generated: {result}\n")