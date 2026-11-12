
import os, csv
import chromadb
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# 1. Read the FAQ and split it into chunks
#text = open("rnest_faq.md", encoding="utf-8").read()
#chunks = [c.strip() for c in text.split("\n---\n")[1:] if c.strip()]
#print("Chunks loaded:", len(chunks))   # should print 38

# FOR APTASENTRY TEST
import csv

# risk level for each issue
risk = {}
with open("healthcare_risk_mapping.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        risk[r["issue_type"]] = r["risk_level"]

chunks, metas = [], []
with open("healthcare_knowledge_base.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        level = risk.get(r["issue_type"], "Unknown")
        chunks.append(
            f"Bucket: {r['bucket']}\nIssue: {r['issue_type']}\n"
            f"Risk level: {level}\nSolution: {r['solution']}"
        )
        metas.append({"bucket": r["bucket"], "issue_type": r["issue_type"],
                      "risk_level": level, "confidence": int(r["confidence"])})

print("Chunks loaded:", len(chunks))   # should print 7

# 2. Store the chunks in a vector database
db = chromadb.Client()
collection = db.create_collection("knowledge_base")
collection.add(documents=chunks, metadatas=metas,
               ids=[str(i) for i in range(len(chunks))])



# 3. Answer a question
def ask(question):
    result = collection.query(query_texts=[question], n_results=3)
    context = "\n\n".join(result["documents"][0])
    system = (
        "You are a support assistant. Answer ONLY from the context given. "
        "If the answer is not in the context, say you don't have that information. "
        "If the risk level is High, tell the user to use the official approval channel. "
        "Never share patient details, PINs or IDs."
    )
    reply = client.models.generate_content(
        model=MODEL,
        contents=f"Context:\n{context}\n\nQuestion: {question}",
        config=types.GenerateContentConfig(system_instruction=system, temperature=0),
    )
    return reply.text