
Moderated multi-agent group chat.


## Developer Notes

### 1. Initialize the Python environment with `uv`
- Create a virtual environment:
  ```sh
  uv venv
  ```
- Activate the virtual environment:
  ```sh
  source .venv/bin/activate  # select the appropriate activate.* for your shell
  ```
- Install dependencies:
  ```sh
  uv sync 
  ```

### 2. Set up configuration files
- Copy the environment template and edit as needed:
  ```sh
  cp .env.template .env
  # Edit .env to set your environment variables
  ```
- Copy the Neo4j connections example and edit as needed:
  ```sh
  cp neo4j.example.json neo4j.json
  # Edit neo4j.json to configure your Neo4j connections
  ```

### 3. Run the agent using `adk`
- Start the agent web server:
  ```sh
  adk web
  ```

You should now be able to access the agent locally. See below for more details or troubleshooting steps.
