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


