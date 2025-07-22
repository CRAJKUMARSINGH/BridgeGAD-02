"""
Unified Bridge Drawing Engine
Generates drawing data that can be rendered to SVG, PDF, or DXF
"""

import math
import logging

class BridgeDrawingEngine:
    """Core bridge drawing calculations and geometry generation"""
    
    def __init__(self, parameters):
        self.params = parameters
        self.elements = []
        self.texts = []
        self.bounds = {'min_x': 0, 'max_x': 0, 'min_y': 0, 'max_y': 0}
        
    def generate_drawing_data(self):
        """Generate complete drawing data with all elements"""
        self.elements.clear()
        self.texts.clear()
        
        # Get key parameters
        lbridge = float(self.params.get('LBRIDGE', 30000))
        toprl = float(self.params.get('TOPRL', 110000))
        sofl = float(self.params.get('SOFL', 108000))
        left = float(self.params.get('LEFT', 0))
        abtlen = float(self.params.get('ABTLEN', 10000))
        alfl = float(self.params.get('ALFL', 105000))
        arfl = float(self.params.get('ARFL', 105000))
        nspan = int(self.params.get('NSPAN', 1))
        
        # Calculate bounds
        self.bounds = {
            'min_x': left,
            'max_x': left + lbridge,
            'min_y': min(alfl, arfl) - 1000,
            'max_y': toprl + 5000
        }
        
        # Draw main bridge deck
        self.add_line(left, toprl, left + lbridge, toprl, 'deck', 2)
        self.add_line(left, sofl, left + lbridge, sofl, 'soffit', 2)
        
        # Draw left abutment
        self.draw_abutment('left', left, abtlen, toprl, sofl, alfl)
        
        # Draw right abutment  
        self.draw_abutment('right', left + lbridge - abtlen, abtlen, toprl, sofl, arfl)
        
        # Draw piers if multi-span
        if nspan > 1:
            self.draw_piers(left, lbridge, nspan)
            
        # Add labels and dimensions
        self.add_labels_and_dimensions()
        
        return {
            'elements': self.elements,
            'texts': self.texts,
            'bounds': self.bounds,
            'parameters': self.params
        }
    
    def add_line(self, x1, y1, x2, y2, layer='default', width=1):
        """Add a line element"""
        self.elements.append({
            'type': 'line',
            'x1': x1, 'y1': y1,
            'x2': x2, 'y2': y2,
            'layer': layer,
            'width': width
        })
    
    def add_text(self, x, y, text, size=400, layer='text'):
        """Add a text element"""
        self.texts.append({
            'x': x, 'y': y,
            'text': str(text),
            'size': size,
            'layer': layer
        })
    
    def draw_abutment(self, side, x_start, width, top_level, soffit_level, footing_level):
        """Draw abutment structure"""
        if side == 'left':
            # Left abutment - front face on left
            self.add_line(x_start, footing_level, x_start + width, footing_level, 'abutment', 1)  # Bottom
            self.add_line(x_start + width, footing_level, x_start + width, top_level, 'abutment', 1)  # Back wall
            self.add_line(x_start + width, top_level, x_start, top_level, 'abutment', 1)  # Top
            self.add_line(x_start, top_level, x_start, soffit_level, 'abutment', 1)  # Front upper
            self.add_line(x_start, soffit_level, x_start, footing_level, 'abutment', 1)  # Front lower
        else:
            # Right abutment - front face on right
            self.add_line(x_start, footing_level, x_start + width, footing_level, 'abutment', 1)  # Bottom
            self.add_line(x_start, footing_level, x_start, top_level, 'abutment', 1)  # Back wall
            self.add_line(x_start, top_level, x_start + width, top_level, 'abutment', 1)  # Top
            self.add_line(x_start + width, top_level, x_start + width, soffit_level, 'abutment', 1)  # Front upper
            self.add_line(x_start + width, soffit_level, x_start + width, footing_level, 'abutment', 1)  # Front lower
    
    def draw_piers(self, left, lbridge, nspan):
        """Draw bridge piers"""
        span_length = lbridge / nspan
        capt = float(self.params.get('CAPT', 109000))
        capb = float(self.params.get('CAPB', 108000))
        futrl = float(self.params.get('FUTRL', 105000))
        piertw = float(self.params.get('PIERTW', 2000))
        
        for i in range(1, nspan):
            pier_center = left + (i * span_length)
            pier_left = pier_center - piertw / 2
            pier_right = pier_center + piertw / 2
            
            # Pier outline
            self.add_line(pier_left, futrl, pier_right, futrl, 'pier', 1)  # Foundation
            self.add_line(pier_right, futrl, pier_right, capt, 'pier', 1)  # Right side
            self.add_line(pier_right, capt, pier_left, capt, 'pier', 1)  # Top
            self.add_line(pier_left, capt, pier_left, futrl, 'pier', 1)  # Left side
            self.add_line(pier_left, capb, pier_right, capb, 'pier', 1)  # Cap division
    
    def add_labels_and_dimensions(self):
        """Add text labels and dimensions"""
        lbridge = float(self.params.get('LBRIDGE', 30000))
        toprl = float(self.params.get('TOPRL', 110000))
        sofl = float(self.params.get('SOFL', 108000))
        left = float(self.params.get('LEFT', 0))
        nspan = int(self.params.get('NSPAN', 1))
        scale1 = int(self.params.get('SCALE1', 100))
        
        # Title
        title_x = left + lbridge / 2
        title_y = toprl + 3000
        self.add_text(title_x, title_y, "SLAB BRIDGE ELEVATION", 800)
        
        # Scale
        scale_x = left + 1000
        scale_y = toprl + 1500
        self.add_text(scale_x, scale_y, f"SCALE 1:{scale1}", 400)
        
        # Span labels
        if nspan > 0:
            span_length = lbridge / nspan
            for i in range(nspan):
                span_center_x = left + (i + 0.5) * span_length
                span_y = sofl - 2000
                span_text = f"SPAN {i+1} = {span_length/1000:.1f}M"
                self.add_text(span_center_x, span_y, span_text, 300)

