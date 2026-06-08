import os
import chromadb
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path ="chroma_db")
collection = client.get_or_create_collection(name = "papers", metadata = {"hnsw:space":"cosine"})

app = Flask(__name__)
CORS(app)

def retrieve(query: str, k: int =5)->list[str]:
    query_embedding = model.encode(query)
    result = collection.query(
        query_embeddings = query_embedding,
        n_results = k
    )
    usable_result = []
    for x in range(len(result["documents"][0])):
        return_dict = {}
        return_dict["text"] = result["documents"][0][x]
        return_dict["source"] = result["metadatas"][0][x]["source"]
        return_dict["distance"] = result["distances"][0][x]
        usable_result.append(return_dict)
    return usable_result

load_dotenv(dotenv_path=Path(__file__).parent/".env",override = True)
groq_client = Groq(api_key =os.getenv("GROQ_API_KEY"))

def generate_ans(query:str, k: int =5)->str:
    answers = retrieve(query)
    content = "\n\n".join(f"[Source: {chunk["source"]}]\n{chunk["text"]}" for chunk in answers)
    content =   f"Question: {query}\n\nContext from research papers:\n\n"+content+"\n\nAnswer the question using only this context."
    
    response = groq_client.chat.completions.create(
        model = "llama-3.3-70b-versatile",
        messages = [{"role":"system", "content": "You are a research assistant that answers questions using excerpts from academic papers.\n\nRules:\n1. Answer using ONLY the provided context. Do not use outside knowledge, even if you know the answer.\n2. If the context does not contain enough information to answer the question, respond with: \"I don't have enough information from the provided papers to answer this question.\" Do not guess or fabricate.\n3. Cite the source paper(s) you used. Use phrasing like \"According to [Paper Name]...\" or \"[Paper Name] describes...\"\n4. Be concise and accurate."},
                    {"role":"user", "content":content}],
        temperature = 0.2
    )
    return response.choices[0].message.content

@app.route("/ask", methods = ["POST"])
def ask():
    data = request.get_json()
    query = data["query"]
    try:
        answer = generate_ans(query)
        return jsonify({"answer":answer})
    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"}), 500
@app.route("/")
def home():
    return send_from_directory(".","index.html")

if __name__ == "__main__":
    app.run(debug= True)


