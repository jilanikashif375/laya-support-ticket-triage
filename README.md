# Laya Support Ticket Triage

A small Streamlit app demonstrating [Laya](https://huggingface.co/convaiinnovations/laya)
on incoming customer-support messages. Paste a message or select a realistic sample to
see structured predictions for sentiment, topic, support-team routing, urgency, and
formality.

## About Laya

Laya is an open-source family of non-autoregressive "System 1" decision models created by
Convai Innovations. Unlike a text-generation LLM that generates an answer token by token,
Laya takes a text or state object together with typed questions and returns structured
decisions and probabilities in a forward pass.

That makes Laya useful for tasks where the desired output is a decision rather than a
written response, such as classification, triage, routing, and scoring. Laya includes
English, multilingual, and typed-decision checkpoints. The `laya.Router` used in this demo
selects an appropriate checkpoint based on the input language.

## About this demo

This repository is a hands-on Laya example, not a new model or a live customer-ticket
integration. It uses `laya.Router.predict` to evaluate five typed questions against one
message:

- **Sentiment:** positive, neutral, or negative.
- **Topic:** such as billing, account access, technical support, or security.
- **Support team:** a suggested destination for the request.
- **Urgency:** a five-level score from routine to critical.
- **Formality:** a five-level score from very casual to very formal.

The interface shows the model's predictions, option probabilities, answer confidence,
selected model, and analysis time. It includes 12 realistic **synthetic** sample tickets;
it does not connect to an inbox or ingest a live ticket feed. Paste a current message
into the text area to test it yourself.

## Laya and Jev

Laya is described in the linked community articles as an open-source, self-hostable
alternative to Jev, a commercial decision-model API. Running a model locally can keep
inference within your own environment and avoid per-call API charges, though hardware,
hosting, and operational costs still apply. Compare the providers' current capabilities,
licensing, and pricing before choosing one for production.

## Suggested GitHub repository

- **Repository name:** `laya-support-ticket-triage`
- **Description:** `Streamlit demo of Laya for support-ticket sentiment, topic classification, team routing, urgency, and formality scoring.`

## Requirements

- Python 3.10–3.13
- Internet access the first time a Laya model checkpoint needs to be downloaded

## Setup

From the project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

```bash
streamlit run app.py
```

Select a sample ticket or paste a message, then click **Analyze incoming message**. The
first prediction may take longer while Laya loads or downloads a model checkpoint.

## Privacy

Treat pasted text as customer data. Use synthetic or appropriately redacted messages
unless you are authorized to process real customer information in your environment.
Model checkpoints may be downloaded from the model provider on first use. For production
use, review the model's license, deployment setup, and data-handling requirements.

## References

- [Laya model page](https://huggingface.co/convaiinnovations/laya)
- [How Laya works and how to run it locally](https://huggingface.co/blog/sora-2/laya-ai-model-how-it-works-run-it-locally-and-eval)
- [What is Laya?](https://daily.dev/posts/what-is-laya--ad3lt99k7)
- [Laya for multilingual classification on CPU](https://medium.com/@tuhinsharma121/laya-system-1-ai-for-multilingual-classification-on-cpu-1b29aaecbaa5)
- [Laya vs. Jev live demo](https://dev.to/vishalmysore/what-is-laya-laya-vs-jev-with-live-demo-4j6e)
- [Laya PHP self-hosted classification](https://laravel-news.com/laya-php-self-hosted-classification)
- [Laya vs. Jev discussion](https://www.youtube.com/watch?v=UoRNo5LoDRE)

See [`requirements.txt`](./requirements.txt) for the app dependencies.
