from langchain_core.documents import (
    Document
)

import uuid

from repositories.vector_repository import (
    VectorRepository
)


class VectorStoreService:

    @staticmethod
    def store_workflow_results(state):
        
       
        vector_store = (
            VectorRepository
            .get_vector_store()
        )
        vector_store.delete_collection()
        
        vector_store = (
            VectorRepository
            .get_vector_store()
        )
        data = vector_store.get()

        print(data)
        workflow_id = str(
            uuid.uuid4()
        )

        documents = [

            Document(

                page_content=
                state["dataset_summary"]
                .get(
                    "summary_report",
                    ""
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

                page_content=
                state["eda_results"]
                .get(
                    "eda_report",
                    ""
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

                page_content=
                state["cleaning_results"]
                .get(
                    "cleaning_report",
                    ""
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

                page_content=
                state["statistical_results"]
                .get(
                    "statistical_report",
                    ""
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

                page_content=
                state["insights"]
                .get(
                    "insights_report",
                    ""
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

                page_content=
                state["final_report"],

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
        data = vector_store.get()

        print(data)

        print(
            "\nWorkflow Results Stored In Vector DB"
        )