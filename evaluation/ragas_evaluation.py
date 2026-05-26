from datasets import Dataset

from ragas import evaluate

from ragas.metrics import (

    faithfulness,

    answer_relevancy,

    context_precision,

    context_recall
)
from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from langchain_groq import (
    ChatGroq
)
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")

from agents.copilot_agent import (
    copilot_agent
)
from services.retriever_service import (
    RetrieverService
)
evaluator_llm = ChatGroq(

    model="llama-3.3-70b-versatile",

    temperature=0
)
embeddings = HuggingFaceEmbeddings(

    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"
)
questions = [

    "Summarize the complete analytics workflow findings.",

    "Which department generated the highest revenue and why?",


    "Which employees are likely to resign next month?"
]


ground_truths = [

    "The workflow identified business trends, correlations, anomalies, and actionable recommendations from the dataset.",

    "IT department generated the highest revenue due to strong operational and customer satisfaction performance.",

    "The dataset does not contain employee resignation or attrition information."
]
data = {

    "question": [],

    "answer": [],

    "contexts": [],

    "ground_truth": []
}

for question, truth in zip(
    questions,
    ground_truths
):

    retrieved_docs = (

        RetrieverService
        .retrieve_context(
            question
        )
    )

    retrieved_context = str(
        retrieved_docs
    )

    answer = "".join(

        copilot_agent(
            question,
            []
        )
    )
    data["question"].append(
        question
    )

    data["answer"].append(
        answer
    )

    data["contexts"].append(
        [retrieved_context]
    )

    data["ground_truth"].append(
        truth
    )
dataset = Dataset.from_dict(
    data
)

result = evaluate(

    dataset,

    metrics=[

        faithfulness,

        answer_relevancy
    ],

    llm=evaluator_llm,
    embeddings=embeddings,
    raise_exceptions=False
)


print(
    "\nRAGAS Evaluation Results:\n"
)

print(result)