"""
Flask Image Text Translation Service
Extracts text from images, translates to Arabic, and re-renders on images
"""

import os
import sys
import tempfile
import zipfile
from io import BytesIO
import asyncio
import logging
from pathlib import Path

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from services.text_extractor import TextExtractor
    OCR_AVAILABLE = True
except ImportError:
    from services.text_extractor_fallback import TextExtractorFallback as TextExtractor
    OCR_AVAILABLE = False

from services.translator import TextTranslator
from services.image_processor import ImageProcessor
from services.arabic_text_renderer import ArabicTextRenderer
from utils.file_handler import FileHandler
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")

# Initialize services
text_extractor = TextExtractor()
translator = TextTranslator()
image_processor = ImageProcessor()
arabic_renderer = ArabicTextRenderer()
file_handler = FileHandler()

@app.route('/')
def index():
    """Main page with upload interface"""
    return render_template('index.html', 
                         ocr_available=OCR_AVAILABLE,
                         max_file_size_mb=Config.MAX_FILE_SIZE // (1024 * 1024),
                         supported_formats=["PNG", "JPG", "JPEG", "WebP", "BMP", "TIFF", "GIF", "PDF", "ZIP", "RAR", "CBZ", "CBR"])

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and processing"""
    try:
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(url_for('index'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            # Save uploaded file temporarily
            filename = secure_filename(file.filename)
            temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{filename}")
            file.save(temp_input.name)
            
            try:
                # Process the file
                processed_files = process_file(temp_input.name, filename)
                
                if len(processed_files) == 1:
                    # Single file - return directly
                    return send_file(processed_files[0], as_attachment=True, 
                                   download_name=f"translated_{filename}")
                else:
                    # Multiple files - create ZIP
                    zip_buffer = BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for i, file_path in enumerate(processed_files):
                            zip_file.write(file_path, f"translated_{i+1}.png")
                    
                    zip_buffer.seek(0)
                    
                    # Clean up temporary files
                    for file_path in processed_files:
                        os.unlink(file_path)
                    
                    return send_file(zip_buffer, as_attachment=True, 
                                   download_name=f"translated_{filename.rsplit('.', 1)[0]}.zip",
                                   mimetype='application/zip')
                                   
            except Exception as e:
                logger.error(f"Error processing file: {e}")
                flash(f'Error processing file: {str(e)}')
                return redirect(url_for('index'))
            finally:
                # Clean up input file
                os.unlink(temp_input.name)
        else:
            flash('Invalid file type')
            return redirect(url_for('index'))
            
    except Exception as e:
        logger.error(f"Upload error: {e}")
        flash(f'Upload failed: {str(e)}')
        return redirect(url_for('index'))

def allowed_file(filename):
    """Check if file type is allowed"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp', 'pdf', 'zip', 'rar', 'cbz', 'cbr'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_file(file_path, filename):
    """Process uploaded file and return list of processed image paths"""
    try:
        # Extract images from file
        images = file_handler.extract_images(file_path, filename)
        processed_files = []
        
        for image_data in images:
            # Extract text from image
            text_regions = text_extractor.extract_text(image_data['data'])
            
            if not text_regions:
                # No text found, save original image
                temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
                image_data['data'].save(temp_output.name, 'PNG')
                processed_files.append(temp_output.name)
                continue
            
            # Translate extracted text
            translated_regions = []
            for region in text_regions:
                try:
                    translated_text = translator.translate(region['text'])
                    translated_regions.append({
                        'text': translated_text,
                        'bbox': region['bbox'],
                        'confidence': region.get('confidence', 1.0)
                    })
                except Exception as e:
                    logger.warning(f"Translation failed for text: {region['text']}, error: {e}")
                    # Use original text if translation fails
                    translated_regions.append(region)
            
            # Process image to remove original text
            cleaned_image = image_processor.remove_text(image_data['data'], text_regions)
            
            # Render Arabic text on cleaned image
            final_image = arabic_renderer.render_text(cleaned_image, translated_regions)
            
            # Save processed image
            temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            final_image.save(temp_output.name, 'PNG')
            processed_files.append(temp_output.name)
        
        return processed_files
        
    except Exception as e:
        logger.error(f"Error processing file {filename}: {e}")
        raise

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'ocr_available': OCR_AVAILABLE,
        'services': {
            'text_extractor': 'ready',
            'translator': 'ready', 
            'image_processor': 'ready',
            'arabic_renderer': 'ready'
        }
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)