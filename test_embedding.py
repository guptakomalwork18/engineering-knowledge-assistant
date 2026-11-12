
from app.services.embedding_service import generate_embedding

text = "Apache Kafka is a distributed event streaming platform."

embedding = generate_embedding(text)

print("Embedding generated successfully!")
print("Vector dimensions:", len(embedding))
print("First 10 values:", embedding[:10])
