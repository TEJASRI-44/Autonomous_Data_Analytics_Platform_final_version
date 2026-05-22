from core.factories.vectorstore_factory import (
    VectorStoreFactory
)


class RetrieverFactory:

    @staticmethod
    def get_retriever():

        vectorstore = (

            VectorStoreFactory
            .get_vectorstore()
        )

        return vectorstore.as_retriever()