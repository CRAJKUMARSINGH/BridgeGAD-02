import math
import os
import ezdxf
from math import atan2, degrees, sqrt, cos, sin, tan, radians, pi
import logging
import io

class BridgeCADGenerator:
    """Main class for generating bridge CAD drawings from parameters"""
    
    def __init__(self, parameters):
        self.params = parameters
        self.doc = None
        self.msp = None
        self.setup_document()
        self.calculate_derived_values()
        
    def setup_document(self):
        """Initialize DXF document with proper settings"""
        self.doc = ezdxf.new("R2010", setup=True)
        self.msp = self.doc.modelspace()
        
        # Set up text style
        try:
            self.doc.styles.new("Arial", dxfattribs={'font': 'Arial.ttf'})
        except:
            logging.warning("Arial font not available, using default")
            
        # Set up dimension style
        try:
            dimstyle = self.doc.dimstyles.new('PMB100')
            dimstyle.dxf.dimasz = 150
            dimstyle.dxf.dimtdec = 0
            dimstyle.dxf.dimexe = 400
            dimstyle.dxf.dimexo = 400
            dimstyle.dxf.dimlfac = 1
            dimstyle.dxf.dimtxsty = "Arial"
            dimstyle.dxf.dimtxt = 400
            dimstyle.dxf.dimtad = 0
        except Exception as e:
            logging.warning(f"Could not set dimension style: {e}")
    
    def calculate_derived_values(self):
        """Calculate derived values from input parameters"""
        self.scale1 = self.params.get('SCALE1', 100)
        self.scale2 = self.params.get('SCALE2', 100)
        self.sc = self.scale1 / self.scale2 if self.scale2 != 0 else 1
        
        self.skew = self.params.get('SKEW', 0)
        self.skew_rad = self.skew * 0.0174532  # Convert to radians
        self.sin_skew = math.sin(self.skew_rad)
        self.cos_skew = math.cos(self.skew_rad)
        self.tan_skew = self.sin_skew / self.cos_skew if self.cos_skew != 0 else 0
        
        self.datum = self.params.get('DATUM', 100000)
        self.left = self.params.get('LEFT', 0)
        
        # Vertical and horizontal scale factors
        self.vvs = 1000.0
        self.hhs = 1000.0
        
    def vpos(self, a):
        """Convert vertical position"""
        return self.datum + self.vvs * (a - self.datum)
        
    def hpos(self, a):
        """Convert horizontal position"""
        return self.left + self.hhs * (a - self.left)
        
    def v2pos(self, a):
        """Convert vertical position with scale"""
        return self.datum + self.sc * self.vvs * (a - self.datum)
        
    def h2pos(self, a):
        """Convert horizontal position with scale"""
        return self.left + self.sc * self.hhs * (a - self.left)
    
    def add_text(self, text, insert, height, rotation=0):
        """Add text to the drawing"""
        self.msp.add_text(str(text), dxfattribs={
            'height': height, 
            'insert': insert, 
            'rotation': rotation
        })
    
    def draw_line(self, points):
        """Draw connected lines from a list of points"""
        for i in range(len(points) - 1):
            self.msp.add_line(points[i], points[i + 1])
    
    def draw_rectangle(self, pt1, pt2):
        """Draw a rectangle from two corner points"""
        self.msp.add_line(pt1, (pt2[0], pt1[1]))  # Bottom line
        self.msp.add_line((pt2[0], pt1[1]), pt2)  # Right line
        self.msp.add_line(pt2, (pt1[0], pt2[1]))  # Top line
        self.msp.add_line((pt1[0], pt2[1]), pt1)  # Left line
    
    def draw_bridge_elevation(self):
        """Draw the main bridge elevation view"""
        # Get key parameters
        abtlen = self.params.get('ABTLEN', 10000)
        laslab = self.params.get('LASLAB', 5000)
        lbridge = self.params.get('LBRIDGE', 30000)
        toprl = self.params.get('TOPRL', 110000)
        sofl = self.params.get('SOFL', 108000)
        
        # Convert positions using helper functions
        left_start = self.hpos(self.left)
        bridge_end = self.hpos(self.left + lbridge)
        top_level = self.vpos(toprl)
        soffit_level = self.vpos(sofl)
        
        # Draw bridge deck
        self.msp.add_line((left_start, top_level), (bridge_end, top_level))
        
        # Draw soffit line
        self.msp.add_line((left_start, soffit_level), (bridge_end, soffit_level))
        
        # Draw abutments
        self.draw_abutments()
        
        # Draw piers if any
        nspan = int(self.params.get('NSPAN', 1))
        if nspan > 1:
            self.draw_piers()
    
    def draw_abutments(self):
        """Draw bridge abutments"""
        # Left abutment
        abtl = self.params.get('ABTL', 0)
        abtlen = self.params.get('ABTLEN', 10000)
        alfl = self.params.get('ALFL', 105000)
        arfl = self.params.get('ARFL', 105000)
        toprl = self.params.get('TOPRL', 110000)
        
        # Convert positions
        left_abt_start = self.hpos(abtl)
        left_abt_end = self.hpos(abtl + abtlen)
        top_level = self.vpos(toprl)
        left_footing = self.vpos(alfl)
        
        # Left abutment outline
        left_abt_points = [
            (left_abt_start, top_level),
            (left_abt_start, left_footing),
            (left_abt_end, left_footing),
            (left_abt_end, top_level)
        ]
        self.draw_line(left_abt_points + [left_abt_points[0]])
        
        # Right abutment
        lbridge = self.params.get('LBRIDGE', 30000)
        right_footing = self.vpos(arfl)
        right_abt_start = self.hpos(self.left + lbridge - abtlen)
        right_abt_end = self.hpos(self.left + lbridge)
        
        right_abt_points = [
            (right_abt_start, top_level),
            (right_abt_start, right_footing),
            (right_abt_end, right_footing),
            (right_abt_end, top_level)
        ]
        self.draw_line(right_abt_points + [right_abt_points[0]])
    
    def draw_piers(self):
        """Draw bridge piers"""
        nspan = int(self.params.get('NSPAN', 1))
        lbridge = self.params.get('LBRIDGE', 30000)
        span_length = lbridge / nspan
        
        capt = self.params.get('CAPT', 109000)
        capb = self.params.get('CAPB', 108000)
        futrl = self.params.get('FUTRL', 105000)
        piertw = self.params.get('PIERTW', 2000)
        
        for i in range(1, nspan):
            pier_x = self.left + (i * span_length)
            
            # Convert positions
            pier_center = self.hpos(pier_x)
            pier_left = self.hpos(pier_x - piertw/2)
            pier_right = self.hpos(pier_x + piertw/2)
            cap_top = self.vpos(capt)
            cap_bottom = self.vpos(capb)
            foundation = self.vpos(futrl)
            
            # Pier cap
            self.msp.add_line((pier_left, cap_top), (pier_right, cap_top))
            self.msp.add_line((pier_left, cap_bottom), (pier_right, cap_bottom))
            
            # Pier shaft
            pier_points = [
                (pier_left, cap_bottom),
                (pier_left, foundation),
                (pier_right, foundation),
                (pier_right, cap_bottom)
            ]
            self.draw_line(pier_points + [pier_points[0]])
    
    def add_dimensions_and_labels(self):
        """Add dimensions and labels to the drawing"""
        # Add title
        lbridge = self.params.get('LBRIDGE', 30000)
        toprl = self.params.get('TOPRL', 110000)
        
        title_x = self.hpos(self.left + lbridge / 2)
        title_y = self.vpos(toprl + 2000)
        self.add_text("SLAB BRIDGE ELEVATION", (title_x, title_y), 800)
        
        # Add scale note
        scale_text = f"SCALE 1:{self.scale1}"
        scale_x = self.hpos(self.left)
        scale_y = self.vpos(toprl + 1000)
        self.add_text(scale_text, (scale_x, scale_y), 400)
        
        # Add span labels
        nspan = int(self.params.get('NSPAN', 1))
        span_length = lbridge / nspan
        sofl = self.params.get('SOFL', 108000)
        
        for i in range(nspan):
            span_center_x = self.hpos(self.left + (i + 0.5) * span_length)
            span_y = self.vpos(sofl - 1000)
            span_text = f"SPAN {i+1} = {span_length/1000:.1f}M"
            self.add_text(span_text, (span_center_x, span_y), 300)
    
    def generate_dxf(self):
        """Generate the complete DXF drawing"""
        try:
            # Draw main bridge elements
            self.draw_bridge_elevation()
            
            # Add dimensions and labels
            self.add_dimensions_and_labels()
            
            # Save to string buffer and convert to bytes
            string_buffer = io.StringIO()
            self.doc.write(string_buffer)
            dxf_content = string_buffer.getvalue()
            string_buffer.close()
            
            # Convert to bytes for download
            return dxf_content.encode('utf-8')
            
        except Exception as e:
            logging.error(f"Error generating DXF: {str(e)}")
            raise Exception(f"Failed to generate bridge drawing: {str(e)}")