class BridgeRenderer:
    """Renders bridge drawing data to different output formats"""
    
    def __init__(self, drawing_data):
        self.data = drawing_data
        self.elements = drawing_data['elements']
        self.texts = drawing_data['texts']
        self.bounds = drawing_data['bounds']
    
    def render_to_svg(self, width=800, height=400):
        """Render drawing to SVG format"""
        # Calculate scale
        drawing_width = self.bounds['max_x'] - self.bounds['min_x']
        drawing_height = self.bounds['max_y'] - self.bounds['min_y']
        
        margin = 40
        available_width = width - 2 * margin
        available_height = height - 2 * margin
        
        scale_x = available_width / drawing_width if drawing_width > 0 else 1
        scale_y = available_height / drawing_height if drawing_height > 0 else 1
        scale = min(scale_x, scale_y) / 1000  # Convert mm to display units
        
        # Center the drawing
        scaled_width = drawing_width * scale
        scaled_height = drawing_height * scale
        offset_x = margin + (available_width - scaled_width) / 2
        offset_y = margin + (available_height - scaled_height) / 2
        
        def transform_x(x):
            return offset_x + (x - self.bounds['min_x']) * scale
        
        def transform_y(y):
            return height - (offset_y + (y - self.bounds['min_y']) * scale)
        
        svg_elements = []
        
        # Render lines
        for elem in self.elements:
            if elem['type'] == 'line':
                x1 = transform_x(elem['x1'])
                y1 = transform_y(elem['y1'])
                x2 = transform_x(elem['x2'])
                y2 = transform_y(elem['y2'])
                width = elem['width']
                
                svg_elements.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="{width}"/>')
        
        # Render text
        for text in self.texts:
            x = transform_x(text['x'])
            y = transform_y(text['y'])
            size = max(8, text['size'] * scale / 50)  # Scale text size
            
            svg_elements.append(f'<text x="{x}" y="{y}" font-family="Arial" font-size="{size}" text-anchor="middle">{text["text"]}</text>')
        
        svg_content = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="white"/>
            {"".join(svg_elements)}
        </svg>'''
        
        return svg_content
    
    def render_to_pdf_data(self):
        """Prepare data for PDF rendering with proper coordinates"""
        return {
            'elements': self.elements,
            'texts': self.texts,
            'bounds': self.bounds,
            'drawing_width': self.bounds['max_x'] - self.bounds['min_x'],
            'drawing_height': self.bounds['max_y'] - self.bounds['min_y']
        }