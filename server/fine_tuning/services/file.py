import os

import aiohttp


class FileService:
    """
    File Service
    Serve OpenAI File APIs https://platform.openai.com/docs/api-reference/files
    """

    def __init__(
        self, url="https://api.openai.com/v1/files", api_key=os.getenv("OPENAI_API_KEY")
    ):
        self.url = url
        self.api_key = api_key

    async def upload(self, file_path, purpose="fine-tune"):
        """
        Upload file
        API doc: https://platform.openai.com/docs/api-reference/files/create

        Args:
            file_path (str): absolute path to file
            purpose (str, optional): intent purpose to upload file. Defaults to "fine-tune".

        Raises:
            Exception: Failed to upload file

        Returns:
            json: uploaded file object
        """
        form_data = aiohttp.FormData()
        form_data.add_field(
            "file", open(file_path, "rb"), filename=os.path.basename(file_path)
        )
        form_data.add_field("purpose", purpose)

        headers = {"Authorization": f"Bearer {self.api_key}"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url, headers=headers, data=form_data
            ) as response:
                if response.status != 200:
                    raise Exception(f"Failed to upload file: {response.json()}")

                return await response.json()

    async def retrieve(self, file_id):
        pass

    async def list(self):
        pass

    async def delete(self, file_id):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.url}/{file_id}",
                headers={"Authorization": f"Bearer {self.api_key}"},
            ) as response:
                return await response.json()

    async def retrieve_file_content(self, file_id):
        pass
