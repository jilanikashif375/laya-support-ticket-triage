from __future__ import annotations

import time
import sys
from pathlib import Path
from typing import Any

import streamlit as st
from laya import Router


SAMPLE_MESSAGES = {
    "Duplicate subscription charge": (
        "I just checked my bank app and the subscription payment went through twice this "
        "morning. Could you reverse one of the charges? I need that money for rent."
    ),
    "Login blocked before a deadline": (
        "I have tried the sign-in code three times and now my account is locked. I need to "
        "download the payroll report before 4pm today. Can someone unlock it?"
    ),
    "Payment missing from account": (
        "My card was charged for a $50 wallet top-up about 20 minutes ago, but the balance "
        "still says zero. Please check whether the payment went through."
    ),
    "Delivery delayed": (
        "The tracking page has not updated since Monday and the package was supposed to "
        "arrive yesterday. I am travelling tomorrow, so please let me know where it is."
    ),
    "Production outage": (
        "URGENT: our team cannot deploy or access the dashboard right now. This started "
        "about 10 minutes ago and is blocking all customer support. The status page says "
        "everything is operational."
    ),
    "Cancel renewal and request refund": (
        "Please cancel my annual plan before it renews again. I was billed this morning "
        "even though I thought I had turned auto-renew off. I would appreciate a refund."
    ),
    "Security alert": (
        "I received two password-reset emails that I did not request. I can still log in, "
        "but I am worried someone has access to my account. Please secure it immediately."
    ),
    "Invoice discrepancy": (
        "Hello, the invoice total is $240 higher than the quote we approved. Our finance "
        "team closes the books on Friday; could you check the itemized charges and send "
        "a corrected invoice if needed?"
    ),
    "Plan and tax details question": (
        "Good afternoon. Could you please confirm whether the Pro plan supports multiple "
        "billing contacts and whether the tax address can be updated after purchase? "
        "Thank you."
    ),
    "App crash after update": (
        "Since installing the latest update, the app freezes whenever I attach a photo "
        "and then closes. I have restarted my phone and reinstalled it, but the problem "
        "is still happening."
    ),
    "Positive feedback and feature request": (
        "Your team was really helpful when I had trouble setting things up, thank you! "
        "One small request: it would be great if reports could be exported as CSV."
    ),
    "Unclear account access question": (
        "Hi, I am setting up a new phone and want to make sure I do not lose my saved "
        "settings. Is there anything I should do before I sign in on the new device?"
    ),
}

SENTIMENT_OPTIONS = {
    "positive": "The customer expresses satisfaction, gratitude, or praise",
    "neutral": "The message is mainly factual or asks a question without clear emotion",
    "negative": "The customer expresses dissatisfaction, frustration, or disappointment",
}

TOPIC_OPTIONS = {
    "billing_and_payments": "Charges, refunds, invoices, subscriptions, or payment status",
    "account_access": "Sign-in, password, verification, or account recovery",
    "technical_support": "Bugs, errors, crashes, performance, or service availability",
    "orders_and_delivery": "Order status, shipping, delivery, or missing items",
    "cancellation_and_retention": "Plan cancellation, renewal, downgrade, or retention",
    "product_information": "Questions about features, plans, or how the product works",
    "security_and_privacy": "Suspicious activity, account compromise, or privacy concerns",
    "feedback_and_feature_request": "Product feedback, suggestions, or compliments",
    "other": "A support request that does not fit the categories above",
}

TEAM_OPTIONS = {
    "billing_support": "Payments, invoices, refunds, and subscription charges",
    "account_support": "Login, password, verification, and account recovery",
    "technical_support": "Product defects, service incidents, and troubleshooting",
    "order_support": "Order fulfilment, shipping, and delivery",
    "retention_team": "Cancellation, renewal, downgrade, and save requests",
    "product_advice": "Plan, feature, and product usage questions",
    "trust_and_safety": "Account security, suspicious access, and privacy",
    "customer_experience": "Complaints, compliments, and feature suggestions",
    "general_support": "Requests that need general triage",
}

URGENCY_LEVELS = [
    "Routine: no time pressure or immediate impact",
    "Low: can wait; limited inconvenience",
    "Moderate: customer is blocked or has a near-term deadline",
    "High: significant impact or urgent deadline",
    "Critical: active outage, security incident, or widespread immediate harm",
]

FORMALITY_LEVELS = [
    "Very casual: slang, shorthand, or highly conversational",
    "Casual: informal everyday language",
    "Neutral: straightforward and neither notably formal nor casual",
    "Polite professional: courteous business communication",
    "Very formal: highly formal or ceremonial language",
]

