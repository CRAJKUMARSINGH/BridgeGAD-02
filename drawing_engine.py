"""
Unified Bridge Drawing Engine
Generates drawing data that can be rendered to SVG, PDF, or DXF
"""

import math
import logging

class BridgeDrawingEngine:
    """Core bridge drawing calculations and geometry generation - matches original Python accuracy"""
    
    def __init__(self, parameters):
        self.params = parameters
        self.elements = []
        self.texts = []
        self.bounds = {'min_x': 0, 'max_x': 0, 'min_y': 0, 'max_y': 0}
        
        # Initialize coordinate transformation functions like original program
        self.scale1 = float(parameters.get('SCALE1', 100))
        self.scale2 = float(parameters.get('SCALE2', 1))
        self.datum = float(parameters.get('DATUM', 100000))
        self.left = float(parameters.get('LEFT', 0))
        self.skew = float(parameters.get('SKEW', 0))
        
        # Calculate scaling factors like original
        self.sc = self.scale1 / self.scale2 if self.scale2 != 0 else 1
        self.vvs = 1000.0 / 1  # vs = 1
        self.hhs = 1000.0 / 1  # hs = 1
        
        # Skew calculations
        self.skew1 = self.skew * 0.0174532  # Convert degrees to radians
        self.s = math.sin(self.skew1)
        self.c = math.cos(self.skew1)
        self.tn = self.s / self.c if self.c != 0 else 0
        
    def vpos(self, a):
        """Vertical position transformation like original"""
        return self.datum + self.vvs * (a - self.datum)
        
    def hpos(self, a):
        """Horizontal position transformation like original"""
        return self.left + self.hhs * (a - self.left)
        
    def v2pos(self, a):
        """Scaled vertical position like original"""
        return self.datum + self.sc * self.vvs * (a - self.datum)
        
    def h2pos(self, a):
        """Scaled horizontal position like original"""
        return self.left + self.sc * self.hhs * (a - self.left)
        
    def generate_drawing_data(self):
        """Generate complete drawing data with all elements - matching original accuracy"""
        self.elements.clear()
        self.texts.clear()
        
        # Get all parameters like original program
        lbridge = float(self.params.get('LBRIDGE', 30000))
        toprl = float(self.params.get('TOPRL', 110000))
        sofl = float(self.params.get('SOFL', 108000))
        left = float(self.params.get('LEFT', 0))
        right = float(self.params.get('RIGHT', 50000))
        abtlen = float(self.params.get('ABTLEN', 10000))
        alfl = float(self.params.get('ALFL', 105000))
        arfl = float(self.params.get('ARFL', 105000))
        nspan = int(self.params.get('NSPAN', 1))
        span1 = float(self.params.get('SPAN1', 30000))
        
        # Abutment parameters like original
        alcw = float(self.params.get('ALCW', 1200))  # Abutment Left Cap Width
        alcd = float(self.params.get('ALCD', 800))   # Abutment Left Cap Depth
        dwth = float(self.params.get('DWTH', 300))   # Dirt wall thickness
        alfb = float(self.params.get('ALFB', 0.1))   # Front batter
        altb = float(self.params.get('ALTB', 0.1))   # Toe batter
        albb = float(self.params.get('ALBB', 0.05))  # Back batter
        alfo = float(self.params.get('ALFO', 500))   # Front offset
        alfd = float(self.params.get('ALFD', 1000))  # Footing depth
        
        # Pier parameters
        capt = float(self.params.get('CAPT', 109000))
        capb = float(self.params.get('CAPB', 108000))
        piertw = float(self.params.get('PIERTW', 1500))
        futrl = float(self.params.get('FUTRL', 100000))
        futd = float(self.params.get('FUTD', 2000))
        futw = float(self.params.get('FUTW', 3000))
        futl = float(self.params.get('FUTL', 8000))
        
        # Approach slab
        laslab = float(self.params.get('LASLAB', 5000))
        apwth = float(self.params.get('APWTH', 8000))
        apthk = float(self.params.get('APTHK', 200))
        
        # Calculate precise bounds like original program
        min_x = left - laslab - 2000
        max_x = left + lbridge + laslab + 2000
        min_y = min(alfl, arfl, futrl) - futd - 2000
        max_y = toprl + 3000
        
        self.bounds = {
            'min_x': min_x,
            'max_x': max_x,
            'min_y': min_y,
            'max_y': max_y
        }
        
        # Draw bridge elements with precise coordinates
        self.draw_bridge_elevation()
        self.draw_abutments_detailed()
        if nspan > 1:
            self.draw_piers_detailed()
        self.draw_approach_slabs()
        self.add_professional_annotations()
        
        return {
            'elements': self.elements,
            'texts': self.texts,
            'bounds': self.bounds,
            'parameters': self.params
        }
        
    def draw_bridge_elevation(self):
        """Draw main bridge elevation like original program"""
        lbridge = float(self.params.get('LBRIDGE', 30000))
        toprl = float(self.params.get('TOPRL', 110000))
        sofl = float(self.params.get('SOFL', 108000))
        left = float(self.params.get('LEFT', 0))
        slbthc = float(self.params.get('SLBTHC', 1000))  # Slab thickness center
        slbthe = float(self.params.get('SLBTHE', 800))   # Slab thickness edge
        
        # Main bridge deck (top line) - thick line
        self.add_line(left, toprl, left + lbridge, toprl, 'deck', 3)
        
        # Bridge soffit (bottom line) 
        self.add_line(left, sofl, left + lbridge, sofl, 'soffit', 2)
        
        # Slab edge details - tapered thickness
        slab_mid = left + lbridge / 2
        slab_edge_left = toprl - slbthe
        slab_edge_right = toprl - slbthe
        slab_center = toprl - slbthc
        
        # Draw slab thickness profile
        self.add_line(left, slab_edge_left, slab_mid, slab_center, 'slab_profile', 1)
        self.add_line(slab_mid, slab_center, left + lbridge, slab_edge_right, 'slab_profile', 1)
        
        # End connections
        self.add_line(left, toprl, left, sofl, 'end_connection', 2)
        self.add_line(left + lbridge, toprl, left + lbridge, sofl, 'end_connection', 2)
        
    def draw_abutments_detailed(self):
        """Draw detailed abutments like original program"""
        left = float(self.params.get('LEFT', 0))
        lbridge = float(self.params.get('LBRIDGE', 30000))
        toprl = float(self.params.get('TOPRL', 110000))
        sofl = float(self.params.get('SOFL', 108000))
        abtlen = float(self.params.get('ABTLEN', 10000))
        alcw = float(self.params.get('ALCW', 1200))
        alcd = float(self.params.get('ALCD', 800))
        alfl = float(self.params.get('ALFL', 105000))
        arfl = float(self.params.get('ARFL', 105000))
        alfo = float(self.params.get('ALFO', 500))
        alfd = float(self.params.get('ALFD', 1000))
        dwth = float(self.params.get('DWTH', 300))
        
        # Left abutment detailed structure
        # Cap structure
        self.add_line(left, toprl, left + alcw, toprl, 'abutment_cap', 2)
        self.add_line(left + alcw, toprl, left + alcw, toprl - alcd, 'abutment_cap', 2)
        self.add_line(left + alcw, toprl - alcd, left, toprl - alcd, 'abutment_cap', 2)
        
        # Abutment wall
        self.add_line(left, toprl - alcd, left, sofl, 'abutment_wall', 2)
        self.add_line(left, sofl, left + abtlen, sofl, 'abutment_wall', 2)
        self.add_line(left + abtlen, sofl, left + abtlen, toprl - alcd, 'abutment_wall', 2)
        
        # Footing
        footing_top = alfl + alfd
        self.add_line(left - alfo, alfl, left + abtlen + alfo, alfl, 'footing', 2)
        self.add_line(left - alfo, alfl, left - alfo, footing_top, 'footing', 1)
        self.add_line(left + abtlen + alfo, alfl, left + abtlen + alfo, footing_top, 'footing', 1)
        self.add_line(left - alfo, footing_top, left + abtlen + alfo, footing_top, 'footing', 1)
        
        # Dirt wall
        self.add_line(left + abtlen, toprl - alcd, left + abtlen, sofl + dwth, 'dirt_wall', 1)
        self.add_line(left + abtlen, sofl + dwth, left + abtlen + dwth, sofl + dwth, 'dirt_wall', 1)
        self.add_line(left + abtlen + dwth, sofl + dwth, left + abtlen + dwth, toprl - alcd, 'dirt_wall', 1)
        
        # Right abutment (mirror image)
        right_start = left + lbridge
        # Cap structure
        self.add_line(right_start - alcw, toprl, right_start, toprl, 'abutment_cap', 2)
        self.add_line(right_start - alcw, toprl, right_start - alcw, toprl - alcd, 'abutment_cap', 2)
        self.add_line(right_start - alcw, toprl - alcd, right_start, toprl - alcd, 'abutment_cap', 2)
        
        # Abutment wall
        self.add_line(right_start, toprl - alcd, right_start, sofl, 'abutment_wall', 2)
        self.add_line(right_start, sofl, right_start - abtlen, sofl, 'abutment_wall', 2)
        self.add_line(right_start - abtlen, sofl, right_start - abtlen, toprl - alcd, 'abutment_wall', 2)
        
        # Right footing
        footing_top_r = arfl + alfd
        self.add_line(right_start + alfo, arfl, right_start - abtlen - alfo, arfl, 'footing', 2)
        self.add_line(right_start + alfo, arfl, right_start + alfo, footing_top_r, 'footing', 1)
        self.add_line(right_start - abtlen - alfo, arfl, right_start - abtlen - alfo, footing_top_r, 'footing', 1)
        self.add_line(right_start + alfo, footing_top_r, right_start - abtlen - alfo, footing_top_r, 'footing', 1)
        
    def draw_piers_detailed(self):
        """Draw detailed piers matching original program"""
        left = float(self.params.get('LEFT', 0))
        lbridge = float(self.params.get('LBRIDGE', 30000))
        nspan = int(self.params.get('NSPAN', 1))
        span1 = float(self.params.get('SPAN1', 30000))
        capt = float(self.params.get('CAPT', 109000))
        capb = float(self.params.get('CAPB', 108000))
        piertw = float(self.params.get('PIERTW', 1500))
        futrl = float(self.params.get('FUTRL', 100000))
        futd = float(self.params.get('FUTD', 2000))
        futw = float(self.params.get('FUTW', 3000))
        futl = float(self.params.get('FUTL', 8000))
        battr = float(self.params.get('BATTR', 0.02))  # Pier batter
        
        if nspan <= 1:
            return
            
        # Calculate pier positions
        for pier_num in range(1, nspan):
            # Pier centerline position
            pier_center_x = left + (pier_num * span1)
            
            # Pier cap dimensions
            cap_half_width = piertw / 2
            pier_left = pier_center_x - cap_half_width
            pier_right = pier_center_x + cap_half_width
            
            # Draw pier cap
            self.add_line(pier_left, capt, pier_right, capt, 'pier_cap', 2)
            self.add_line(pier_left, capt, pier_left, capb, 'pier_cap', 2)
            self.add_line(pier_right, capt, pier_right, capb, 'pier_cap', 2)
            self.add_line(pier_left, capb, pier_right, capb, 'pier_cap', 2)
            
            # Pier shaft with batter
            shaft_height = capb - futrl - futd
            batter_offset = shaft_height * battr
            
            # Shaft outline with batter
            shaft_left_top = pier_left
            shaft_right_top = pier_right
            shaft_left_bottom = pier_left - batter_offset
            shaft_right_bottom = pier_right + batter_offset
            
            self.add_line(shaft_left_top, capb, shaft_left_bottom, futrl + futd, 'pier_shaft', 2)
            self.add_line(shaft_right_top, capb, shaft_right_bottom, futrl + futd, 'pier_shaft', 2)
            
            # Pier footing
            footing_left = pier_center_x - futw / 2
            footing_right = pier_center_x + futw / 2
            
            self.add_line(footing_left, futrl + futd, footing_right, futrl + futd, 'pier_footing', 2)
            self.add_line(footing_left, futrl + futd, footing_left, futrl, 'pier_footing', 2)
            self.add_line(footing_right, futrl + futd, footing_right, futrl, 'pier_footing', 2)
            self.add_line(footing_left, futrl, footing_right, futrl, 'pier_footing', 2)
            
            # Connect shaft to footing
            self.add_line(shaft_left_bottom, futrl + futd, footing_left, futrl + futd, 'pier_connection', 1)
            self.add_line(shaft_right_bottom, futrl + futd, footing_right, futrl + futd, 'pier_connection', 1)
            
    def draw_approach_slabs(self):
        """Draw approach slabs like original program"""
        left = float(self.params.get('LEFT', 0))
        lbridge = float(self.params.get('LBRIDGE', 30000))
        toprl = float(self.params.get('TOPRL', 110000))
        laslab = float(self.params.get('LASLAB', 5000))
        apwth = float(self.params.get('APWTH', 8000))
        apthk = float(self.params.get('APTHK', 200))
        rtl = float(self.params.get('RTL', 110000))  # Road top level
        
        # Left approach slab
        left_slab_start = left - laslab
        left_slab_end = left
        approach_top = toprl
        approach_bottom = toprl - apthk
        
        # Left approach slab outline
        self.add_line(left_slab_start, approach_top, left_slab_end, approach_top, 'approach_slab', 2)
        self.add_line(left_slab_start, approach_top, left_slab_start, approach_bottom, 'approach_slab', 1)
        self.add_line(left_slab_end, approach_top, left_slab_end, approach_bottom, 'approach_slab', 1)
        self.add_line(left_slab_start, approach_bottom, left_slab_end, approach_bottom, 'approach_slab', 2)
        
        # Right approach slab
        right_slab_start = left + lbridge
        right_slab_end = left + lbridge + laslab
        
        # Right approach slab outline
        self.add_line(right_slab_start, approach_top, right_slab_end, approach_top, 'approach_slab', 2)
        self.add_line(right_slab_start, approach_top, right_slab_start, approach_bottom, 'approach_slab', 1)
        self.add_line(right_slab_end, approach_top, right_slab_end, approach_bottom, 'approach_slab', 1)
        self.add_line(right_slab_start, approach_bottom, right_slab_end, approach_bottom, 'approach_slab', 2)
        
    def add_professional_annotations(self):
        """Add professional annotations like original program"""
        left = float(self.params.get('LEFT', 0))
        lbridge = float(self.params.get('LBRIDGE', 30000))
        toprl = float(self.params.get('TOPRL', 110000))
        sofl = float(self.params.get('SOFL', 108000))
        nspan = int(self.params.get('NSPAN', 1))
        span1 = float(self.params.get('SPAN1', 30000))
        scale1 = int(self.params.get('SCALE1', 100))
        
        # Title
        title_x = left + lbridge / 2
        title_y = toprl + 2500
        self.add_text(title_x, title_y, "BRIDGE ELEVATION", 800)
        
        # Scale annotation
        scale_x = left + 1000
        scale_y = toprl + 1500
        self.add_text(scale_x, scale_y, f"SCALE 1:{scale1}", 400)
        
        # Bridge length dimension
        dim_y = sofl - 3000
        self.add_text(left + lbridge / 2, dim_y, f"BRIDGE LENGTH = {lbridge/1000:.1f}M", 400)
        
        # Span annotations
        if nspan > 1:
            span_length = lbridge / nspan
            for i in range(nspan):
                span_center_x = left + (i + 0.5) * span_length
                span_y = sofl - 1500
                self.add_text(span_center_x, span_y, f"SPAN {i+1}", 300)
        else:
            # Single span
            span_center_x = left + lbridge / 2
            span_y = sofl - 1500
            self.add_text(span_center_x, span_y, f"SPAN = {lbridge/1000:.1f}M", 400)
            
        # Level annotations
        level_x = left - 2000
        self.add_text(level_x, toprl, f"TOP RL {toprl/1000:.1f}", 300)
        self.add_text(level_x, sofl, f"SOFFIT RL {sofl/1000:.1f}", 300)
        
        # Abutment labels
        abt_y = (toprl + sofl) / 2
        self.add_text(left + 2000, abt_y, "LEFT\nABUTMENT", 350)
        self.add_text(left + lbridge - 2000, abt_y, "RIGHT\nABUTMENT", 350)
        
        # Pier labels for multi-span
        if nspan > 1:
            for pier_num in range(1, nspan):
                pier_x = left + (pier_num * span1)
                pier_y = (toprl + sofl) / 2
                self.add_text(pier_x, pier_y, f"PIER {pier_num}", 350)
    
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
    
    def draw_abutment(self, side, x_start, width, top_level, footing_level):
        """Draw abutment structure"""
        # Get soffit level from parameters
        soffit_level = float(self.params.get('SOFL', 108000))
        
        if side == 'left':
            # Left abutment - vertical face at bridge start
            self.add_line(x_start, footing_level, x_start + width, footing_level, 'abutment', 1)  # Bottom
            self.add_line(x_start + width, footing_level, x_start + width, top_level, 'abutment', 1)  # Back wall
            self.add_line(x_start, top_level, x_start, soffit_level, 'abutment', 1)  # Front upper
            self.add_line(x_start, soffit_level, x_start, footing_level, 'abutment', 1)  # Front lower
            # Connect soffit to back wall
            self.add_line(x_start, soffit_level, x_start + width, soffit_level, 'abutment', 1)
        else:
            # Right abutment - vertical face at bridge end
            self.add_line(x_start, footing_level, x_start + width, footing_level, 'abutment', 1)  # Bottom
            self.add_line(x_start, footing_level, x_start, top_level, 'abutment', 1)  # Back wall
            self.add_line(x_start + width, top_level, x_start + width, soffit_level, 'abutment', 1)  # Front upper
            self.add_line(x_start + width, soffit_level, x_start + width, footing_level, 'abutment', 1)  # Front lower
            # Connect soffit to back wall
            self.add_line(x_start, soffit_level, x_start + width, soffit_level, 'abutment', 1)
    
    def draw_piers(self, left, lbridge, nspan, toprl, sofl):
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
            
            # Cap at soffit level
            if capb != capt:
                self.add_line(pier_left, capb, pier_right, capb, 'pier', 1)  # Cap division
                
    def draw_wingwalls(self, left, lbridge, toprl, alfl, arfl):
        """Draw wing walls at abutments"""
        winglen = float(self.params.get('WINGLEN', 5000))  # Wing wall length
        
        # Left wing walls
        # Front wing wall
        self.add_line(left - winglen, alfl, left, alfl, 'wingwall', 1)
        self.add_line(left - winglen, alfl, left - winglen, toprl, 'wingwall', 1)
        # Back wing wall
        abtlen = float(self.params.get('ABTLEN', 10000))
        self.add_line(left + abtlen, alfl, left + abtlen + winglen, alfl, 'wingwall', 1)
        self.add_line(left + abtlen + winglen, alfl, left + abtlen + winglen, toprl, 'wingwall', 1)
        
        # Right wing walls
        # Front wing wall
        self.add_line(left + lbridge, arfl, left + lbridge + winglen, arfl, 'wingwall', 1)
        self.add_line(left + lbridge + winglen, arfl, left + lbridge + winglen, toprl, 'wingwall', 1)
        # Back wing wall
        self.add_line(left + lbridge - abtlen - winglen, arfl, left + lbridge - abtlen, arfl, 'wingwall', 1)
        self.add_line(left + lbridge - abtlen - winglen, arfl, left + lbridge - abtlen - winglen, toprl, 'wingwall', 1)
    
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