# Week 5 — Day 1

## Task(s) Assigned
What are embeddings?
Text embeddings
Semantic similarity
Cosine similarity
Vector databases
Why vector search is required for AI applications
Chunking
Chunk size
Overlap
Metadata
Similarity search
Top-K retrieval
Hands-on:
Generate embeddings.
Store and search vectorized documents.

## What I Did
First I created my Own Enviroment and then I studied the theory behind embeddings and vector search, such as text embeddings, semantic similarity, cosine similarity, vector databases, chunking, metadata, similarity search and Top-K retrieval. Then, in VS Code I wrote all of the hands-on code in one Python file: Tasksw5d1.py. Implementing locally was done using Python, the sentence-transformers library (specifically the all-MiniLM-L6-v2 model), to locally generate 384-dimensional text embeddings, NumPy to calculate cosine similarity, and ChromaDB as the vector database.

First of all, I created embeddings of some sample sentences and saw their shape. Next, I wrote my own cosine similarity function based on the formula (A·B) / (|A|·|B|) and compared sentences using this function. I got some high results on sentences that shared nearly no words, such as a sentence about a cat sitting on a sofa and another sentence about a kitten sitting on a couch, but a sentence about the stock market got low. I then wrote a chunking function which breaks a document down into chunks of a certain word size and has a certain amount of overlap between chunks and tied metadata to each chunk that includes the source file name, chunk index, and category.

I chunked the text and then made a collection called ChromaDB with cosine distance, then embedded all the chunks and added them to the collection with the original text and metadata. Finally, I created a search function that will insert a user's query into the model, query the database for the top K most similar chunks, and print the chunks and their similarity score. I also tried the metadata filter to search for items within a single category and explored different categories, different queries and values of K, different chunk size and overlap sizes to observe how this affected the results.

## Key Learnings
I learnt that embedding is a technique to encode text into a vector space from a list of numbers, such that text segments with similar meanings are positioned close in the vector space. This is why semantic search exists: it looks for content, rather than by exact keywords, and can thus extract information from text even if the language is completely different. The measure used for comparing two embeddings is the cosine similarity and it examines the cosine of the angle between the two vectors, therefore a similarity score near to 1 indicates the texts are very similar, while a score near to 0 indicates that they have no relation.

I also got a grasp of the need of vector databases and vector search in AI applications. Language models have no knowledge of private or recent data, and can only process a certain number of words within a prompt; our documents are all stored as vectors, and we only fetch the most relevant part of the document for each question.

Another lesson that was important was chunking. If the large document contains more than one main focus, then it should be divided into smaller sections so that each of the vectors reflects one main focus. The decision of chunk size is a compromise – very small chunks lack context; very large chunks lose meaning; and a good size is about 200 to 500 tokens. Chunks overlap so that no information is lost at the end of each chunk, and metadata (such as source, category or page number) can be used to filter the results and display the source of an answer. Finally, I learned that the number of results returned is controlled by a parameter K, which can be either small (may not return the answer), or large (may return some noise); and that the embedding model has to be the same for the document and for the query, otherwise their vectors cannot be compared properly.

## Files in this folder
- `Tasksw5d1.py` — Complete hands-on code that generates embeddings, computes cosine similarity, chunks documents with overlap and metadata, stores vectors in ChromaDB and runs Top-K similarity search with metadata filtering.
- `chroma_db/` — Local ChromaDB folder created automatically when the script runs, which stores the vector database.
