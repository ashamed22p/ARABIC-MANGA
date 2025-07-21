# Image Text Translation API

## Overview

This is a comprehensive FastAPI-based service that extracts text from images, translates it to Arabic, and re-renders the translated text back onto the images. The application supports multiple input formats including single images, PDFs, and various archive formats (ZIP, RAR, CBZ, CBR). It uses advanced OCR technology for text extraction, Google Translate for translation, and sophisticated Arabic text rendering with proper RTL support.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular microservices architecture with clear separation of concerns:

### Core Architecture Components

1. **API Layer** (FastAPI)
   - RESTful endpoints for file upload and processing
   - CORS-enabled for cross-origin requests
   - Built-in documentation with OpenAPI/Swagger
   - Async request handling for better performance

2. **Service Layer** (Modular Services)
   - **TextExtractor**: OCR text detection using EasyOCR
   - **TextTranslator**: Arabic translation using Google Translate
   - **ImageProcessor**: Text masking and image inpainting
   - **ArabicTextRenderer**: Arabic text rendering with RTL support

3. **Utility Layer**
   - **FileHandler**: File validation, format detection, and extraction
   - **Config**: Centralized configuration management

4. **Frontend Layer**
   - Modern web interface with Bootstrap 5
   - Drag-and-drop file upload functionality
   - Real-time progress tracking and status updates

## Key Components

### 1. Text Extraction Service (`services/text_extractor.py`)
- **Primary**: EasyOCR for multi-language text detection (English and Arabic)
- **Fallback**: Graceful degradation when OCR libraries are unavailable
- **Features**: 
  - Bounding box coordinate extraction
  - Confidence threshold filtering (0.3 minimum)
  - Async processing with thread pools

### 2. Translation Service (`services/translator.py`)
- **Engine**: Google Translate via deep-translator library
- **Languages**: Auto-detection to Arabic translation
- **Features**:
  - Batch translation support
  - Error handling and fallback mechanisms
  - Async processing for better performance

### 3. Image Processing Service (`services/image_processor.py`)
- **Primary Tool**: OpenCV for image manipulation
- **Features**:
  - Text region masking using inpainting techniques
  - Bounding box expansion for better coverage
  - Professional text removal with background preservation

### 4. Arabic Text Rendering Service (`services/arabic_text_renderer.py`)
- **Text Processing**: arabic_reshaper and python-bidi for proper RTL display
- **Font Rendering**: Pillow with Arabic fonts (Amiri)
- **Features**:
  - Intelligent font sizing based on original text dimensions
  - Proper Arabic text shaping and bidirectional text handling
  - Precise positioning to match original text locations

### 5. File Handler Utility (`utils/file_handler.py`)
- **Archive Support**: ZIP, RAR, CBZ, CBR extraction
- **PDF Processing**: pdf2image for PDF-to-image conversion
- **Features**:
  - MIME type validation
  - Large file streaming (up to 200MB)
  - Temporary file management with auto-cleanup

## Data Flow

1. **File Upload**: User uploads file via web interface or API
2. **Validation**: File type, size, and format validation
3. **Extraction**: Archives and PDFs are extracted to individual images
4. **OCR Processing**: Text extraction with bounding box coordinates
5. **Translation**: Extracted text translated to Arabic
6. **Image Processing**: Original text regions masked using inpainting
7. **Text Rendering**: Arabic text rendered with proper formatting
8. **Output Generation**: Processed images packaged into ZIP file
9. **Cleanup**: Temporary files automatically removed

## External Dependencies

### Core Dependencies
- **FastAPI**: Web framework for API development
- **EasyOCR**: Optical Character Recognition
- **OpenCV**: Image processing and computer vision
- **Pillow**: Image manipulation and text rendering
- **deep-translator**: Translation service integration

### Arabic Text Support
- **arabic-reshaper**: Arabic text reshaping for proper display
- **python-bidi**: Bidirectional text algorithm for RTL support

### File Processing
- **pdf2image**: PDF to image conversion
- **rarfile**: RAR archive extraction
- **patool**: Universal archive extraction

## Deployment Strategy

### Current Setup
- **Development**: Local development server with uvicorn
- **Port Configuration**: Dynamic port assignment via environment variables
- **Static Files**: Served directly by FastAPI for development

### Production Considerations
- **Memory Management**: Streaming file processing to handle large files
- **Async Processing**: Non-blocking operations for better scalability
- **Error Handling**: Comprehensive fallback mechanisms for missing dependencies
- **Resource Cleanup**: Automatic temporary file cleanup to prevent storage bloat

### Key Architectural Decisions

1. **Async Processing**: Chosen to handle multiple concurrent requests without blocking, especially important for CPU-intensive OCR operations.

2. **Modular Service Architecture**: Each service has a single responsibility, making the system maintainable, testable, and allowing for easy feature expansion.

3. **Graceful Degradation**: Fallback mechanisms when optional dependencies (EasyOCR, OpenCV) are unavailable, ensuring the application remains functional.

4. **Streaming File Handling**: Large file processing through temporary files and streaming to prevent memory overflow with 200MB file size limit.

5. **Frontend Integration**: Modern web interface provides user-friendly access while maintaining API-first design for programmatic access.

The system is designed to be robust, scalable, and maintainable while providing professional-quality Arabic text translation and rendering capabilities.