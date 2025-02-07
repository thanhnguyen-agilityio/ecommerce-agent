import os

import requests
from openai import OpenAI


class FineTuningService:
    def __init__(
        self,
        client=OpenAI(),
        url="https://api.openai.com/v1/fine_tuning",
        api_key=os.getenv("OPENAI_API_KEY"),
    ):
        self.url = url
        self.api_key = api_key
        self.client = client

    def create_job(
        self,
        file_id,
        model="gpt-4o-mini-2024-07-18",
        n_epochs=1,
        batch_size="auto",
        learning_rate_multiplier="auto",
    ):
        # 1. Use API call to create a job
        # response = requests.post(
        #     f"{self.url}/jobs",
        #     headers={
        #         "Authorization": f"Bearer {self.api_key}"
        #     },
        #     json={
        #         "training_file": file_id,
        #         "model": model,
        #         "hyperparameters": {
        #             "n_epochs": n_epochs,
        #             "batch_size": batch_size,
        #             "learning_rate_multiplier": learning_rate_multiplier,
        #         },
        #     }
        # )
        # print("Job created successfully!")
        # return response.json()

        # 2. Use client to create a job
        result = self.client.fine_tuning.jobs.create(
            training_file=file_id,
            model=model,
            hyperparameters={
                "n_epochs": n_epochs,
                "batch_size": batch_size,
                "learning_rate_multiplier": learning_rate_multiplier,
            },
        )
        return result

    def list_jobs(self):
        response = requests.get(
            f"{self.url}/jobs", headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()

    def cancel_job(self, job_id):
        response = requests.post(
            f"{self.url}/jobs/{job_id}/cancel",
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        return response.json()
