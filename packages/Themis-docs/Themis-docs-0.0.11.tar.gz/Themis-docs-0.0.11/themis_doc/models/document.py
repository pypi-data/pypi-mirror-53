"""Document represents rendered instance of template."""
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative.base import declared_attr
from sqlalchemy.orm import relationship
import pdfkit


class Document:
    id = Column(Integer, primary_key=True)
    document_text = Column(Text, nullable=False)
    variables = Column(JSONB)

    @declared_attr
    def template_id(self):
        return Column(Integer, ForeignKey("template.id", ondelete="CASCADE"))

    @declared_attr
    def template(self):
        return relationship('Template', back_populates="documents")

    def render_to_pdf(self):
        return pdfkit.from_string(self.document_text, False)

    def store_as_pdf(self):
        raise NotImplemented()
