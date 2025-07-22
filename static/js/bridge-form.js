// Bridge CAD Generator JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Bridge CAD Generator initialized');
    
    // Form validation
    const form = document.querySelector('form');
    const validateBtn = document.getElementById('validateBtn');
    const resetBtn = document.getElementById('resetBtn');
    const generateDxfBtn = document.getElementById('generateDxfBtn');
    const generatePdfBtn = document.getElementById('generatePdfBtn');
    
    // Validation function
    if (validateBtn) {
        validateBtn.addEventListener('click', function() {
            // Simple client-side validation
            const requiredFields = form.querySelectorAll('input[required]');
            let isValid = true;
            let errors = [];
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    errors.push(`${field.name} is required`);
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            // Show validation results
            const resultsDiv = document.getElementById('validationResults');
            const contentDiv = document.getElementById('validationContent');
            
            if (resultsDiv && contentDiv) {
                if (isValid) {
                    contentDiv.innerHTML = '<div class="alert alert-success"><i class="fas fa-check-circle me-2"></i>All parameters are valid!</div>';
                } else {
                    contentDiv.innerHTML = '<div class="alert alert-danger"><i class="fas fa-exclamation-triangle me-2"></i>Please fix the following errors:<ul class="mb-0 mt-2">' + 
                        errors.map(error => `<li>${error}</li>`).join('') + '</ul></div>';
                }
                resultsDiv.style.display = 'block';
            }
        });
    }
    
    // Reset function
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            if (confirm('Reset all parameters to default values?')) {
                form.reset();
                
                // Clear validation classes
                const invalidFields = form.querySelectorAll('.is-invalid');
                invalidFields.forEach(field => field.classList.remove('is-invalid'));
                
                // Hide validation results
                const resultsDiv = document.getElementById('validationResults');
                if (resultsDiv) {
                    resultsDiv.style.display = 'none';
                }
            }
        });
    }
    
    // Disable buttons during submission
    if (generateDxfBtn) {
        generateDxfBtn.addEventListener('click', function() {
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating DXF...';
        });
    }
    
    if (generatePdfBtn) {
        generatePdfBtn.addEventListener('click', function() {
            this.disabled = true;
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Generating PDF...';
        });
    }
});