/**
 * Bridge CAD Generator - Client-side JavaScript
 * Handles form validation, user interactions, and real-time feedback
 */

class BridgeCADApp {
    constructor() {
        this.form = document.getElementById('bridgeForm');
        this.validateBtn = document.getElementById('validateBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.generateBtn = document.getElementById('generateBtn');
        this.validationResults = document.getElementById('validationResults');
        this.validationContent = document.getElementById('validationContent');
        
        this.parameterInputs = document.querySelectorAll('.parameter-input');
        this.validationErrors = {};
        this.isValidating = false;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupFormValidation();
        console.log('Bridge CAD Generator initialized');
    }
    
    setupEventListeners() {
        // Validate button click
        this.validateBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.validateParameters();
        });
        
        // Reset button click
        this.resetBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.resetToDefaults();
        });
        
        // Form submission
        this.form.addEventListener('submit', (e) => {
            this.handleFormSubmit(e);
        });
        
        // Real-time validation on input change (with debounce)
        this.parameterInputs.forEach(input => {
            let timeoutId;
            input.addEventListener('input', (e) => {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => {
                    this.validateSingleParameter(e.target);
                }, 500);
            });
            
            // Immediate validation on blur
            input.addEventListener('blur', (e) => {
                this.validateSingleParameter(e.target);
            });
        });
        
        // Prevent form submission on Enter key in input fields
        this.parameterInputs.forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.validateParameters();
                }
            });
        });
    }
    
    setupFormValidation() {
        // Enable HTML5 validation styles
        this.form.classList.add('needs-validation');
    }
    
    validateParameters() {
        if (this.isValidating) return;
        
        this.isValidating = true;
        this.setButtonLoading(this.validateBtn, true);
        
        const parameters = this.collectFormData();
        
        // Show validation results section
        this.validationResults.style.display = 'block';
        this.validationResults.classList.add('validation-slide-in');
        
        // Perform client-side validation first
        const clientErrors = this.performClientSideValidation(parameters);
        
        if (clientErrors.length > 0) {
            this.displayValidationResults(false, clientErrors);
            this.setButtonLoading(this.validateBtn, false);
            this.isValidating = false;
            return;
        }
        
        // Perform server-side validation
        fetch('/validate-parameters', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(parameters)
        })
        .then(response => response.json())
        .then(data => {
            this.displayValidationResults(data.valid, data.errors || []);
            this.updateFormValidationState(data.valid, data.errors || []);
        })
        .catch(error => {
            console.error('Validation error:', error);
            this.displayValidationResults(false, ['Server validation error. Please try again.']);
        })
        .finally(() => {
            this.setButtonLoading(this.validateBtn, false);
            this.isValidating = false;
        });
    }
    
    validateSingleParameter(input) {
        const paramKey = input.dataset.paramKey;
        const value = input.value;
        
        // Basic validation
        if (input.hasAttribute('min') && parseFloat(value) < parseFloat(input.getAttribute('min'))) {
            this.setInputValidation(input, false, `Minimum value is ${input.getAttribute('min')}`);
            return;
        }
        
        if (input.hasAttribute('max') && parseFloat(value) < parseFloat(input.getAttribute('max'))) {
            this.setInputValidation(input, false, `Maximum value is ${input.getAttribute('max')}`);
            return;
        }
        
        if (input.hasAttribute('required') && !value.trim()) {
            this.setInputValidation(input, false, 'This field is required');
            return;
        }
        
        // Clear validation state if valid
        this.setInputValidation(input, true);
    }
    
    performClientSideValidation(parameters) {
        const errors = [];
        
        // Required field validation
        const requiredFields = ['SCALE1', 'SCALE2', 'LBRIDGE', 'NSPAN', 'TOPRL', 'SOFL', 'CCBR'];
        requiredFields.forEach(field => {
            if (!parameters[field] || parameters[field] === '') {
                errors.push(`${field} is required`);
            }
        });
        
        // Logical validations
        if (parameters.TOPRL && parameters.SOFL) {
            if (parseFloat(parameters.TOPRL) <= parseFloat(parameters.SOFL)) {
                errors.push('Top RL must be greater than Soffit Level');
            }
        }
        
        if (parameters.SCALE2 && parseFloat(parameters.SCALE2) === 0) {
            errors.push('Scale2 cannot be zero');
        }
        
        if (parameters.SLBTHC && parameters.SLBTHE && parameters.SLBTHT) {
            const center = parseFloat(parameters.SLBTHC);
            const edge = parseFloat(parameters.SLBTHE);
            const tip = parseFloat(parameters.SLBTHT);
            
            if (center <= edge) {
                errors.push('Slab thickness at center should be greater than at edge');
            }
            if (edge <= tip) {
                errors.push('Slab thickness at edge should be greater than at tip');
            }
        }
        
        return errors;
    }
    
    displayValidationResults(isValid, errors) {
        const statusIcon = isValid ? 
            '<i class="fas fa-check-circle text-success"></i>' : 
            '<i class="fas fa-exclamation-triangle text-danger"></i>';
        
        const statusText = isValid ? 
            '<span class="text-success fw-bold">All parameters are valid</span>' : 
            '<span class="text-danger fw-bold">Validation errors found</span>';
        
        let content = `
            <div class="d-flex align-items-center mb-3">
                ${statusIcon}
                <span class="ms-2">${statusText}</span>
            </div>
        `;
        
        if (!isValid && errors.length > 0) {
            content += '<div class="alert alert-danger mb-0"><ul class="mb-0">';
            errors.forEach(error => {
                content += `<li>${error}</li>`;
            });
            content += '</ul></div>';
        } else if (isValid) {
            content += '<div class="alert alert-success mb-0">Ready to generate DXF drawing!</div>';
        }
        
        this.validationContent.innerHTML = content;
    }
    
    updateFormValidationState(isValid, errors) {
        // Update generate button state
        this.generateBtn.disabled = !isValid;
        
        if (isValid) {
            this.generateBtn.classList.remove('btn-secondary');
            this.generateBtn.classList.add('btn-light');
        } else {
            this.generateBtn.classList.remove('btn-light');
            this.generateBtn.classList.add('btn-secondary');
        }
    }
    
    setInputValidation(input, isValid, message = '') {
        const errorElement = document.getElementById(`${input.name}_error`);
        
        if (isValid) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            if (errorElement) errorElement.textContent = '';
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            if (errorElement) errorElement.textContent = message;
        }
    }
    
    collectFormData() {
        const formData = new FormData(this.form);
        const parameters = {};
        
        for (let [key, value] of formData.entries()) {
            parameters[key] = value;
        }
        
        return parameters;
    }
    
    resetToDefaults() {
        if (confirm('Are you sure you want to reset all parameters to default values?')) {
            // Reset form inputs to their default values
            this.parameterInputs.forEach(input => {
                const defaultValue = input.getAttribute('value');
                if (defaultValue !== null) {
                    input.value = defaultValue;
                }
                
                // Clear validation classes
                input.classList.remove('is-valid', 'is-invalid');
            });
            
            // Hide validation results
            this.validationResults.style.display = 'none';
            
            // Reset generate button state
            this.generateBtn.disabled = false;
            this.generateBtn.classList.remove('btn-secondary');
            this.generateBtn.classList.add('btn-light');
            
            // Show success message
            this.showToast('Parameters reset to defaults', 'success');
        }
    }
    
    handleFormSubmit(e) {
        // Perform final validation before submission
        const parameters = this.collectFormData();
        const errors = this.performClientSideValidation(parameters);
        
        if (errors.length > 0) {
            e.preventDefault();
            this.displayValidationResults(false, errors);
            this.validationResults.style.display = 'block';
            this.showToast('Please fix validation errors before generating', 'error');
            return;
        }
        
        // Show loading state
        this.setButtonLoading(this.generateBtn, true, 'Generating DXF...');
        
        // Let the form submit naturally
        // Loading state will be cleared when page reloads or on error
    }
    
    setButtonLoading(button, isLoading, text = null) {
        if (isLoading) {
            button.disabled = true;
            const originalText = button.innerHTML;
            button.dataset.originalText = originalText;
            button.innerHTML = `
                <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                ${text || 'Processing...'}
            `;
        } else {
            button.disabled = false;
            const originalText = button.dataset.originalText;
            if (originalText) {
                button.innerHTML = originalText;
            }
        }
    }
    
    showToast(message, type = 'info') {
        // Create a simple toast notification
        const toast = document.createElement('div');
        toast.className = `alert alert-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'info'} position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.bridgeCADApp = new BridgeCADApp();
});

// Utility functions for enhanced user experience
function copyParametersToClipboard() {
    const app = window.bridgeCADApp;
    const parameters = app.collectFormData();
    const paramString = JSON.stringify(parameters, null, 2);
    
    navigator.clipboard.writeText(paramString).then(() => {
        app.showToast('Parameters copied to clipboard', 'success');
    }).catch(err => {
        console.error('Could not copy parameters:', err);
        app.showToast('Could not copy parameters', 'error');
    });
}

function loadParametersFromClipboard() {
    navigator.clipboard.readText().then(text => {
        try {
            const parameters = JSON.parse(text);
            const app = window.bridgeCADApp;
            
            // Load parameters into form
            Object.entries(parameters).forEach(([key, value]) => {
                const input = document.getElementById(key);
                if (input) {
                    input.value = value;
                }
            });
            
            app.showToast('Parameters loaded from clipboard', 'success');
        } catch (e) {
            window.bridgeCADApp.showToast('Invalid parameter format in clipboard', 'error');
        }
    }).catch(err => {
        window.bridgeCADApp.showToast('Could not read from clipboard', 'error');
    });
}

// Export functions for potential external use
window.BridgeCADUtils = {
    copyParametersToClipboard,
    loadParametersFromClipboard
};
