from src.utils.CloudinaryService import CloudinaryService


class ProcessImages:

    @staticmethod
    async def process_images(request_id: str, products):

        for product in products:
            serial_number, product_name, input_urls = product
            image_urls = input_urls.split(",")  # Handle multiple URLs

            for image_url in image_urls:
                public_id = f"{request_id}_{product_name}"
                CloudinaryService.upload_image(image_url, public_id)
