# AI-Powered Commerce Assistant

This project is an AI-powered product assistant that helps users find relevant products through natural language queries and image-based search. The system combines a user-friendly frontend, a smart multimodal backend, and a semantic recommendation engine.

---

## Technologies Used

| Component       | Technology                                |
| --------------- | ----------------------------------------- |
| Frontend        | Streamlit                                 |
| Backend API     | FastAPI                                   |
| Embedding Model | `sentence-transformers` (MiniLM)          |
| Image Model     | `CLIP` (via Hugging Face Transformers)    |
| Database        | SQLite3 (lightweight, file-based)         |
| LLM             | Google Gemini (via `google.generativeai`) |

### Why This Stack?

* **Streamlit** provides a fast building experience and clear UI for the user
* **FastAPI** is lightweight and supports async multimodal endpoints
* **CLIP + MiniLM** offer strong performance for visual and semantic similarity and easy to integrate
* **SQLite** is easy to set up and perfect for mockup/product catalogs
* **Gemini** is powerful for flexible, natural interaction and summarization

---

## 📦 Deliverables

### 1. 📃 Code Repository

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

## 🔄 How to Run

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


