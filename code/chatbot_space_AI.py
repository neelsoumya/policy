'''
A chatbot for space AI policy
'''

#####################
# Load packages
#####################
import os
import re
# import faiss # Facebook AI Similarity Search
import chromadb # for vector database managaement
import numpy as np
import gradio as gr # Gradio for building chatbot interface
from sentence_transformers import SentenceTransformer # For generatijng text embeddings
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

#####################
# Documents
#####################

DOCS = [
    "The Outer Space Treaty states that outer space shall be used for the benefit and in the interests of all countries.",
    "Outer space is to be explored and used for peaceful purposes.",
    "AI systems in space should be transparent, accountable, and subject to human oversight where risks are high.",
    "A global AI strategy for space should treat space as a commons and discourage militarization.",
    "Space sustainability requires debris mitigation, cooperation, and long-term stewardship.",
    "AI can support safer space governance by helping analyze scenarios, policies, and risks.",
    "Dual-use AI in space can create escalation, surveillance, and autonomy risks.",
    "International cooperation is essential for governing AI in outer space.",
]

# list of keywords considered safe
#.  r for raw string to avoid escape characetrs being invoked
SAFE_KEYWORDS = [
    r"weapon", r"weapons", r"target", r"missile", r"strike", r"kill", r"combat",
    r"surveillance", r"espionage", r"jamming", r"attack", r"explosive", r"offensive",
    r"military", r"drone", r"autonomous weapon", r"battle", r"sabotage"
]

SYSTEM_PROMPT = """You are a policy-focused AI assistant helping users re-envision a global AI strategy for space as a commons.
Prioritize peaceful use, safety, accountability, transparency, sustainability, and international cooperation.
Do not provide military, surveillance, targeting, offensive, or sabotage guidance.
If a request is harmful, refuse briefly and redirect to governance, ethics, or peaceful-use alternatives.
When possible, answer in concise policy language suitable for a manuscript or briefing note."""

#####################
# Models
#####################

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2" # for generating text embeddings
GEN_MODEL = os.environ.get("GEN_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", 220))
TOP_K = int(os.environ.get("TOP_K", "4"))
CHROMA_DIR = os.environ.get("CHROMA_DIR", "output/chroma_db")
COLLECTION_NAME = "space_commons"

#############################
# Initialize mebedding model
#############################

embedder = SentenceTransformer(EMBED_MODEL)
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# Add documents to ChromaDB collection if empty
if collection.count() == 0:
    print("Addng documents to ChromaDB collection\n")

    ids = [f"doc_{i}" for i in range(len(DOCS))]

    # generate embeddings for documents
    embeddings = embedder.encode(DOCS, 
                                 normalize_embeddings=True,
                                 convert_to_numpy=True)
    
    
    # if embedding is a tensor, convert to list
    if hasattr(embeddings, "tolist"):
        embeddings = embeddings.tolist()
        

    # add documents to collection
    collection.add(
        ids = ids, 
        documents = DOCS,
        embeddings = embeddings
    )


# Tokenizer
tokenizer = AutoTokenizer.from_pretrained(GEN_MODEL)
model = AutoModelForCausalLM.from_pretrained(
    GEN_MODEL,
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map = "auto" if torch.cuda.is_available() else None
)

if not torch.cuda.is_available():
    print("Warning: Running on CPU. This may be slow \n")
    model.to("cpu")


def is_harmful(text: str) -> bool:
    '''
    Check if harmful text
    '''
    t = text.lower()
    return any(re.search(p,t) for p in SAFE_KEYWORDS)


def retrieve(query: str, k: int = TOP_K):
    q = embedder.encode([query], normalize_embeddings=True).tolist()[0]
    result = collection.query(query_embeddings=[q], n_results=k)
    return result.get("documents", [[]])[0]

def build_prompt(query: str, ctx):
    context = "\n".join(f"- {c}" for c in ctx)
    return f"""{SYSTEM_PROMPT}\n\nContext:\n{context}\n\nUser question: {query}\n\nAnswer:"""

def generate(query: str, history):
    if not query.strip():
        return "Please ask a question about a global AI strategy for space."
    if is_harmful(query):
        return (
            "I can’t help with military, surveillance, or offensive space applications. "
            "I can help you frame the issue as a governance, safety, or peaceful-use question."
        )
    ctx = retrieve(query)
    prompt = build_prompt(query, ctx)
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=MAX_TOKENS,
            do_sample=True,
            temperature=0.4,
            top_p=0.9,
            eos_token_id=tokenizer.eos_token_id,
        )
    text = tokenizer.decode(output[0], skip_special_tokens=True)
    answer = text.split("Answer:", 1)[-1].strip()
    if not answer:
        answer = "I can help draft principles for a peaceful, globally governed AI strategy for space."
    answer += "\n\nSources considered: " + "; ".join(ctx)
    return answer


def chat(user_msg, history):
    history = history or []
    reply = generate(user_msg, history)
    history.append((user_msg, reply))
    return history, history


with gr.Blocks(title="Commons for Space Bot") as demo:
    gr.Markdown("# Commons for Space Bot\nA prototype chatbot for re-envisioning AI strategy for space as a global commons.")
    chatbot = gr.Chatbot(height=500)
    state = gr.State([])
    msg = gr.Textbox(label="Ask a question", placeholder="Example: What principles should a global AI strategy for space include?")
    send = gr.Button("Send")
    clear = gr.Button("Clear")

    send.click(chat, inputs=[msg, state], outputs=[chatbot, state])
    msg.submit(chat, inputs=[msg, state], outputs=[chatbot, state])
    clear.click(lambda: ([], []), outputs=[chatbot, state])


# TODO: run on Mac
#if torch.cuda.is_available():
#    device = torch.device("cuda")
#elif torch.backends.mps.is_available():
#    device = torch.device("mps")
#else:
#    device = torch.device("cpu")
#print(f"Using device: {device}")

#model = AutoModelForCausalLM.from_pretrained(
#    GEN_MODEL,
#    torch_dtype=torch.float16 if device.type in ["cuda", "mps"] else torch.float32,
#)
#model.to(device)

if __name__ == "__main__":
    demo.launch(share = True)
