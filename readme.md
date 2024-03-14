## Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```
Start vector database

```bash
docker pull qdrant/qdrant
```
```
docker run -p 6333:6333 -p 6334:6334 \
    -v $(pwd)/qdrant_storage:/qdrant/storage:z \
    qdrant/qdrant
```
Execute the main Python script:

```bash

python main.py
```

You can hit the API using the following endpoint:

http://0.0.0.0:8000/api/chat


using provided payload


{
    "messages":[
        {"role":"user","content":"<question>"}
    ]
}
