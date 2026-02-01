# 🤖 Agentic AI RAG Chatbot with Reinforcement Learning

A production-ready **Retrieval-Augmented Generation (RAG)** chatbot that answers questions based on a specific PDF document (`Ebook-Agentic-AI.pdf`). It features a **Reinforcement Learning (RL)** loop that learns from human feedback to improve answers over time and a specialized engine for reading data tables.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Interface-FF4B4B.svg)
![Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange.svg)

---

## 🚀 Key Features

* **RAG Engine:** Retrieves precise answers from the source PDF with zero hallucinations.
* **Self-Learning (RL):** If you mark an answer as "Incorrect" and provide a fix, the bot remembers it for next time.
* **Table Intelligence:** Automatically detects when you ask for "lists" or "capabilities" and formats the data into clean Markdown tables.
* **Dual Interface:**
    * **Web UI:** A modern Streamlit dashboard with feedback buttons.
    * **Terminal:** A fast CLI for quick testing and database initialization.
* **Citation System:** Every answer cites the specific page number from the PDF.

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-name>

```

### 2. Install Dependencies

Make sure you have Python installed, then run:

```bash
pip install -r requirements.txt

```

### 3. Configure API Keys (IMPORTANT)

⚠️ **Note:** The `.env` file is NOT included in this repository for security reasons. You must create it yourself.

1. Create a file named `.env` in the root folder.
2. Paste the following content into it:
```ini
GOOGLE_API_KEY=your_actual_api_key_here
MODEL_NAME=gemini-2.0-flash
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

```


3. Replace `your_actual_api_key_here` with your Google Gemini API key. (Get one [here](https://aistudio.google.com/app/apikey)).

### 4. Initialize the Database

Before the first run, you must process the PDF and build the vector database:

```bash
python main.py --init

```

*Wait for the message: "✅ System Ready"*

---

## 🖥️ How to Run

### **Option 1: Web Interface (Recommended)**

Use the full visual interface with feedback controls.

```bash
streamlit run app.py

```

*The app will open in your browser at `http://localhost:8501*`

### **Option 2: Terminal Mode**

Chat directly in your command line.

```bash
python main.py

```

---

## 🧠 How the Learning Works

1. **Ask a Question:** (e.g., *"What is Agentic AI?"*)
2. **Review Answer:** The bot retrieves context from the PDF.
3. **Give Feedback:**
* Click **👍 Correct** to reinforce the behavior.
* Click **👎 Incorrect** to open the correction form.


4. **Teach:** Type the correct answer and submit.
5. **Verify:** Ask the same question again. The bot will now reply with **[Learned Answer]** followed by your correction.

---

## 📂 File Structure

* `app.py`: Main Streamlit web application.
* `main.py`: CLI script and database initializer.
* `rag_engine.py`: Core logic for retrieving data and generating answers.
* `feedback_manager.py`: Handles the Reinforcement Learning (RL) memory.
* `vector_store.py`: Manages the ChromaDB vector database.
* `table_parser.py`: Logic for extracting and formatting tables from text.
* `config.py`: Central settings (API keys, paths, params).
* `Ebook-Agentic-AI.pdf`: The source knowledge base.

---

## 📞 Troubleshooting

* **Error: `GOOGLE_API_KEY not found**`
* Make sure you created the `.env` file and it is in the same folder as `main.py`.


* **Error: `Model not found**`
* If `gemini-1.5-flash` is not available in your region, change `MODEL_NAME` to `gemini-pro` in your `.env` file.


* **Error: `Vector Store not initialized**`
* Run `python main.py --init` to rebuild the database.



---

### **Author**

* **Bollu Sai Likhitha** 

```

```
