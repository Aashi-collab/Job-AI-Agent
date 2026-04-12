import sys
import os

# Fix import path FIRST
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph

from memory.vector_memory import save_job, is_similar
from my_agents.job_agent import job_agent
from my_agents.resume_agent import resume_agent
from my_agents.cover_letter_agent import cover_letter_agent
from my_agents.apply_agent import apply_agent


# -----------------------------
# 🔹 STATE DEFINITION
# -----------------------------
class AgentState(TypedDict):
    user_profile: dict
    jobs: List[dict]
    selected_job: Optional[dict]
    resume: Optional[str]
    cover_letter: Optional[str]
    decision: Optional[str]
    feedback: Optional[str]


# -----------------------------
# 🔹 NODE 1: JOB AGENT
# -----------------------------
def job_node(state: AgentState):
    jobs = job_agent(state["user_profile"])
    return {"jobs": jobs}


# -----------------------------
# 🔹 NODE 2: DECISION
# -----------------------------
def decision_node(state: AgentState):

    if not state["jobs"]:
        return {
            "decision": "skip",
            "feedback": "No jobs found"
        }

    job = state["jobs"][0]

    # 🚫 check duplicate
    if is_similar(job):
        print("⚠️ Similar job found → skipping")

        return {
            "decision": "skip",
            "feedback": "Already applied to this job"
        }

    return {
        "selected_job": job,
        "decision": "apply"
    }


# -----------------------------
# 🔹 NODE 3: RESUME
# -----------------------------
def resume_node(state: AgentState):
    resume = resume_agent(
        state["selected_job"],
        state["user_profile"]
    )
    return {"resume": resume}


# -----------------------------
# 🔹 NODE 4: COVER LETTER
# -----------------------------
def cover_letter_node(state: AgentState):
    cl = cover_letter_agent(
        state["selected_job"],
        state["user_profile"]
    )
    return {"cover_letter": cl}


# -----------------------------
# 🔹 NODE 5: APPLY
# -----------------------------
def apply_node(state: AgentState):

    result = apply_agent(
        state["selected_job"],
        state["resume"],
        state["cover_letter"]
    )

    # 💾 save job
    save_job(state["selected_job"])

    return {"feedback": result}


# -----------------------------
# 🔹 ROUTING
# -----------------------------
def route_decision(state: AgentState):

    if state["decision"] == "apply":
        return "resume"

    return "__end__"


# -----------------------------
# 🔹 BUILD GRAPH
# -----------------------------
def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("job", job_node)
    graph.add_node("decision", decision_node)
    graph.add_node("resume", resume_node)
    graph.add_node("cover_letter", cover_letter_node)
    graph.add_node("apply", apply_node)

    graph.set_entry_point("job")

    graph.add_edge("job", "decision")
    graph.add_conditional_edges("decision", route_decision)
    graph.add_edge("resume", "cover_letter")
    graph.add_edge("cover_letter", "apply")
    graph.add_edge("apply", "__end__")

    return graph.compile()


# -----------------------------
# 🔹 TEST RUN
# -----------------------------
if __name__ == "__main__":

    app = build_graph()

    result = app.invoke({
        "user_profile": {
            "skills": ["Python", "AI"],
            "role": "Data Scientist"
        }
    })

    print("\n✅ RESULT:")
    print(result.get("feedback", "No feedback"))