QUESTIONS = {
    "sentiment": {
        "type": "choice",
        "instructions": "Classify the customer's overall sentiment in this message.",
        "criteria": SENTIMENT_OPTIONS,
    },
    "topic": {
        "type": "choice",
        "instructions": "Choose the main topic of the customer's support request.",
        "criteria": TOPIC_OPTIONS,
    },
    "support_team": {
        "type": "choice",
        "instructions": "Route this incoming support request to the best team.",
        "criteria": TEAM_OPTIONS,
    },
    "urgency": {
        "type": "score",
        "instructions": (
            "Rate how urgently this support request needs attention, using the scale "
            "from routine to critical."
        ),
        "criteria": URGENCY_LEVELS,
    },
    "formality": {
        "type": "score",
        "instructions": (
            "Rate the formality of the customer's writing, from very casual to very formal."
        ),
        "criteria": FORMALITY_LEVELS,
    },
}


@st.cache_resource
def get_router() -> Router:
    return Router()


def load_selected_sample() -> None:
    selected = st.session_state.get("sample_message")
    st.session_state["incoming_message"] = SAMPLE_MESSAGES.get(selected, "")


def render_choice_result(title: str, answer: dict[str, Any]) -> None:
    st.subheader(title)
    st.metric("Prediction", answer["choice"])
    st.caption(f"Answer confidence: {answer['answer_confidence']:.0%}")
    probabilities = answer["probabilities"]
    st.dataframe(
        [
            {"Option": label, "Probability": f"{probability:.1%}"}
            for label, probability in probabilities.items()
        ],
        hide_index=True,
        width="stretch",
    )


def render_score_result(
    title: str, answer: dict[str, Any], levels: list[str]
) -> None:
    st.subheader(title)
    score = float(answer["score"])
    nearest_level = min(round(score), len(levels) - 1)
    st.metric("Expected score", f"{score:.2f} / {len(levels) - 1}")
    st.caption(f"Closest level: {levels[nearest_level]}")
    st.caption(f"Answer confidence: {answer['answer_confidence']:.0%}")
    probabilities = answer["probabilities"]
    st.dataframe(
        [
            {
                "Level": f"{level}: {levels[int(level)]}",
                "Probability": f"{probability:.1%}",
            }
            for level, probability in probabilities.items()
        ],
        hide_index=True,
        width="stretch",
    )


def main() -> None:
    st.set_page_config(page_title="Live Support Message Tester", page_icon="📨", layout="wide")
    st.title("Live Support Message Tester")
    st.write(
        "Test sentiment, topic classification, support-team routing, urgency, and "
        "formality on a realistic incoming customer message."
    )
    st.caption(
        "The examples below are synthetic test messages written to resemble live support "
        "tickets; paste an actual incoming message to test your own data."
    )

    st.session_state.setdefault("incoming_message", "")
    st.selectbox(
        "Load a realistic sample ticket",
        options=[None, *SAMPLE_MESSAGES.keys()],
        format_func=lambda name: "Choose a sample or paste a live message" if name is None else name,
        key="sample_message",
        on_change=load_selected_sample,
    )
    message = st.text_area(
        "Incoming customer message",
        key="incoming_message",
        height=180,
        placeholder="Paste or type the latest incoming support message here...",
    )

    if st.button("Analyze incoming message", type="primary", disabled=not message.strip()):
        with st.spinner("Classifying message with Laya..."):
            started_at = time.perf_counter()
            try:
                result = get_router().predict(message.strip(), QUESTIONS)
            except Exception as error:
                st.error(f"Message analysis failed: {error}")
                st.exception(error)
                return
            elapsed_seconds = time.perf_counter() - started_at

        st.divider()
        st.subheader("Analysis")
        overview = st.columns(3)
        overview[0].metric("Model", result["model"])
        overview[1].metric("Analysis time", f"{elapsed_seconds:.2f} sec")
        overview[2].metric("Checks completed", len(result["answers"]))

        if "routing" in result:
            with st.expander("Language/model routing details"):
                st.json(result["routing"])

        answers = result["answers"]
        choice_columns = st.columns(3)
        with choice_columns[0]:
            render_choice_result("Sentiment", answers["sentiment"])
        with choice_columns[1]:
            render_choice_result("Topic", answers["topic"])
        with choice_columns[2]:
            render_choice_result("Suggested support team", answers["support_team"])

        score_columns = st.columns(2)
        with score_columns[0]:
            render_score_result("Urgency", answers["urgency"], URGENCY_LEVELS)
        with score_columns[1]:
            render_score_result("Formality", answers["formality"], FORMALITY_LEVELS)


if __name__ == "__main__":
    main()
