import asyncio

from openai import OpenAI
from services.file import FileService
from services.fine_tuning import FineTuningService

client = OpenAI()

file_service = FileService()
fine_tuning_service = FineTuningService()


async def main():
    # Upload a file
    # file_uploaded_obj = await file_service.upload(
    #     os.path.abspath("server/fine_tuning/data/ivy_fine_tuning_data_v2.jsonl")
    # )

    # Create a job
    # file_upload_id = file_uploaded_obj["id"]
    fine_tuning_service.create_job("file-WHQPk689sgJr74sqJQSDtX")

    # Cancel a job
    # fine_tuning_service.cancel_job(fine_tuning_job.id)

    # Delete file
    # await file_service.delete(file_upload_id)


if __name__ == "__main__":
    asyncio.run(main())
