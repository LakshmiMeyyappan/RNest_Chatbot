# RNest Care FAQ Chatbot (RAG)

A small chatbot that answers questions about RNest Care using only an FAQ document.
If the answer is not in the FAQ, it says it does not know instead of guessing.

## How it works

```
rnest_faq.md -> split into chunks -> embeddings -> ChromaDB (vector store)

User question -> embedding -> find top 3 chunks -> Groq LLM -> answer
```

1. The FAQ has 38 Q&A pairs. Each pair is one chunk.
2. Chunks are stored in ChromaDB, which creates the embeddings with its default model.
3. For each question, the 3 closest chunks are found.
4. The chunks and the question go to a Groq model (`llama-3.1-8b-instant`).
5. The prompt tells the model to answer only from the chunks and not to give medical advice.

## Tech used

- Python 3.14 (tested on this version)
- ChromaDB (vector store, runs in memory)
- Groq API (LLM)
- FastAPI + Uvicorn (backend)
- Plain HTML, CSS and JavaScript (chat window)

## Files

| File | What it does |
|---|---|
| `rag.py` | Loads the FAQ, builds the vector store, answers questions |
| `chat.py` | Test the bot in the terminal |
| `api.py` | FastAPI app: `POST /chat`, `GET /health`, `GET /` (chat page) |
| `widget.html` | The chat window (one file, no other CSS or JS files) |
| `rnest_faq.md` | FAQ used by the code |
| `rnest_faq.pdf` | Same FAQ in PDF, for reading |
| `Dockerfile` | To build a container image |
| `requirements.txt` | Python packages |

## Run locally

```
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file with your key:

```
GROQ_API_KEY=your_key_here
```

Test in the terminal:

```
python chat.py
```

Run the web app:

```
uvicorn api:app --reload
```

Open http://127.0.0.1:8000/ to see the chat window.

## Run with Docker

```
docker build -t rnest-bot .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key_here rnest-bot
```

Note: the Docker build is not tested yet.

## API

`POST /chat`

```json
{ "question": "How much is Plus Care?" }
```

Response:

```json
{ "answer": "..." }
```

## Add to a website (for example WordPress)

Host the app on HTTPS, then paste this into a Custom HTML block:

```html
<iframe src="https://YOUR-APP-URL/" style="width:100%;max-width:420px;height:600px;border:0;border-radius:12px"></iframe>
```

## Notes for the deployment team

- Set `GROQ_API_KEY` as an environment variable. Do not put it in the code.
- Before going live, change `allow_origins=["*"]` in `api.py` to the RNest website address.
- The first start downloads the embedding model unless it was baked into the Docker image.
- The free Groq key has rate limits. Use a paid key or another model for real traffic.
- This is a test project. It has no login, no rate limiting and no chat history.
- The FAQ was written from the public pages of rnest.care and should be checked by RNest before real use.