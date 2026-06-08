import fitz
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

script_dir = Path(__file__).parent

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path =str(script_dir / "chroma_db"))
collection = client.get_or_create_collection(name = "papers", metadata = {"hnsw:space":"cosine"})
def parse_pdf(path:Path) -> str:
    text = ""
    pdf = fitz.open(path)
    for page in pdf:
        text += page.get_text()
    index = text.rfind("References")
    if(index != -1):
        text = text[:index]
    return text

def chunk(text: str, chunk_size: int = 1000, overlap: int =  200) -> list[str]:
    chunks = []
    for cursor in range(0,len(text),chunk_size-overlap):
        chunks.append(text[cursor:cursor+chunk_size])
    return chunks

def store_chunks(CHUNKS,EMBEDDINGS,source):
    id_s = []
    meta_datas = []
    for i in range(len(CHUNKS)):
        id_s.append(f"{source}_chunk_"+str(i))
        meta_dict = {"source":source}
        meta_dict['chunk_index'] = i
        meta_datas.append(meta_dict)
    collection.add(
        documents = CHUNKS,
        embeddings = EMBEDDINGS,
        ids = id_s,
        metadatas = meta_datas
    )

if collection.count() > 0:
    print("Collection is already polluted. Delete chromaDB folder to re-ingest")
else:
    for pdf_path in (script_dir / "RAG_PDFs").glob("*.pdf"):
        text = parse_pdf(pdf_path)
        CHUNKS = chunk(text)
        embeddings = model.encode(CHUNKS)
        store_chunks(CHUNKS, embeddings,pdf_path.stem)
