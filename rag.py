from huggingface_hub import InferenceClient

from config import HF_TOKEN
from config import MODEL_NAME

from utils.transcript import get_transcript
from utils.embeddings import load_embeddings
from utils.vectorstore import create_retriever
from utils.prompt import create_prompt

client = InferenceClient(
    api_key=HF_TOKEN
)

embeddings = load_embeddings()

retriever = None


def load_video(video_id):

    global retriever

    transcript = get_transcript(video_id)

    retriever = create_retriever(
        transcript,
        embeddings
    )


def ask_question(question):
    if retriever is None:
        raise ValueError("No video loaded.")

    docs = retriever.invoke(question)

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    prompt = create_prompt(
        context,
        question
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.2,
        max_tokens=1000
    )

    return response.choices[0].message.content