import csv
from io import StringIO
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.responses import StreamingResponse

from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.models.ProcessingSessions import ProcessingSession
from src.models.ProductDetails import ProductDetail
from src.services.ProcessImages import ProcessImages
from src.utils.DatabaseManager import DatabaseManager

api_router = APIRouter()

db_manager = DatabaseManager()

@api_router.post("/upload")
async def upload_file(
        background_tasks: BackgroundTasks,
        file: UploadFile = File(...),
        db: Session = Depends(db_manager.get_db()),
) -> dict:
    """
    Accepts the CSV, Validate the Formatting and returns a unique request ID.

    :param background_tasks:
    :param file:
    :param db:
    :return:
    """
    content = await file.read()
    csv_data = StringIO(content.decode("utf-8"))
    reader = csv.reader(csv_data)

    next(reader)  # Skip header row

    new_processing_session = ProcessingSession()
    db.add(new_processing_session)
    db.commit()
    request_id = new_processing_session.id

    for row in reader:
        serial_number, product_name, input_urls = row
        # image_urls = input_urls.split(",")  # Handle multiple URLs

        new_product = ProductDetail(
            request_id=request_id,
            serial_number=serial_number,
            product_name=product_name,
            input_urls=input_urls
        )
        db.add(new_product)
    db.commit()

    background_tasks.add_task(ProcessImages.process_images, request_id, reader)

    return {"request_id": request_id, "message": "File is being processed"}


@api_router.get("/status/{request_id}")
def get_status(
        request_id: str,
        db: Session = Depends(db_manager.get_db()),
):
    """
    Allows users to query processing status with the request ID.

    :param request_id:
    :param db:
    :return:
    """
    current_session = db.query(ProcessingSession).filter(ProcessingSession.id == request_id).first()
    if not current_session:
        raise HTTPException(status_code=404, detail="Session not found")

    related_products = current_session.products

    for product in related_products:
        if not product.input_urls.count(",") == product.output_urls.count(","):
            return {"status": current_session.status}

    current_session.status = "completed"
    db.commit()

    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["S. No.", "Product Name", "Input Image Urls", "Output Image Urls"])  # Header

    for product in related_products:
        writer.writerow([product.serial_number, product.product_name, product.input_urls, product.output_urls])

    # Move cursor to beginning of file
    output.seek(0)

    # Return response as a CSV file
    return StreamingResponse(output, media_type="text/csv",
                             headers={"Content-Disposition": f"attachment; filename={request_id}_results.csv"})


@api_router.post("/webhook/")
async def webhook_handler(payload: dict, db: Session = Depends(db_manager.get_db())):
    """Webhook receives compressed image URLs and updates DB"""
    try:
        public_id = payload.get("public_id")
        output_url = payload.get("secure_url")

        if not public_id or not output_url:
            raise HTTPException(status_code=400, detail="Invalid payload")

        # Extract request_id and product_name from public_id
        parts = public_id.split("_")
        request_id = parts[0]
        product_name = parts[1]

        # Update output URLs for the product
        product_record = db.query(ProductDetail).filter(
            ProductDetail.request_id == request_id,
            ProductDetail.product_name == product_name,
        ).first()

        if product_record.output_urls:
            product_record.output_urls += f",{output_url}"
        else:
            product_record.output_urls = output_url
        db.commit()

        return {"message": "Product images updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
