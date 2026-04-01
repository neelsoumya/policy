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
CHROMA_DB = os.environ.get("CHROMA_DB", "output/chroma_db")
COLLECTION_NAME = "space_commons"