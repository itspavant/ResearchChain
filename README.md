Live: [Click Here](https://researchchain.streamlit.app/)

# ResearchChain

ResearchChain is an autonomous multi-agent research platform built with **LangChain** that automates the research workflow using specialized AI agents. It performs web search, content extraction, report generation, and quality evaluation to produce structured research reports from a single user query.

## Features

- Multi-agent architecture with specialized AI agents
- Autonomous web search using Tavily Search
- Webpage content extraction and processing
- Structured research report generation
- AI-powered report evaluation and feedback
- Real-time agent execution tracking
- Execution timeline visualization
- Interactive Streamlit dashboard

## Architecture

```
User Query
     │
     ▼
Search Agent
     │
     ▼
Reader Agent
     │
     ▼
Writer Chain (LCEL)
     │
     ▼
Critic Chain (LCEL)
     │
     ▼
Final Research Report
```

## Tech Stack

- Python
- LangChain
- LCEL (LangChain Expression Language)
- Groq (Llama 3.3-70B)
- Tavily Search API
- BeautifulSoup
- Streamlit

## Project Structure

```
ResearchChain/
│── app.py
│── agents.py
│── tools.py
│── pipeline.py
│── requirements.txt
└── README.md
```

## Installation

```bash
git clone https://github.com/yourusername/ResearchChain.git
cd ResearchChain

pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Run

```bash
streamlit run app.py
```

## Workflow

1. User enters a research topic.
2. Search Agent retrieves relevant web sources.
3. Reader Agent extracts detailed content from selected sources.
4. Writer Chain generates a structured research report.
5. Critic Chain evaluates the report and provides feedback.
6. Results are displayed through the interactive dashboard.

## Future Improvements

- LangGraph-based agent orchestration
- Retrieval-Augmented Generation (RAG)
- Multi-source content synthesis
- PDF export support
- Multi-document research
- Citation management
- Local LLM support

## License

This project is licensed under the MIT License.
