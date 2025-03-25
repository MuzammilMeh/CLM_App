import logging
import os


from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
)

import glob
from llama_index.llms.openai import OpenAI


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from llama_index.llms.openai import OpenAI

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient

from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.core import Settings
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import qdrant_client

"

STORAGE_DIR = "./qdrant_storage"  # directory to cache the generated index
DATA_DIR = "./data"  # directory containing the documents to index

files = glob.glob(DATA_DIR)

# client = QdrantClient("localhost", port=6333)
# client = QdrantClient(path="./qdrant_data")

qdrant = QdrantClient(":memory:")

client = QdrantClient("http://localhost:6333")
# client = QdrantClient(path="./qdrant_data_new2")

# client = QdrantClient(path="./qdrant_data")
# vector_store = QdrantVectorStore(
#     collection_name="my_collection",
#     client=client,
#     enable_hybrid=True,
#     batch_size=20,
# )
# print(client.get_collections())
collections = client.get_collections()

print(type(collections))
collection_list = collections.collections
for collection in collection_list:
    collection_name = collection.name

if "my_collection" in collection_name:
    collection_exists = True
else:
    collection_exists = False
# print(collection_exists)


def get_index():
    logger = logging.getLogger("uvicorn")
    # check if storage already exists
    if not collection_exists:

        logger.info("Creating new index")
        embed_model = HuggingFaceEmbedding(
            model_name="sentence-transformers/all-mpnet-base-v2", max_length=512
        )
        # load the documents and create the index
        Settings.embed_model = embed_model

        documents = SimpleDirectoryReader(DATA_DIR).load_data()
        # client = QdrantClient(path=STORAGE_DIR)
        # how many sentences on either side to capture

        vector_store = QdrantVectorStore(
            collection_name="my_collection",
            client=client,
            enable_hybrid=True,
            batch_size=20,
        )

        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        Settings.chunk_size = 512

        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
        )

        logger.info("here")

        logger.info(f"Finished creating new index. Stored in {STORAGE_DIR}")
    else:
        # load the existing index
        logger.info(f"Loading index from {STORAGE_DIR}...")

        vector_store = QdrantVectorStore(
            "my_collection", client=client, enable_hybrid=True, batch_size=20
        )

        # vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        # storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
        # index = load_index_from_storage(storage_context)
        index = VectorStoreIndex.from_vector_store(vector_store)
        logger.info(f"Finished loading index from {STORAGE_DIR}")
    return index
