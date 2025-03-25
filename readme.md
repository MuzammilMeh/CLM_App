# CLM_api

**CLM_api** is a Python-based application that leverages natural language processing to generate responses based on user input. It embeds the data and stores it in a **Qdrant** vector database. When a user sends a query, the question is embedded and searched using **Qdrant's hybrid search**, returning relevant document results.

## Features

- **Natural Language Processing (NLP)**: Processes user queries and generates responses.
- **Vector Database Integration**: Uses Qdrant to store and retrieve embeddings efficiently.
- **Hybrid Search**: Combines keyword and semantic search for relevant document retrieval.
- **FastAPI-based API**: Provides an endpoint to interact with the system.

## Key Components

### `main.py`
- **Purpose**: Entry point for the application.
- **Functionality**:
  - Initializes the **FastAPI** application.
  - Sets up API routes (e.g., `/api/chat`).
  - Handles user requests and communicates with processing functions.

### `app/` Directory
- **Purpose**: Contains core application logic.
- **Subcomponents**:
  - `models.py`: Defines request and response data models using **Pydantic**.
  - `services.py`: Implements key functionalities:
    - Handles user messages.
    - Generates responses.
    - Interacts with **Qdrant** to store/retrieve embeddings.
  - `utils.py`: Contains utility functions for processing.

### `data/` Directory
- **Purpose**: Stores essential data files, such as pre-trained models or datasets.

### `qdrant_storage/` Directory
- **Purpose**: Persists Qdrant database data across sessions.

Prerequisites
-------------

Before setting up the project, ensure you have the following installed:

*   **Python 3.x**: The programming language used for the project.
    
*   **Docker**: To run the Qdrant vector database container.
    

Installation
------------

1.  bashCopyEditgit clone https://github.com/MuzammilMeh/CLM\_api.gitcd CLM\_api
    
2.  Use pip to install the required Python packages:bashCopyEditpip install -r requirements.txt
    
3.  Pull the Qdrant Docker image:bashCopyEditdocker pull qdrant/qdrantRun the Qdrant container:bashCopyEditdocker run -p 6333:6333 -p 6334:6334 \\ -v $(pwd)/qdrant\_storage:/qdrant/storage:z \\ qdrant/qdrantThis command maps the necessary ports and sets up a volume for data persistence.
    
4.  Create a .env file in the project root directory and define any necessary environment variables. Refer to .env.example if available.
    
5.  Execute the main Python script:bashCopyEditpython main.pyThe API should now be running and accessible.
    

Contributing
------------

If you'd like to contribute to **CLM\_api**, please follow these steps:

1.  Fork the repository.
    
2.  Create a new branch (git checkout -b feature/YourFeature).
    
3.  Commit your changes (git commit -m 'Add some feature').
    
4.  Push to the branch (git push origin feature/YourFeature).
    
5.  Open a pull request.