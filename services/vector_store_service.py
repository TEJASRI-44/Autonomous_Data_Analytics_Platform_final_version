from langchain_chroma import Chroma

from langchain_core.documents import (
    Document
)
import uuid
from core.factories.embedding_factory import (
    EmbeddingFactory
)

from config.settings import (
    Settings
)


class VectorStoreService:

    @staticmethod
    def store_workflow_results(state):

        embeddings = (
            EmbeddingFactory
            .get_embeddings()
        )

        vector_store = Chroma(

            collection_name=(
                "analytics_copilot"
            ),

            persist_directory=str(
                Settings.VECTOR_DB_DIR
            ),

            embedding_function=embeddings
        )
        workflow_id = str(uuid.uuid4())
        documents = [

            Document(

                page_content=(
                    state["dataset_summary"]
                    .get(
                        "summary_report",
                        ""
                    )
                ),

                metadata={
                    "workflow_id":
                    workflow_id,

                    "dataset_name":
                    state["file_path"],
                    
                    "type":
                    "dataset_summary"
                }
            ),

            Document(

                page_content=(
                    state["eda_results"]
                    .get(
                        "eda_report",
                        ""
                    )
                ),

                metadata={
                    "workflow_id":
                    workflow_id,

                    "dataset_name":
                    state["file_path"],
                    
                    "type":
                    "eda"
                }
            ),

            Document(

                page_content=(
                    state["cleaning_results"]
                    .get(
                        "cleaning_report",
                        ""
                    )
                ),

                metadata={
                    "workflow_id":
                    workflow_id,

                    "dataset_name":
                    state["file_path"],
                    
                    "type":
                    "cleaning"
                }
            ),

            Document(

                page_content=(
                    state["statistical_results"]
                    .get(
                        "statistical_report",
                        ""
                    )
                ),

                metadata={
                    "workflow_id":
                    workflow_id,

                    "dataset_name":
                    state["file_path"],
                    
                    "type":
                    "statistics"
                }
            ),

            Document(

                page_content=(
                    state["insights"]
                    .get(
                        "insights_report",
                        ""
                    )
                ),

                metadata={
                    "workflow_id":
                    workflow_id,

                    "dataset_name":
                    state["file_path"],
                    
                    "type":
                    "insights"
                }
            ),

            Document(

                page_content=(
                    state["final_report"]
                ),

                metadata={
                    "workflow_id":
                    workflow_id,

                    "dataset_name":
                    state["file_path"],
                    
                    "type":
                    "final_report"
                }
            )
        ]

        vector_store.add_documents(
            documents
        )

        print(
            "\nWorkflow Results Stored In Vector DB"
        )