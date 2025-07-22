"""
Bridge parameter definitions and grouping for the web interface
"""

PARAMETER_DEFINITIONS = {
    # Scale and General Parameters
    'SCALE1': {
        'name': 'Primary Scale',
        'type': 'int',
        'default': 100,
        'min': 1,
        'max': 1000,
        'unit': '',
        'description': 'Primary drawing scale factor'
    },
    'SCALE2': {
        'name': 'Secondary Scale',
        'type': 'int',
        'default': 100,
        'min': 1,
        'max': 1000,
        'unit': '',
        'description': 'Secondary drawing scale factor'
    },
    'SKEW': {
        'name': 'Bridge Skew Angle',
        'type': 'float',
        'default': 0,
        'min': -45,
        'max': 45,
        'unit': '°',
        'description': 'Angle of skew for the bridge in degrees'
    },
    'DATUM': {
        'name': 'Drawing Datum',
        'type': 'float',
        'default': 100000,
        'min': 0,
        'max': 200000,
        'unit': 'mm',
        'description': 'Reference datum level for the drawing'
    },
    'TOPRL': {
        'name': 'Top RL of Bridge',
        'type': 'float',
        'default': 110000,
        'min': 90000,
        'max': 150000,
        'unit': 'mm',
        'description': 'Top level of the bridge deck'
    },
    'LEFT': {
        'name': 'Left Chainage',
        'type': 'float',
        'default': 0,
        'min': 0,
        'max': 100000,
        'unit': 'm',
        'description': 'Left-most chainage point'
    },
    'RIGHT': {
        'name': 'Right Chainage',
        'type': 'float',
        'default': 50000,
        'min': 10000,
        'max': 200000,
        'unit': 'm',
        'description': 'Right-most chainage point'
    },
    
    # Bridge Geometry
    'NSPAN': {
        'name': 'Number of Spans',
        'type': 'int',
        'default': 1,
        'min': 1,
        'max': 10,
        'unit': '',
        'description': 'Total number of bridge spans'
    },
    'LBRIDGE': {
        'name': 'Bridge Length',
        'type': 'float',
        'default': 30000,
        'min': 5000,
        'max': 200000,
        'unit': 'mm',
        'description': 'Total length of the bridge'
    },
    'SPAN1': {
        'name': 'Individual Span Length',
        'type': 'float',
        'default': 30000,
        'min': 5000,
        'max': 50000,
        'unit': 'mm',
        'description': 'Length of individual spans'
    },
    'CCBR': {
        'name': 'Clear Carriageway Width',
        'type': 'float',
        'default': 7500,
        'min': 3000,
        'max': 20000,
        'unit': 'mm',
        'description': 'Clear width of the carriageway'
    },
    
    # Slab Parameters
    'SLBTHC': {
        'name': 'Slab Thickness at Centre',
        'type': 'float',
        'default': 1000,
        'min': 200,
        'max': 2000,
        'unit': 'mm',
        'description': 'Thickness of slab at center'
    },
    'SLBTHE': {
        'name': 'Slab Thickness at Edge',
        'type': 'float',
        'default': 800,
        'min': 200,
        'max': 2000,
        'unit': 'mm',
        'description': 'Thickness of slab at edge'
    },
    'SLBTHT': {
        'name': 'Slab Thickness at Tip',
        'type': 'float',
        'default': 600,
        'min': 150,
        'max': 1500,
        'unit': 'mm',
        'description': 'Thickness of slab at tip'
    },
    'SOFL': {
        'name': 'Soffit Level',
        'type': 'float',
        'default': 108000,
        'min': 90000,
        'max': 148000,
        'unit': 'mm',
        'description': 'Level of the bridge soffit'
    },
    
    # Kerb Parameters
    'KERBW': {
        'name': 'Kerb Width',
        'type': 'float',
        'default': 300,
        'min': 100,
        'max': 600,
        'unit': 'mm',
        'description': 'Width of the kerb'
    },
    'KERBD': {
        'name': 'Kerb Depth',
        'type': 'float',
        'default': 150,
        'min': 100,
        'max': 300,
        'unit': 'mm',
        'description': 'Depth of the kerb'
    },
    
    # Abutment Parameters
    'ABTLEN': {
        'name': 'Abutment Length',
        'type': 'float',
        'default': 10000,
        'min': 5000,
        'max': 20000,
        'unit': 'mm',
        'description': 'Length of the abutment'
    },
    'ABTL': {
        'name': 'Left Abutment Chainage',
        'type': 'float',
        'default': 0,
        'min': 0,
        'max': 50000,
        'unit': 'm',
        'description': 'Chainage of the left abutment'
    },
    'ALCW': {
        'name': 'Left Abutment Cap Width',
        'type': 'float',
        'default': 1200,
        'min': 800,
        'max': 2000,
        'unit': 'mm',
        'description': 'Width of left abutment cap excluding dirt wall'
    },
    'ALCD': {
        'name': 'Left Abutment Cap Depth',
        'type': 'float',
        'default': 800,
        'min': 500,
        'max': 1500,
        'unit': 'mm',
        'description': 'Depth of left abutment cap'
    },
    'ALFL': {
        'name': 'Left Abutment Footing Level',
        'type': 'float',
        'default': 105000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Footing level of left abutment'
    },
    'ARFL': {
        'name': 'Right Abutment Footing Level',
        'type': 'float',
        'default': 105000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Footing level of right abutment'
    },
    'ALFB': {
        'name': 'Left Abutment Front Batter',
        'type': 'float',
        'default': 0.1,
        'min': 0,
        'max': 0.5,
        'unit': '',
        'description': 'Front batter ratio for left abutment'
    },
    'ALFBL': {
        'name': 'Left Abutment Front Batter RL',
        'type': 'float',
        'default': 108000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Reference level for left abutment front batter'
    },
    'ALFBR': {
        'name': 'Right Abutment Front Batter RL',
        'type': 'float',
        'default': 108000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Reference level for right abutment front batter'
    },
    'ALTB': {
        'name': 'Left Abutment Toe Batter',
        'type': 'float',
        'default': 0.1,
        'min': 0,
        'max': 0.5,
        'unit': '',
        'description': 'Toe batter ratio for left abutment'
    },
    'ALTBL': {
        'name': 'Left Abutment Toe Batter Level',
        'type': 'float',
        'default': 107000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Footing top level for left abutment toe batter'
    },
    'ALTBR': {
        'name': 'Right Abutment Toe Batter Level',
        'type': 'float',
        'default': 107000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Footing top level for right abutment toe batter'
    },
    'ALFO': {
        'name': 'Left Abutment Front Offset to Footing',
        'type': 'float',
        'default': 500,
        'min': 200,
        'max': 1000,
        'unit': 'mm',
        'description': 'Front offset to footing for left abutment'
    },
    'ALFD': {
        'name': 'Left Abutment Footing Depth',
        'type': 'float',
        'default': 1000,
        'min': 500,
        'max': 2000,
        'unit': 'mm',
        'description': 'Depth of left abutment footing'
    },
    'ALBB': {
        'name': 'Left Abutment Back Batter',
        'type': 'float',
        'default': 0.05,
        'min': 0,
        'max': 0.3,
        'unit': '',
        'description': 'Back batter ratio for left abutment'
    },
    'ALBBL': {
        'name': 'Left Abutment Back Batter RL',
        'type': 'float',
        'default': 108000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Reference level for left abutment back batter'
    },
    'ALBBR': {
        'name': 'Right Abutment Back Batter RL',
        'type': 'float',
        'default': 108000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Reference level for right abutment back batter'
    },
    'DWTH': {
        'name': 'Dirt Wall Thickness',
        'type': 'float',
        'default': 300,
        'min': 200,
        'max': 500,
        'unit': 'mm',
        'description': 'Thickness of dirt wall'
    },
    
    # Pier Parameters
    'CAPT': {
        'name': 'Pier Cap Top RL',
        'type': 'float',
        'default': 109000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Top level of pier cap'
    },
    'CAPB': {
        'name': 'Pier Cap Bottom RL',
        'type': 'float',
        'default': 108000,
        'min': 90000,
        'max': 145000,
        'unit': 'mm',
        'description': 'Bottom level of pier cap'
    },
    'CAPW': {
        'name': 'Pier Cap Width',
        'type': 'float',
        'default': 2000,
        'min': 1000,
        'max': 4000,
        'unit': 'mm',
        'description': 'Width of pier cap'
    },
    'PIERTW': {
        'name': 'Pier Top Width',
        'type': 'float',
        'default': 1500,
        'min': 800,
        'max': 3000,
        'unit': 'mm',
        'description': 'Top width of pier'
    },
    'BATTR': {
        'name': 'Pier Batter',
        'type': 'float',
        'default': 0.02,
        'min': 0,
        'max': 0.1,
        'unit': '',
        'description': 'Batter ratio for pier'
    },
    'PIERST': {
        'name': 'Pier Straight Length',
        'type': 'float',
        'default': 5000,
        'min': 2000,
        'max': 15000,
        'unit': 'mm',
        'description': 'Straight length of pier'
    },
    'PIERN': {
        'name': 'Pier Serial Number',
        'type': 'int',
        'default': 1,
        'min': 1,
        'max': 20,
        'unit': '',
        'description': 'Serial number of pier'
    },
    'FUTRL': {
        'name': 'Foundation RL',
        'type': 'float',
        'default': 100000,
        'min': 85000,
        'max': 140000,
        'unit': 'mm',
        'description': 'Foundation level'
    },
    'FUTD': {
        'name': 'Foundation Depth',
        'type': 'float',
        'default': 2000,
        'min': 1000,
        'max': 5000,
        'unit': 'mm',
        'description': 'Depth of foundation'
    },
    'FUTW': {
        'name': 'Foundation Width',
        'type': 'float',
        'default': 3000,
        'min': 2000,
        'max': 8000,
        'unit': 'mm',
        'description': 'Width of foundation'
    },
    'FUTL': {
        'name': 'Foundation Length',
        'type': 'float',
        'default': 8000,
        'min': 5000,
        'max': 20000,
        'unit': 'mm',
        'description': 'Length of foundation'
    },
    
    # Approach Slab Parameters
    'LASLAB': {
        'name': 'Approach Slab Length',
        'type': 'float',
        'default': 5000,
        'min': 2000,
        'max': 10000,
        'unit': 'mm',
        'description': 'Length of approach slab'
    },
    'APWTH': {
        'name': 'Approach Slab Width',
        'type': 'float',
        'default': 8000,
        'min': 5000,
        'max': 15000,
        'unit': 'mm',
        'description': 'Width of approach slab'
    },
    'APTHK': {
        'name': 'Approach Slab Thickness',
        'type': 'float',
        'default': 200,
        'min': 150,
        'max': 400,
        'unit': 'mm',
        'description': 'Thickness of approach slab'
    },
    'WCTH': {
        'name': 'Wearing Course Thickness',
        'type': 'float',
        'default': 75,
        'min': 50,
        'max': 150,
        'unit': 'mm',
        'description': 'Thickness of wearing course'
    },
    
    # Additional Parameters
    'RTL': {
        'name': 'Road Top Level',
        'type': 'float',
        'default': 110000,
        'min': 90000,
        'max': 150000,
        'unit': 'mm',
        'description': 'Top level of road surface'
    },
    'XINCR': {
        'name': 'X Direction Increment',
        'type': 'float',
        'default': 1000,
        'min': 100,
        'max': 5000,
        'unit': 'mm',
        'description': 'Chainage increment in X direction'
    },
    'YINCR': {
        'name': 'Y Direction Increment',
        'type': 'float',
        'default': 1000,
        'min': 100,
        'max': 5000,
        'unit': 'mm',
        'description': 'Elevation increment in Y direction'
    },
    'NOCH': {
        'name': 'Number of Chainages',
        'type': 'int',
        'default': 50,
        'min': 10,
        'max': 200,
        'unit': '',
        'description': 'Total number of chainages'
    }
}

PARAMETER_GROUPS = {
    'General': [
        'SCALE1', 'SCALE2', 'SKEW', 'DATUM', 'TOPRL', 'LEFT', 'RIGHT', 'RTL'
    ],
    'Bridge Geometry': [
        'NSPAN', 'LBRIDGE', 'SPAN1', 'CCBR', 'XINCR', 'YINCR', 'NOCH'
    ],
    'Slab Design': [
        'SLBTHC', 'SLBTHE', 'SLBTHT', 'SOFL', 'KERBW', 'KERBD', 'WCTH'
    ],
    'Abutments': [
        'ABTLEN', 'ABTL', 'ALCW', 'ALCD', 'ALFL', 'ARFL', 'ALFB', 'ALFBL', 'ALFBR',
        'ALTB', 'ALTBL', 'ALTBR', 'ALFO', 'ALFD', 'ALBB', 'ALBBL', 'ALBBR', 'DWTH'
    ],
    'Piers': [
        'CAPT', 'CAPB', 'CAPW', 'PIERTW', 'BATTR', 'PIERST', 'PIERN',
        'FUTRL', 'FUTD', 'FUTW', 'FUTL'
    ],
    'Approach': [
        'LASLAB', 'APWTH', 'APTHK'
    ]
}
