import math
import os
import ezdxf
from math import atan2, degrees, sqrt, cos, sin, tan, radians, pi
import logging
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.colors import black, blue, red
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
        try:
            self.doc = ezdxf.new("R2010", setup=True)
            self.msp = self.doc.modelspace()
            logging.info("DXF document created successfully")
        except Exception as e:
            logging.error(f"Failed to create DXF document: {e}")
            raise
    
    def calculate_derived_values(self):
        """Calculate derived values from input parameters"""
        self.scale1 = self.params.get('SCALE1', 100)
        self.scale2 = self.params.get('SCALE2', 100)
        self.sc = self.scale1 / self.scale2 if self.scale2 != 0 else 1
        
        self.skew = self.params.get('SKEW', 0)
        self.datum = self.params.get('DATUM', 100000)
        self.left = self.params.get('LEFT', 0)
        
        logging.info(f"Calculated values - Scale: {self.sc}, Skew: {self.skew}, Datum: {self.datum}")
    
    def draw_bridge_elevation(self):
        """Draw the main bridge elevation view"""
        try:
            # Get key parameters with safe defaults
            lbridge = float(self.params.get('LBRIDGE', 30000))
            toprl = float(self.params.get('TOPRL', 110000))
            sofl = float(self.params.get('SOFL', 108000))
            left_pos = float(self.left)
            
            # Simple coordinate scaling for drawing
            scale_factor = 0.01  # Scale down for drawing visibility
            
            # Calculate drawing coordinates
            start_x = left_pos * scale_factor
            end_x = (left_pos + lbridge) * scale_factor
            top_y = toprl * scale_factor
            soffit_y = sofl * scale_factor
            
            # Draw bridge deck (top line)
            self.msp.add_line((start_x, top_y), (end_x, top_y))
            
            # Draw soffit line (bottom line)
            self.msp.add_line((start_x, soffit_y), (end_x, soffit_y))
            
            # Draw end lines
            self.msp.add_line((start_x, soffit_y), (start_x, top_y))
            self.msp.add_line((end_x, soffit_y), (end_x, top_y))
            
            # Draw abutments
            self.draw_abutments(scale_factor)
            
            # Draw piers if any
            nspan = int(self.params.get('NSPAN', 1))
            if nspan > 1:
                self.draw_piers(scale_factor)
                
            logging.info("Bridge elevation drawn successfully")
            
        except Exception as e:
            logging.error(f"Error drawing bridge elevation: {e}")
            raise
    
    def draw_abutments(self, scale_factor):
        """Draw bridge abutments"""
        try:
            # Get abutment parameters
            abtlen = float(self.params.get('ABTLEN', 10000))
            alfl = float(self.params.get('ALFL', 105000))
            arfl = float(self.params.get('ARFL', 105000))
            toprl = float(self.params.get('TOPRL', 110000))
            lbridge = float(self.params.get('LBRIDGE', 30000))
            left_pos = float(self.left)
            
            # Left abutment
            left_start = left_pos * scale_factor
            left_end = (left_pos + abtlen) * scale_factor
            top_level = toprl * scale_factor
            left_footing = alfl * scale_factor
            
            # Draw left abutment rectangle
            self.msp.add_line((left_start, left_footing), (left_end, left_footing))
            self.msp.add_line((left_end, left_footing), (left_end, top_level))
            self.msp.add_line((left_end, top_level), (left_start, top_level))
            self.msp.add_line((left_start, top_level), (left_start, left_footing))
            
            # Right abutment
            right_start = (left_pos + lbridge - abtlen) * scale_factor
            right_end = (left_pos + lbridge) * scale_factor
            right_footing = arfl * scale_factor
            
            # Draw right abutment rectangle
            self.msp.add_line((right_start, right_footing), (right_end, right_footing))
            self.msp.add_line((right_end, right_footing), (right_end, top_level))
            self.msp.add_line((right_end, top_level), (right_start, top_level))
            self.msp.add_line((right_start, top_level), (right_start, right_footing))
            
            logging.info("Abutments drawn successfully")
            
        except Exception as e:
            logging.error(f"Error drawing abutments: {e}")
    
    def draw_piers(self, scale_factor):
        """Draw bridge piers"""
        try:
            nspan = int(self.params.get('NSPAN', 1))
            lbridge = float(self.params.get('LBRIDGE', 30000))
            span_length = lbridge / nspan
            left_pos = float(self.left)
            
            capt = float(self.params.get('CAPT', 109000))
            capb = float(self.params.get('CAPB', 108000))
            futrl = float(self.params.get('FUTRL', 105000))
            piertw = float(self.params.get('PIERTW', 2000))
            
            for i in range(1, nspan):
                pier_x = left_pos + (i * span_length)
                pier_center = pier_x * scale_factor
                pier_half_width = (piertw / 2) * scale_factor
                
                cap_top = capt * scale_factor
                cap_bottom = capb * scale_factor
                foundation = futrl * scale_factor
                
                # Draw pier rectangle
                pier_left = pier_center - pier_half_width
                pier_right = pier_center + pier_half_width
                
                # Pier outline
                self.msp.add_line((pier_left, foundation), (pier_right, foundation))
                self.msp.add_line((pier_right, foundation), (pier_right, cap_top))
                self.msp.add_line((pier_right, cap_top), (pier_left, cap_top))
                self.msp.add_line((pier_left, cap_top), (pier_left, foundation))
                
                # Cap detail
                self.msp.add_line((pier_left, cap_bottom), (pier_right, cap_bottom))
                
            logging.info(f"Drew {nspan-1} piers successfully")
            
        except Exception as e:
            logging.error(f"Error drawing piers: {e}")
    
    def add_dimensions_and_labels(self):
        """Add dimensions and labels to the drawing"""
        try:
            scale_factor = 0.01
            lbridge = float(self.params.get('LBRIDGE', 30000))
            toprl = float(self.params.get('TOPRL', 110000))
            left_pos = float(self.left)
            
            # Add title above the bridge
            title_x = (left_pos + lbridge / 2) * scale_factor
            title_y = (toprl + 5000) * scale_factor
            
            self.msp.add_text(
                "SLAB BRIDGE ELEVATION",
                dxfattribs={'height': 100, 'insert': (title_x, title_y)}
            )
            
            # Add scale note
            scale_x = left_pos * scale_factor
            scale_y = (toprl + 2000) * scale_factor
            scale_text = f"SCALE 1:{self.scale1}"
            
            self.msp.add_text(
                scale_text,
                dxfattribs={'height': 50, 'insert': (scale_x, scale_y)}
            )
            
            # Add span labels
            nspan = int(self.params.get('NSPAN', 1))
            span_length = lbridge / nspan
            sofl = float(self.params.get('SOFL', 108000))
            
            for i in range(nspan):
                span_center_x = (left_pos + (i + 0.5) * span_length) * scale_factor
                span_y = (sofl - 3000) * scale_factor
                span_text = f"SPAN {i+1} = {span_length/1000:.1f}M"
                
                self.msp.add_text(
                    span_text,
                    dxfattribs={'height': 40, 'insert': (span_center_x, span_y)}
                )
            
            logging.info("Dimensions and labels added successfully")
            
        except Exception as e:
            logging.error(f"Error adding dimensions and labels: {e}")
    
    def generate_dxf(self):
        """Generate the complete DXF drawing"""
        try:
            logging.info("Starting DXF generation")
            
            # Draw main bridge elements
            self.draw_bridge_elevation()
            
            # Add dimensions and labels
            self.add_dimensions_and_labels()
            
            # Save to string buffer
            string_buffer = io.StringIO()
            self.doc.write(string_buffer)
            dxf_content = string_buffer.getvalue()
            string_buffer.close()
            
            logging.info("DXF generation completed successfully")
            return dxf_content.encode('utf-8')
            
        except Exception as e:
            logging.error(f"Error generating DXF: {str(e)}")
            raise Exception(f"Failed to generate bridge drawing: {str(e)}")
    
    def generate_pdf_from_drawing_data(self, drawing_data):
        """Generate PDF using unified drawing data"""
        try:
            logging.info("Starting PDF generation with drawing data")
            
            from drawing_engine import BridgeRenderer
            
            pdf_buffer = io.BytesIO()
            page_width, page_height = landscape(A4)
            c = canvas.Canvas(pdf_buffer, pagesize=landscape(A4))
            
            margin = 20 * mm
            drawing_width = page_width - 2 * margin
            drawing_height = page_height - 2 * margin
            
            # Use drawing data bounds
            bounds = drawing_data['bounds']
            bridge_width_mm = bounds['max_x'] - bounds['min_x']
            bridge_height_mm = bounds['max_y'] - bounds['min_y']
            
            # Calculate scale
            available_width_mm = drawing_width / mm
            available_height_mm = drawing_height / mm
            
            scale_x = available_width_mm / bridge_width_mm if bridge_width_mm > 0 else 1
            scale_y = available_height_mm / bridge_height_mm if bridge_height_mm > 0 else 1
            pdf_scale = min(scale_x, scale_y, 1.0)
            
            logging.info(f"PDF Scale: {pdf_scale}, Bridge: {bridge_width_mm}x{bridge_height_mm}mm")
            
            # Center drawing
            final_width_pts = bridge_width_mm * pdf_scale * mm
            final_height_pts = bridge_height_mm * pdf_scale * mm
            offset_x = margin + (drawing_width - final_width_pts) / 2
            offset_y = margin + (drawing_height - final_height_pts) / 2
            
            # Transform coordinates
            def transform_x(x):
                return offset_x + (x - bounds['min_x']) * pdf_scale * mm
            
            def transform_y(y):
                return offset_y + (bounds['max_y'] - y) * pdf_scale * mm
            
            # Set drawing properties
            c.setLineWidth(0.5)
            c.setStrokeColor(black)
            
            # Draw all elements
            for elem in drawing_data['elements']:
                if elem['type'] == 'line':
                    x1 = transform_x(elem['x1'])
                    y1 = transform_y(elem['y1'])
                    x2 = transform_x(elem['x2'])
                    y2 = transform_y(elem['y2'])
                    c.setLineWidth(elem['width'] * 0.5)
                    c.line(x1, y1, x2, y2)
            
            # Draw text
            for text in drawing_data['texts']:
                x = transform_x(text['x'])
                y = transform_y(text['y'])
                font_size = max(8, text['size'] * pdf_scale / 50)
                
                c.setFont("Helvetica", font_size)
                text_width = c.stringWidth(text['text'], "Helvetica", font_size)
                c.drawString(x - text_width/2, y, text['text'])
            
            c.save()
            pdf_content = pdf_buffer.getvalue()
            pdf_buffer.close()
            
            logging.info("PDF generation completed successfully")
            return pdf_content
            
        except Exception as e:
            logging.error(f"Error generating PDF: {str(e)}")
            raise Exception(f"Failed to generate bridge PDF: {str(e)}")
    
    
    
    def draw_bridge_pdf(self, c, offset_x, offset_y, pdf_scale):
        """Draw bridge elements on PDF"""
        try:
            # Get parameters
            lbridge = float(self.params.get('LBRIDGE', 30000))
            toprl = float(self.params.get('TOPRL', 110000))
            sofl = float(self.params.get('SOFL', 108000))
            left_pos = float(self.left)
            
            # Transform coordinates from mm to points with proper scaling
            def transform_x(x_mm):
                return offset_x + ((x_mm - left_pos) * pdf_scale * mm)
            
            def transform_y(y_mm):
                base_y = sofl - 5000  # Base reference in mm
                return offset_y + ((y_mm - base_y) * pdf_scale * mm)
            
            # Get all required parameters for complete bridge drawing
            abtlen = float(self.params.get('ABTLEN', 10000))
            alfl = float(self.params.get('ALFL', 105000))
            arfl = float(self.params.get('ARFL', 105000))
            nspan = int(self.params.get('NSPAN', 1))
            
            # Calculate all drawing coordinates
            bridge_start_x = transform_x(left_pos)
            bridge_end_x = transform_x(left_pos + lbridge)
            deck_top_y = transform_y(toprl)
            deck_bottom_y = transform_y(sofl)
            
            # Draw main bridge deck outline
            c.line(bridge_start_x, deck_top_y, bridge_end_x, deck_top_y)  # Top deck
            c.line(bridge_start_x, deck_bottom_y, bridge_end_x, deck_bottom_y)  # Bottom soffit
            
            # Draw left abutment details
            left_abt_front = transform_x(left_pos)
            left_abt_back = transform_x(left_pos + abtlen)
            left_footing_y = transform_y(alfl)
            
            # Left abutment outline (not just rectangle)
            c.line(left_abt_front, left_footing_y, left_abt_back, left_footing_y)  # Bottom
            c.line(left_abt_back, left_footing_y, left_abt_back, deck_top_y)      # Back wall
            c.line(left_abt_back, deck_top_y, left_abt_front, deck_top_y)        # Top
            c.line(left_abt_front, deck_top_y, left_abt_front, deck_bottom_y)    # Front upper
            c.line(left_abt_front, deck_bottom_y, left_abt_front, left_footing_y) # Front lower
            
            # Right abutment details
            right_abt_front = transform_x(left_pos + lbridge)
            right_abt_back = transform_x(left_pos + lbridge - abtlen)
            right_footing_y = transform_y(arfl)
            
            # Right abutment outline
            c.line(right_abt_back, right_footing_y, right_abt_front, right_footing_y)  # Bottom
            c.line(right_abt_back, right_footing_y, right_abt_back, deck_top_y)        # Back wall
            c.line(right_abt_back, deck_top_y, right_abt_front, deck_top_y)           # Top
            c.line(right_abt_front, deck_top_y, right_abt_front, deck_bottom_y)       # Front upper
            c.line(right_abt_front, deck_bottom_y, right_abt_front, right_footing_y)  # Front lower
            
            # Draw piers if multi-span bridge
            if nspan > 1:
                span_length = lbridge / nspan
                capt = float(self.params.get('CAPT', 109000))
                capb = float(self.params.get('CAPB', 108000))
                futrl = float(self.params.get('FUTRL', 105000))
                piertw = float(self.params.get('PIERTW', 2000))
                
                for i in range(1, nspan):
                    pier_center_x = left_pos + (i * span_length)
                    pier_x = transform_x(pier_center_x)
                    pier_half_width = transform_x(pier_center_x + piertw/2) - pier_x
                    
                    cap_top_y = transform_y(capt)
                    cap_bottom_y = transform_y(capb)
                    foundation_y = transform_y(futrl)
                    
                    # Pier outline
                    pier_left = pier_x - pier_half_width
                    pier_right = pier_x + pier_half_width
                    
                    c.line(pier_left, foundation_y, pier_right, foundation_y)    # Foundation
                    c.line(pier_right, foundation_y, pier_right, cap_top_y)      # Right side
                    c.line(pier_right, cap_top_y, pier_left, cap_top_y)         # Top
                    c.line(pier_left, cap_top_y, pier_left, foundation_y)       # Left side
                    c.line(pier_left, cap_bottom_y, pier_right, cap_bottom_y)   # Cap division
            
            # Add text labels
            c.setFont("Helvetica-Bold", 12)
            title_x = transform_x(left_pos + lbridge / 2)
            title_y = transform_y(toprl + 3000)
            title_text = "SLAB BRIDGE ELEVATION"
            text_width = c.stringWidth(title_text, "Helvetica-Bold", 12)
            c.drawString(title_x - text_width/2, title_y, title_text)
            
            # Scale note
            c.setFont("Helvetica", 10)
            scale_text = f"SCALE 1:{int(1/scale)}" if scale < 1 else "SCALE 1:1"
            c.drawString(start_x, transform_y(toprl + 1500), scale_text)
            
            # Span labels
            nspan = int(self.params.get('NSPAN', 1))
            span_length = lbridge / nspan
            c.setFont("Helvetica", 8)
            
            for i in range(nspan):
                span_center_x = transform_x(left_pos + (i + 0.5) * span_length)
                span_y = transform_y(sofl - 2000)
                span_text = f"SPAN {i+1} = {span_length/1000:.1f}M"
                text_width = c.stringWidth(span_text, "Helvetica", 8)
                c.drawString(span_center_x - text_width/2, span_y, span_text)
            
        except Exception as e:
            logging.error(f"Error drawing bridge PDF: {e}")
            raise