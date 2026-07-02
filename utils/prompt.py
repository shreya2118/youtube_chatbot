def create_prompt(context, question):

    return f"""
You are an AI assistant.

Answer ONLY from the transcript below.

If the answer is not available in the transcript,
reply:

"This is not discussed in the video, please give relevant video for this question."

Transcript:

{context}

Question:

{question}

Answer:
"""