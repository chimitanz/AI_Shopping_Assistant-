# AI-Powered Shopping Assistant

This project is an AI-powered product assistant that helps users find relevant products through natural language queries and image-based search. The system combines a user-friendly frontend, a smart multimodal backend, and a semantic recommendation engine.

---

## Technologies Used

| Component       | Technology                             |
| --------------- |----------------------------------------|
| Frontend        | Streamlit                              |
| Backend API     | FastAPI                                |
| Embedding Model | `sentence-transformers` (MiniLM)       |
| Image Model     | `CLIP` (via Hugging Face Transformers) |
| Database        | SQLite3 (lightweight, file-based)      |
| LLM             | gemini-1.5-flash                       |

* **Streamlit** was chosen for its simplicity and speed in building user-facing interfaces. It allows rapid development of a chat-like UI with image upload support.

* **FastAPI** is a lightweight and developer-friendly web framework that makes it easy to define structured APIs. It was selected for its simplicity, fast development experience.

* **MiniLM** was selected as the text embedding model for semantic search. It provides sentence embeddings at low computational cost.

* **CLIP** was used as the visual encoder for image-based product search. CLIP maps both images into a shared embedding space, allowing image queries to be compared directly with product image.

* **SQLite** was selected because the project does not require handling large-scale concurrent access or complex relational queries. It is lightweight, serverless, and easy to set up.

* **Gemini 1.5 Flash** was selected for its fast response speed and low cost. Since the assistant mainly needs to extract intent and generate short replies.

---

## Deliverables

### 1. Code Repository

* Fully documented code with modular structure
* Database generation scripts, product loading, embedding generation

### 2. User-Friendly Frontend

* Conversational UI using Streamlit
* Supports image uploading and text input in a unified chat window

### 3. Agent API

#### `POST /chat`

Handles both text-based and image-based product search.

**Input:**

```json
{
  "text": "looking for a fruity drink",
  "image_path": "images/sample.png",
  "history_prompt": "User: ...\nAssistant: ..."
}
```

**Output:**

```json
{
  "text": "Here are some refreshing options you might like!",
  "recommendations": [
    {
      "name": "Peach Iced Tea",
      "image_path": "images/ice_tea.jpg",
      "link": "https://example.com/peach-iced-tea"
    }
  ],
  "image_url": null
}
```

---

## How to Run

1. Clone the repository
2. Install dependencies 
3. Run backend:

```bash
uvicorn main:app --reload --port 8600
```

4. Run frontend:

```bash
streamlit run ui.py
```


