"""
Configuration settings for the Image Text Translation API
"""

import os

class Config:
    """Application configuration"""
    
    # File size limits
    MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB in bytes
    MAX_BATCH_SIZE = 50  # Maximum number of files in batch processing
    
    # OCR settings
    OCR_CONFIDENCE_THRESHOLD = 0.3
    OCR_LANGUAGES = ['en', 'ar']  # English and Arabic
    
    # Translation settings
    TRANSLATION_SERVICE = "google"  # Using Google Translate via deep-translator
    
    # Image processing settings
    IMAGE_QUALITY = 95
    MAX_IMAGE_DIMENSION = 4096  # Maximum width or height
    
    # Arabic text rendering settings
    ARABIC_FONT_PATH = os.path.join("fonts", "Amiri-Regular.ttf")
    MIN_FONT_SIZE = 8
    MAX_FONT_SIZE = 200
    FONT_SIZE_PADDING = 0.1  # 10% padding around text
    
    # Supported file formats
    SUPPORTED_IMAGE_FORMATS = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff', '.gif'}
    SUPPORTED_PDF_FORMATS = {'.pdf'}
    SUPPORTED_ARCHIVE_FORMATS = {'.zip', '.rar', '.cbz', '.cbr'}
    
    # Processing settings
    USE_ASYNC_PROCESSING = True
    TEMP_DIR_PREFIX = "arabic_translator_"
    
    # API settings
    API_TITLE = "Image Text Translation API"
    API_DESCRIPTION = "Extract text from images, translate to Arabic, and re-render"
    API_VERSION = "1.0.0"
    
    # CORS settings
    CORS_ORIGINS = ["*"]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]
    
    @classmethod
    def get_supported_formats(cls):
        """Get all supported file formats"""
        return cls.SUPPORTED_IMAGE_FORMATS | cls.SUPPORTED_PDF_FORMATS | cls.SUPPORTED_ARCHIVE_FORMATS
    
    @classmethod
    def is_image_format(cls, extension):
        """Check if extension is a supported image format"""
        return extension.lower() in cls.SUPPORTED_IMAGE_FORMATS
    
    @classmethod
    def is_pdf_format(cls, extension):
        """Check if extension is PDF"""
        return extension.lower() in cls.SUPPORTED_PDF_FORMATS
    
    @classmethod
    def is_archive_format(cls, extension):
        """Check if extension is a supported archive format"""
        return extension.lower() in cls.SUPPORTED_ARCHIVE_FORMATS
