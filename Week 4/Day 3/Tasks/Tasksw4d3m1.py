from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"

def load_model():
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    model.eval()
    return tokenizer, model

def predict_sentiment(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1)
    predicted_id = probs.argmax().item()
    label = model.config.id2label[predicted_id]
    confidence = probs[0][predicted_id].item()

    return label, confidence

if __name__ == "__main__":
    tokenizer, model = load_model()

    sample_texts = [
        "I absolutely loved this movie, it was fantastic!",
        "This was a complete waste of my time.",
        "The product works fine, nothing special though.",
        "Best customer service I've ever experienced.",
    ]

    print("\n--- Sentiment Analysis Results ---")
    for text in sample_texts:
        label, confidence = predict_sentiment(text, tokenizer, model)
        print(f"Text: {text}")
        print(f"  -> Prediction: {label} (confidence: {confidence:.4f})\n")