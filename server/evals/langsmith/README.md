# LangSmith Evaluation

- Create dataset:
  - Way 1: Drag the data file to LangSmith "New Dataset"
  - Way 2: Run script
    ```
    cd server
    uv run langsmith/dataset.py
    ```


- Run evaluation:
```
cd server
uv run langsmith/experiment.py
```
