from langchain_chroma import Chroma

from config.settings import Settings

from core.factories.embedding_factory import (
    EmbeddingFactory
)


class VectorRepository:

    @staticmethod
    def get_vector_store():

        embeddings = (
            EmbeddingFactory
            .get_embeddings()
        )

        return Chroma(

            collection_name=
            "analytics_copilot",

            persist_directory=str(
                Settings.VECTOR_DB_DIR
            ),

            embedding_function=
            embeddings
        )