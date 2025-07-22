# Bridge CAD Generator

## Overview

This is a Flask-based web application that generates DXF (AutoCAD) drawings for slab bridge designs. The application provides a web interface for engineers to input bridge parameters and generates professional CAD drawings that can be opened in AutoCAD or compatible software.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Traditional server-side rendered Flask application using Jinja2 templates
- **UI Framework**: Bootstrap 5 with dark theme for professional engineering appearance
- **JavaScript**: Vanilla JavaScript with class-based architecture for form validation and user interactions
- **Styling**: Custom CSS with engineering-focused design patterns and monospace fonts for technical data

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Structure**: Modular design with separate modules for different concerns
- **CAD Generation**: Custom Python classes using the `ezdxf` library for DXF file creation
- **Validation**: Dedicated validation utilities for engineering parameter checking

## Key Components

### Core Application (`app.py`)
- Flask application setup with ProxyFix middleware for deployment
- Route handlers for main interface and bridge generation
- Parameter processing and type conversion logic
- Error handling with flash messages

### CAD Generation Engine (`bridge_generator.py`)
- `BridgeCADGenerator` class responsible for creating DXF drawings
- Document setup with proper CAD standards (R2010 format)
- Mathematical calculations for bridge geometry
- Layer management and drawing standards

### Parameter Management (`parameter_definitions.py`)
- Centralized parameter definitions with validation rules
- Type definitions (int, float, string) with min/max constraints
- Parameter grouping for organized UI presentation
- Engineering units and descriptions

### Validation System (`utils/validators.py`)
- Parameter validation against engineering constraints
- Type checking and range validation
- Engineering-specific validation rules
- Error message generation for user feedback

### User Interface Templates
- **Base Template**: Common layout with Bootstrap navigation and flash message handling
- **Index Template**: Parameter input form with grouped sections
- **Generate Template**: Results page with download functionality

## Data Flow

1. **Parameter Input**: Users fill out engineering parameters through grouped form sections
2. **Validation**: Client-side and server-side validation ensures parameter integrity
3. **Processing**: Parameters are converted to appropriate types and validated against engineering constraints
4. **CAD Generation**: `BridgeCADGenerator` creates DXF drawing with calculated geometry
5. **File Delivery**: Generated DXF file is served for download

## External Dependencies

### Python Libraries
- **Flask**: Web framework for application structure
- **ezdxf**: DXF file creation and manipulation library
- **Werkzeug**: WSGI utilities and ProxyFix middleware

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme
- **Font Awesome**: Icon library for professional interface
- **Custom CSS**: Engineering-focused styling

### Development Tools
- **Pandas**: Data processing (referenced in attached assets)
- **Math libraries**: Mathematical calculations for bridge geometry

## Deployment Strategy

### Configuration
- Environment-based secret key management
- Debug mode configurable via application entry point
- ProxyFix middleware for reverse proxy deployment

### File Handling
- Temporary file generation for DXF downloads
- Static file serving for CSS and JavaScript assets
- Template rendering with Jinja2

### Scaling Considerations
- Stateless design suitable for horizontal scaling
- File generation uses temporary storage
- No persistent database requirements identified

### Security
- CSRF protection through Flask's secret key mechanism
- Input validation and sanitization
- Secure file handling for generated downloads

### Engineering Standards
- DXF R2010 format compatibility
- Professional CAD drawing standards
- Engineering unit consistency and validation