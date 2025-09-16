# utils/validators.py
"""
Parameter validation functions for Bridge CAD Generator
"""

from parameter_definitions import PARAMETER_DEFINITIONS

def validate_parameters(parameters):
    """Validate bridge parameters and return list of errors"""
    errors = []
    
    # Check required parameters
    required_params = ['SCALE1', 'SCALE2', 'LBRIDGE', 'NSPAN', 'TOPRL', 'SOFL']
    for param in required_params:
        if param not in parameters or parameters[param] is None:
            param_info = PARAMETER_DEFINITIONS.get(param, {})
            errors.append(f"{param_info.get('name', param)} is required")
    
    # Validate parameter ranges
    for key, value in parameters.items():
        if key in PARAMETER_DEFINITIONS:
            param_def = PARAMETER_DEFINITIONS[key]
            
            try:
                # Convert to appropriate type
                if param_def['type'] == 'float':
                    num_value = float(value)
                elif param_def['type'] == 'int':
                    num_value = int(value)
                else:
                    continue
                    
                # Check min/max bounds
                if 'min' in param_def and num_value < param_def['min']:
                    errors.append(f"{param_def['name']} must be at least {param_def['min']}")
                    
                if 'max' in param_def and num_value > param_def['max']:
                    errors.append(f"{param_def['name']} must be at most {param_def['max']}")
                    
            except (ValueError, TypeError):
                errors.append(f"Invalid value for {param_def['name']}")
    
    # Logical validations
    try:
        if 'TOPRL' in parameters and 'SOFL' in parameters:
            toprl = float(parameters['TOPRL'])
            sofl = float(parameters['SOFL'])
            if toprl <= sofl:
                errors.append("Top RL must be greater than Soffit Level")
        
        if 'SCALE2' in parameters:
            scale2 = float(parameters['SCALE2'])
            if scale2 == 0:
                errors.append("Scale2 cannot be zero")
        
        # Slab thickness validation
        if all(k in parameters for k in ['SLBTHC', 'SLBTHE', 'SLBTHT']):
            center = float(parameters['SLBTHC'])
            edge = float(parameters['SLBTHE'])
            tip = float(parameters['SLBTHT'])
            
            if center <= edge:
                errors.append("Slab thickness at center should be greater than at edge")
            if edge <= tip:
                errors.append("Slab thickness at edge should be greater than at tip")
                
    except (ValueError, TypeError, KeyError):
        pass  # Skip validation if conversion fails
    
    return errors

def validate_single_parameter(key, value):
    """Validate a single parameter"""
    if key not in PARAMETER_DEFINITIONS:
        return ["Unknown parameter"]
    
    param_def = PARAMETER_DEFINITIONS[key]
    errors = []
    
    try:
        if param_def['type'] == 'float':
            num_value = float(value)
        elif param_def['type'] == 'int':
            num_value = int(value)
        else:
            return errors
            
        if 'min' in param_def and num_value < param_def['min']:
            errors.append(f"Must be at least {param_def['min']}")
            
        if 'max' in param_def and num_value > param_def['max']:
            errors.append(f"Must be at most {param_def['max']}")
            
    except (ValueError, TypeError):
        errors.append("Invalid numeric value")
    
    return errors
