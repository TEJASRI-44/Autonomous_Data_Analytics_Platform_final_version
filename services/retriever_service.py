from langchain_chroma import Chroma

from core.factories.embedding_factory import (
    EmbeddingFactory
)

from config.settings import (
    Settings
)


class RetrieverService:

    @staticmethod
    def retrieve_context(query):

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

        retriever = (
            vector_store.as_retriever(
                search_kwargs={"k": 4}
            )
        )

        documents = retriever.invoke(
            query
        )

        context = "\n\n".join(

            [
                doc.page_content

                for doc in documents
            ]
        )

        return context