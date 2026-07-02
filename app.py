import streamlit as st
from urllib.parse import urlparse, parse_qs

from rag import load_video, ask_question

# ---------------- PAGE ---------------- #

st.set_page_config(
    page_title="YouTube RAG Chatbot",
    page_icon="🎥",
    layout="wide"
)

# ---------------- CSS ---------------- #

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.main-title{
    font-size:42px;
    font-weight:700;
    margin-bottom:0px;
}

.sub-title{
    color:gray;
    margin-bottom:25px;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages=[]

if "video_loaded" not in st.session_state:
    st.session_state.video_loaded=False

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🎥 YouTube RAG")

    st.write("Paste a YouTube URL")

    youtube_url=st.text_input(
        "Video URL",
        placeholder="https://www.youtube.com/watch?v=..."
    )

    load_btn=st.button(
        "📥 Load Video",
        use_container_width=True
    )

    st.divider()

    if st.button(
        "🗑 Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages=[]
        st.rerun()

# ---------------- URL ---------------- #

def extract_video_id(url):

    parsed=urlparse(url)

    if parsed.hostname=="youtu.be":
        return parsed.path[1:]

    if parsed.hostname in (
        "www.youtube.com",
        "youtube.com"
    ):
        return parse_qs(
            parsed.query
        )["v"][0]

    return None

# ---------------- LOAD VIDEO ---------------- #

if load_btn:

    video_id=extract_video_id(youtube_url)

    if video_id is None:

        st.sidebar.error("Invalid YouTube URL")

    else:

        with st.spinner("Loading transcript..."):

            load_video(video_id)

        st.session_state.video_loaded=True

        st.sidebar.success("✅ Video Loaded!")

# ---------------- TITLE ---------------- #

st.markdown(
    '<div class="main-title">🎥 YouTube RAG Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Ask questions about any YouTube video using Retrieval-Augmented Generation.</div>',
    unsafe_allow_html=True
)

# ---------------- CHAT HISTORY ---------------- #

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------- CHAT INPUT ---------------- #

prompt=st.chat_input(
    "Ask something about the video..."
)

if prompt:

    if not st.session_state.video_loaded:

        st.warning("Load a YouTube video first.")

        st.stop()

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer=ask_question(prompt)

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )