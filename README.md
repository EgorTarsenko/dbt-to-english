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