from langchain_huggingface import (
    HuggingFaceEmbeddings
)

from config.settings import (
    Settings
)


class EmbeddingFactory:

    @staticmethod
    def get_embeddings():

        return HuggingFaceEmbeddings(

            model_name=(

                Settings
                .EMBEDDING_MODEL
            )
        )