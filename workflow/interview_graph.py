from typing import TypedDict, Optional
from langgraph.graph import StateGraph

from my_agents.interview_agent import interview_agent
from my_agents.feedback_agent import feedback_agent


# -----------------------------
# STATE
# -----------------------------
class InterviewState(TypedDict):
    user_profile: dict
    question: Optional[str]
    answer: Optional[str]
    feedback: Optional[str]
    step: int
    end: bool


# -----------------------------
# NODE: QUESTION
# -----------------------------
def question_node(state: InterviewState):

    step = state.get("step", 0)

    # 🔚 Stop after 3 questions OR exit
    if state.get("end", False) or step >= 3:
        return {"question": "🎉 Interview completed. Great job!"}

    q = interview_agent(
        state["user_profile"],
        state.get("answer")
    )

    return {
        "question": q,
        "step": step + 1
    }


# -----------------------------
# NODE: ANSWER
# -----------------------------
def answer_node(state: InterviewState):

    ans = input(f"\nQ: {state['question']}\nYour Answer: ")

    # 🔥 EXIT CONDITION
    if ans.lower() in ["exit", "quit", "stop"]:
        return {
            "answer": ans,
            "end": True
        }

    return {
        "answer": ans,
        "end": False
    }


# -----------------------------
# NODE: FEEDBACK
# -----------------------------
def feedback_node(state: InterviewState):

    fb = feedback_agent(state["answer"])

    print("\n📊 Feedback:")
    print(fb)

    return {"feedback": fb}


# -----------------------------
# ROUTING LOGIC
# -----------------------------
def route_after_question(state: InterviewState):

    if state.get("end", False):
        return "__end__"

    if state.get("step", 0) >= 3:
        return "__end__"

    return "answer"


# -----------------------------
# BUILD GRAPH
# -----------------------------
def build_interview_graph():

    graph = StateGraph(InterviewState)

    graph.add_node("question", question_node)
    graph.add_node("answer", answer_node)
    graph.add_node("feedback", feedback_node)

    graph.set_entry_point("question")

    # 🔥 Correct flow
    graph.add_conditional_edges("question", route_after_question)
    graph.add_edge("answer", "feedback")
    graph.add_edge("feedback", "question")

    return graph.compile()


# -----------------------------
# RUN TEST
# -----------------------------
if __name__ == "__main__":

    app = build_interview_graph()

    app.invoke({
        "user_profile": {
            "role": "Data Scientist",
            "skills": ["Python", "ML"]
        },
        "step": 0,
        "end": False
    })