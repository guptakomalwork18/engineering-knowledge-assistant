
from app.services.rag_service import build_prompt


question = "How does Kafka handle parallel processing?"

context = """
[Source 1] (sample_kafka_notes.pdf, Page 2):
Kafka distributes partitions across consumers in a consumer group.

[Source 2] (sample_kafka_notes.pdf, Page 3):
Each partition is assigned to only one consumer within a consumer group.
"""

prompt = build_prompt(
    question=question,
    context=context,
)

print("Prompt generated successfully!")
print("\nGenerated Prompt:\n")
print(prompt)

assert question in prompt
assert "[Source 1]" in prompt
assert "[Source 2]" in prompt
assert "ONLY" in prompt

print("\nAll prompt construction checks passed!")
