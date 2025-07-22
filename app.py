import os
import logging
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
import tempfile
import json
from bridge_generator import BridgeCADGenerator
from drawing_engine import BridgeDrawingEngine, BridgeRenderer
from parameter_definitions import PARAMETER_DEFINITIONS, PARAMETER_GROUPS
from utils.validators import validate_parameters

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-for-bridge-cad")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def index():
    """Main page with parameter input form"""
    return render_template('index.html', 
                         parameter_groups=PARAMETER_GROUPS,
                         parameter_definitions=PARAMETER_DEFINITIONS)

@app.route('/generate', methods=['POST'])
def generate_bridge():
    """Generate bridge CAD drawing from parameters"""
    try:
        # Get parameters from form
        parameters = {}
        for key in request.form:
            if key in PARAMETER_DEFINITIONS:
                param_def = PARAMETER_DEFINITIONS[key]
                value = request.form[key]
                try:
                    # Convert to appropriate type based on parameter definition
                    if param_def['type'] == 'float':
                        parameters[key] = float(value)
                    elif param_def['type'] == 'int':
                        parameters[key] = int(value)
                    else:
                        parameters[key] = value
                        
                except (ValueError, TypeError) as e:
                    flash(f"Invalid value for {param_def['name']}: {value}", 'error')
                    return redirect(url_for('index'))
        
        # Validate parameters
        validation_errors = validate_parameters(parameters)
        if validation_errors:
            for error in validation_errors:
                flash(error, 'error')
            return redirect(url_for('index'))
        
        # Get file format from form
        file_format = request.form.get('file_format', 'dxf')
        
        # Generate the bridge CAD
        generator = BridgeCADGenerator(parameters)
        
        if file_format == 'pdf':
            # Generate PDF
            pdf_data = generator.generate_pdf()
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            temp_file.write(pdf_data)
            temp_file.close()
            
            flash('Bridge PDF generated successfully!', 'success')
            return send_file(temp_file.name, 
                            as_attachment=True, 
                            download_name='bridge_drawing.pdf',
                            mimetype='application/pdf')
        else:
            # Generate DXF
            dxf_data = generator.generate_dxf()
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.dxf')
            temp_file.write(dxf_data)
            temp_file.close()
            
            flash('Bridge DXF generated successfully!', 'success')
            return send_file(temp_file.name, 
                            as_attachment=True, 
                            download_name='bridge_drawing.dxf',
                            mimetype='application/dxf')
                        
    except Exception as e:
        app.logger.error(f"Error generating bridge: {str(e)}")
        flash(f"Error generating bridge: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/generate-dxf', methods=['POST'])
def generate_dxf():
    """Generate DXF file specifically"""
    request.form = request.form.copy()
    request.form['file_format'] = 'dxf'
    return generate_bridge()

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    """Generate PDF file specifically"""
    request.form = request.form.copy()
    request.form['file_format'] = 'pdf'
    return generate_bridge()

@app.route('/preview', methods=['POST'])
def preview_bridge():
    """Show bridge preview before generating files"""
    try:
        app.logger.info(f"Preview request received with data: {dict(request.form)}")
        
        # Get parameters from form - include ALL form data, not just defined parameters
        parameters = {}
        for key, value in request.form.items():
            if key in PARAMETER_DEFINITIONS:
                param_def = PARAMETER_DEFINITIONS[key]
                try:
                    if param_def['type'] == 'float':
                        parameters[key] = float(value) if value else 0.0
                    elif param_def['type'] == 'int':
                        parameters[key] = int(float(value)) if value else 0
                    else:
                        parameters[key] = value
                except (ValueError, TypeError) as e:
                    app.logger.warning(f"Invalid value for {key}: {value}, using default")
                    # Use default values for invalid inputs
                    if param_def['type'] == 'float':
                        parameters[key] = param_def.get('default', 0.0)
                    elif param_def['type'] == 'int':
                        parameters[key] = param_def.get('default', 0)
                    else:
                        parameters[key] = param_def.get('default', '')
            
        # Add default values for missing required parameters
        defaults = {
            'LBRIDGE': 30000.0,
            'NSPAN': 1,
            'TOPRL': 110000.0,
            'SOFL': 108000.0,
            'LEFT': 0.0,
            'ABTLEN': 10000.0,
            'ALFL': 105000.0,
            'ARFL': 105000.0,
            'SCALE1': 100,
            'SCALE2': 1,
            'CCBR': 50.0
        }
        
        for key, default_value in defaults.items():
            if key not in parameters:
                parameters[key] = default_value
                
        app.logger.info(f"Final parameters for preview: {parameters}")
        
        # Skip validation for preview - just show the drawing
        # Generate drawing data
        engine = BridgeDrawingEngine(parameters)
        drawing_data = engine.generate_drawing_data()
        
        app.logger.info(f"Drawing data generated: {len(drawing_data['elements'])} elements, {len(drawing_data['texts'])} texts")
        
        # Convert to JSON for JavaScript
        bridge_data_json = json.dumps(parameters)
        
        return render_template('preview.html', 
                             parameters=parameters,
                             bridge_data=bridge_data_json)
                             
    except Exception as e:
        app.logger.error(f"Error in preview: {str(e)}", exc_info=True)
        flash(f"Error generating preview: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/validate-parameters', methods=['POST'])
def validate_parameters_ajax():
    """AJAX endpoint for real-time parameter validation"""
    try:
        parameters = request.get_json()
        
        # Convert string values to appropriate types
        for key, value in parameters.items():
            if key in PARAMETER_DEFINITIONS and value != '':
                param_def = PARAMETER_DEFINITIONS[key]
                try:
                    if param_def['type'] == 'float':
                        parameters[key] = float(value)
                    elif param_def['type'] == 'int':
                        parameters[key] = int(value)
                except (ValueError, TypeError):
                    return jsonify({'valid': False, 'errors': [f"Invalid value for {param_def['name']}"]})
        
        errors = validate_parameters(parameters)
        return jsonify({'valid': len(errors) == 0, 'errors': errors})
        
    except Exception as e:
        return jsonify({'valid': False, 'errors': [str(e)]})

@app.route('/parameter-info/<parameter_key>')
def get_parameter_info(parameter_key):
    """Get detailed information about a parameter"""
    if parameter_key in PARAMETER_DEFINITIONS:
        return jsonify(PARAMETER_DEFINITIONS[parameter_key])
    return jsonify({'error': 'Parameter not found'}), 404

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
