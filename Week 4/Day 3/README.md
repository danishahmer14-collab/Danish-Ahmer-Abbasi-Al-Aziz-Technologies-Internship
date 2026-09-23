# Week 4 — Day 3

## Task(s) Assigned
What is Hugging Face?
Model Hub
Transformers library
Pre-trained models
Tokenizers
Pipelines
Text classification
Text generation
Embeddings overview
Model inference
Local vs API-based inference
Model selection
GPU/CPU considerations
Hands-on:
Load a pretrained Transformer model.
Perform inference using Python.
Experiment with different models.

## What I Did
First, I had to configure my own environment (venv) and install the necessary modules using python -m pip install transformers torch. After the environment was set up, I wrote two Python scripts to accomplish the hands-on task. The script Tasksw4d3m1.py loads the DistilBERT model (distilbert-base-uncased-finetuned-sst-2-english) alongside its specific tokenizer to perform inference on sample sentences, classifying them as POSITIVE or NEGATIVE sentiment with a confidence score. Both scripts follow the same structure: loading the pre-trained model and matching tokenizer from the Hugging Face Model Hub, tokenizing the input text, making a forward pass through the model using torch.no_grad() for inference-only mode, and finally decoding and interpreting the output. I executed both scripts from the integrated terminal of VS Code and verified that the models were downloaded, stored locally, and ran successfully.

## Key Learnings
Hugging Face is a platform where pretrained ML models, datasets, and tools are stored, with the Model Hub offering thousands of models for anyone to download and use. The Transformers library provides a common Python API for loading virtually any model for any architecture. For a model to process raw text, the text must be broken down into numerical IDs by a specific tokenizer. The easiest way to perform inference for common tasks is by using pipelines, while manually loading the tokenizer and model provides much more control over data preprocessing and result handling. Text classification generates a label and a confidence score, whereas text generation predicts and generates new tokens from a prompt. Embeddings act as numerical vectors representing the meaning of text, which can be used for semantic search and similarity comparisons. Model inference simply refers to passing input into an existing model to obtain a prediction without any training or weight updates. Local inference is free and private but limited by hardware, whereas API-based inference is faster to deploy but incurs network latency and per-use costs. Model selection heavily depends on the task, model size, license, and language support, with smaller distilled models like DistilBERT being well-suited for rapid experimentation with limited data. For these small models, a CPU is generally good enough, but GPU acceleration is highly beneficial when processing heavy amounts of text or running larger models. Finally, switching between various pre-trained models by simply modifying the MODEL_NAME string demonstrated the flexibility and adaptability of the Transformers API, allowing different models to easily achieve similar results.

## Files in this folder
- `Tasksw4d3m1.py` — Loads DistilBERT and performs sentiment analysis (text classification) on sample sentences.
- `Tasksw4d3m2.py` — Loads GPT-2 and performs text generation on sample prompts.
