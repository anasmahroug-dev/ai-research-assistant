import cloudinary
import cloudinary.uploader
import os


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)


def upload_file(file):
    result = cloudinary.uploader.upload(
        file,
        resource_type="raw",
        folder="research-pdfs",
    )
    print(result)
    return {
        "url": result["secure_url"],
        "public_id": result["public_id"],
    }
    
    
def delete_pdf_from_cloudinary(public_id: str):
    cloudinary.uploader.destroy(
        public_id,
        resource_type="raw",
    )