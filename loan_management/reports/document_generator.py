from docxtpl import DocxTemplate
from django.conf import settings
from datetime import date
import os

class DocumentGenerator:
    """Generate Word documents from templates"""

    def __init__(self, template_name):
        self.template_path = os.path.join(
            settings.MEDIA_ROOT, 'templates', 'template_name'
        )
    
    def generate(self, context, output_filename):
        """ Generate document with given context"""
        try:
            doc = DocxTemplate(self.template_path)
            doc.render(context)

            # Create output directory if it doesn't exist
            output_dir = os.path.join(settings.MEDIA_ROOT, 'generated_reports')
            os.makedirs(output_dir, exist_ok=True)

            output_path = os.path.join(output_dir, output_filename)
            doc.save(output_path)

            return output_path
        except Exception as e:
            raise Exception(f"Failed to generate document: {str(e)}")