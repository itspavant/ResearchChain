"""
Streamlit UI for the multi-agent research pipeline.

This does NOT call run_research_pipeline() as a single black box -- instead it
re-implements the same 4 steps (search agent -> reader agent -> writer chain ->
critic chain) inline, so each stage's progress and output can be streamed to the
UI as it happens. The underlying agents/chains are imported unchanged from
agents.py, so the actual logic/prompts stay exactly as you built them.

Run with:
    streamlit run app.py
"""

import streamlit as st
from langchain_core.messages import ToolMessage

from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain


# ----------------------------- Page setup -----------------------------

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

st.title("Multi-Agent Research System")
st.caption("Search agent → Reader agent → Writer chain → Critic chain")

if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {topic, search, scraped, report, feedback}


# ----------------------------- Sidebar -----------------------------

with st.sidebar:
    st.header("About")
    st.write(
        "1. **Search agent** finds sources via web search\n"
        "2. **Reader agent** scrapes the most relevant URL\n"
        "3. **Writer chain** drafts a structured report\n"
        "4. **Critic chain** scores and critiques the report"
    )
    st.divider()
    if st.session_state.history:
        st.header("Past runs")
        for i, run in enumerate(reversed(st.session_state.history)):
            st.write(f"**{i + 1}.** {run['topic']}")


# ----------------------------- Input -----------------------------

with st.form("topic_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of quantum computing on cybersecurity",
    )
    submitted = st.form_submit_button("Run pipeline", type="primary", use_container_width=True)


# ----------------------------- Pipeline run -----------------------------

def run_pipeline_streamed(topic: str):
    """Runs the 4-stage pipeline, updating the UI live as each stage completes."""

    state = {}

    # ---- Step 1: Search agent ----
    step1 = st.status("Step 1 — Search agent is working...", expanded=True)
    with step1:
        search_agent = build_search_agent()
        search_result = search_agent.invoke(
            {"messages": [("user", f"Find recent, reliable and detailed information about:{topic}")]}
        )
        tool_messages = [
            msg.content for msg in search_result["messages"] if isinstance(msg, ToolMessage)
        ]
        state["search_results"] = "\n\n".join(tool_messages)
        st.markdown(state["search_results"] or "_No search results returned._")
    step1.update(label="Step 1 — Search complete", state="complete", expanded=False)

    # ---- Step 2: Reader agent ----
    step2 = st.status("Step 2 — Reader agent is scraping top resources...", expanded=True)
    with step2:
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Based on the following search results about '{topic}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{state['search_results'][:800]}",
                    )
                ]
            }
        )
        tool_messages = [
            msg.content for msg in reader_result["messages"] if isinstance(msg, ToolMessage)
        ]
        state["scraped_content"] = "\n\n".join(tool_messages)
        st.markdown(state["scraped_content"] or "_No scraped content returned._")
    step2.update(label="Step 2 — Scraping complete", state="complete", expanded=False)

    # ---- Step 3: Writer chain ----
    step3 = st.status("Step 3 — Writer is drafting the report...", expanded=True)
    with step3:
        research_combined = (
            f"SEARCH RESULTS : \n {state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT: \n {state['scraped_content']}"
        )
        state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
        st.markdown(state["report"])
    step3.update(label="Step 3 — Report drafted", state="complete", expanded=False)

    # ---- Step 4: Critic chain ----
    step4 = st.status("Step 4 — Critic is reviewing the report...", expanded=True)
    with step4:
        state["feedback"] = critic_chain.invoke({"report": state["report"]})
        st.markdown(state["feedback"])
    step4.update(label="Step 4 — Review complete", state="complete", expanded=False)

    return state


if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        try:
            result = run_pipeline_streamed(topic.strip())
            st.session_state.history.append({"topic": topic.strip(), **result})

            st.divider()
            st.subheader("📄 Final Report")
            st.markdown(result["report"])

            st.subheader("🧐 Critic Feedback")
            st.markdown(result["feedback"])

            st.download_button(
                "Download report as .md",
                data=f"# Research Report: {topic}\n\n{result['report']}\n\n---\n\n## Critic Feedback\n\n{result['feedback']}",
                file_name=f"{topic.strip().replace(' ', '_')}_report.md",
                mime="text/markdown",
            )
        except Exception as e:
            st.error(f"Pipeline failed: {e}")