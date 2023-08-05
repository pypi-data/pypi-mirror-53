from themis_doc.pdf_storage import PDFStorage
from boto3 import Session
from os import environ

class S3Storage(PDFStorage):

    def __init__(self):
        session = Session()
        self.s3 = session.resource('s3')
        self.bucket_name = environ.get('THEMIS_PDF_BUCKET')

    def save_pdf(self, pdf) -> str:
        """Save and return url"""
        pdf_file_name = f"order_id_{int(time.time())}.pdf"
        result = self.s3.Object(self.bucket_name, pdf_file_name).put(Body=pdf)
        s3_client = self.session.client('s3')
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': pdf_file_name
            }
        )
        return url