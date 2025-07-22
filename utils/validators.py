"""
Parameter validation utilities for bridge design
"""

from parameter_definitions import PARAMETER_DEFINITIONS

def validate_parameters(parameters):
    """
    Validate bridge parameters and return list of error messages
    """
    errors = []
    
    # Check required parameters
    required_params = [
        'SCALE1', 'SCALE2', 'LBRIDGE', 'NSPAN', 'TOPRL', 'SOFL', 'CCBR'
    ]
    
    for param in required_params:
        if param not in parameters or parameters[param] == '':
            param_def = PARAMETER_DEFINITIONS.get(param, {})
            param_name = param_def.get('name', param)
            errors.append(f"{param_name} is required")
    
    # Validate individual parameters against their definitions
    for param, value in parameters.items():
        if param in PARAMETER_DEFINITIONS and value != '':
            param_def = PARAMETER_DEFINITIONS[param]
            param_name = param_def['name']
            
            try:
                # Type validation
                if param_def['type'] == 'float':
                    float_val = float(value)
                    if 'min' in param_def and float_val < param_def['min']:
                        errors.append(f"{param_name} must be at least {param_def['min']}")
                    if 'max' in param_def and float_val > param_def['max']:
                        errors.append(f"{param_name} must be at most {param_def['max']}")
                        
                elif param_def['type'] == 'int':
                    int_val = int(float(value))  # Handle float strings
                    if 'min' in param_def and int_val < param_def['min']:
                        errors.append(f"{param_name} must be at least {param_def['min']}")
                    if 'max' in param_def and int_val > param_def['max']:
                        errors.append(f"{param_name} must be at most {param_def['max']}")
                        
            except (ValueError, TypeError):
                errors.append(f"{param_name} must be a valid {param_def['type']}")
    
    # Engineering validation rules
    if 'TOPRL' in parameters and 'SOFL' in parameters:
        try:
            toprl = float(parameters['TOPRL'])
            sofl = float(parameters['SOFL'])
            if toprl <= sofl:
                errors.append("Top RL must be greater than Soffit Level")
        except (ValueError, TypeError):
            pass  # Already caught in individual validation
    
    if 'SCALE1' in parameters and 'SCALE2' in parameters:
        try:
            scale1 = float(parameters['SCALE1'])
            scale2 = float(parameters['SCALE2'])
            if scale2 == 0:
                errors.append("Scale2 cannot be zero")
        except (ValueError, TypeError):
            pass
    
    if 'NSPAN' in parameters and 'LBRIDGE' in parameters:
        try:
            nspan = int(float(parameters['NSPAN']))
            lbridge = float(parameters['LBRIDGE'])
            
            # Calculate individual span length
            if nspan > 0:
                calculated_span_length = lbridge / nspan
                
                # Check if spans are reasonable (between 5m and 50m typically)
                if calculated_span_length < 5000:  # 5m minimum
                    errors.append(f"Individual span length ({calculated_span_length/1000:.1f}m) is too short. Minimum 5m recommended.")
                elif calculated_span_length > 50000:  # 50m maximum
                    errors.append(f"Individual span length ({calculated_span_length/1000:.1f}m) is too long. Maximum 50m recommended.")
            

        except (ValueError, TypeError):
            pass
    
    if 'SLBTHC' in parameters and 'SLBTHE' in parameters and 'SLBTHT' in parameters:
        try:
            center = float(parameters['SLBTHC'])
            edge = float(parameters['SLBTHE'])
            tip = float(parameters['SLBTHT'])
            
            if center <= edge:
                errors.append("Slab thickness at center should be greater than at edge")
            if edge <= tip:
                errors.append("Slab thickness at edge should be greater than at tip")
        except (ValueError, TypeError):
            pass
    
    if 'ALFL' in parameters and 'ARFL' in parameters and 'FUTRL' in parameters:
        try:
            alfl = float(parameters['ALFL'])
            arfl = float(parameters['ARFL'])
            futrl = float(parameters['FUTRL'])
            
            if alfl < futrl:
                errors.append("Left abutment footing level should be at or above foundation level")
            if arfl < futrl:
                errors.append("Right abutment footing level should be at or above foundation level")
        except (ValueError, TypeError):
            pass
    
    return errors

def validate_parameter_combination(param1, param2, operator, message):
    """
    Helper function to validate relationships between parameters
    """
    # This can be extended for more complex validations
    pass
