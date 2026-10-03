# Retrieval-Augmented Generation

RAG gives a language model access to private or recent knowledge without retraining it. The pipeline is: split documents into chunks, embed each chunk, store the vectors in a vector database, embed the user question, retrieve the most similar chunks, and place them in the prompt so the model answers from that context.

## Chunking

Chunking matters. Chunks that are too large dilute meaning and waste context window space. Chunks that are too small lose the surrounding context that makes a sentence understandable. Chunk overlap repeats a little text between neighbouring chunks so a sentence cut at a boundary is still found. A good starting point is 500 to 1000 characters with 10 to 20 percent overlap.

## Embeddings

An embedding is a list of numbers that represents the meaning of a piece of text. Texts with similar meaning end up close together in vector space. Cosine similarity compares the angle between two vectors and is the most common metric for text search.

## Reducing hallucination

To reduce hallucination, instruct the model to answer only from the provided context, cite its sources, and admit when it does not know the answer. Retrieval quality limits answer quality: if the right chunk is never retrieved, the model cannot use it.