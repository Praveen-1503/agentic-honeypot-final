class AgentState:
    ENGAGE = "engage"
    EXTRACT = "extract"
    EXIT = "exit"


def agent_reply(state: str, turn: int, context: str = "") -> str:
    if state == AgentState.ENGAGE:
        return (
            "I’m not very familiar with this. "
            "Can you explain clearly?\n"
            f"{context}"
        )

    if state == AgentState.EXTRACT:
        return (
            "I tried but the payment failed. "
            "Please resend the correct UPI or link.\n"
            f"{context}"
        )

    return "Okay, thank you."