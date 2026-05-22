from langchain_chroma import Chroma

from config.settings import (
    Settings
)

from core.factories.embedding_factory import (
    EmbeddingFactory
)


class VectorStoreFactory:

    @staticmethod
    def get_vectorstore():

        embeddings = (

            EmbeddingFactory
            .get_embeddings()
        )

        return Chroma(

            persist_directory=str(
                Settings.VECTOR_DB_DIR
            ),

            embedding_function=embeddings
        )