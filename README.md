# dbt-to-english

# Project Setup  

## Getting Started  

1. Copy the environment template file:  
   ```sh
   cp private.env-template private.env
   ```

2. Open private.env and add your AWS credentials if you use Bedrock:
    ```
    AWS_ACCESS_KEY_ID=your-access-key  
    AWS_SECRET_ACCESS_KEY=your-secret-key  
    AWS_REGION=your-region  
    ```

    If using Anthropic, add your API key instead:
    ```
    ANTHROPIC_API_KEY=
    ```

3. If you're using a different AWS Bedrock model, update the LLM_MODEL variable in private.env. If using Anthropic, uncomment the LLM_MODEL variable with `Anthropic` prefix and specify the desired model.

# Running the Project

Start the project using Docker Compose:

```
docker compose up --build
```

# UI

Visit [http://localhost:8501/](http://localhost:8501/) to access the Streamlit interface.

1. Upload both `catalog.json` and `manifest.json`.  
   If you don’t have a DBT project, you can use the sample files from `DbtExampleProject/target`.

2. Click the **"Parse JSON File"** button.

3. A new dropdown field labeled **"Select a node ID"** will appear. Choose the node(s) you want to parse.

4. Click the **"Submit"** button to proceed.

---

# Backend

The Streamlit UI communicates with a FastAPI backend. It uses the `/get_node_in_english` endpoint, which can also be used independently of Streamlit.

### Endpoint: `/get_node_in_english`

**Parameters:**
- `catalog_file`
- `manifest_file`
- `node_to_parse`
- `prompt`

This endpoint processes the provided inputs and returns a natural language interpretation of the selected node.
