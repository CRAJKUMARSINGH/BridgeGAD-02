import requests
import json

def test_bridge_app_api():
    """Test the Bridge Flask application API"""
    
    # Sample bridge parameters
    sample_params = {
        'LBRIDGE': 30000,
        'NSPAN': 1,
        'TOPRL': 110000,
        'SOFL': 108000,
        'LEFT': 0,
        'ABTLEN': 10000,
        'ALFL': 105000,
        'ARFL': 105000,
        'SCALE1': 100,
        'SCALE2': 1,
        'CCBR': 50,
        'SKEW': 0,
        'KERBW': 1000,
        'KERBD': 500,
        'SLBTHC': 300,
        'SLBTHE': 250,
        'SLBTHT': 150,
        'PIERTW': 1500,
        'BATTR': 12,
        'PIERST': 10000,
        'SPAN1': 15000,
        'SPAN2': 15000,
        'FUTD': 1000,
        'FUTW': 3000,
        'FUTL': 5000,
        'DWTH': 500,
        'ALCW': 2000,
        'ALCD': 500,
        'ALFB': 6000,
        'ALFBL': 101500,
        'ALTB': 12000,
        'ALTBL': 100500,
        'ALFO': 1000,
        'ALFD': 1000,
        'ALBB': 6000,
        'ALBBL': 101500
    }
    
    base_url = "http://127.0.0.1:5000"
    
    try:
        # Test if app is running
        response = requests.get(base_url, timeout=5)
        print(f"✓ App is running: {response.status_code}")
        
        # Test generating DXF
        print("\\nTesting DXF generation...")
        response = requests.post(f"{base_url}/generate", data=sample_params, timeout=30)
        
        if response.status_code == 200:
            # Save the DXF file
            output_file = "C:/Users/Rajkumar/BridgeGAD-02/OUTPUT_01_16092025/test_bridge_output.dxf"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            print(f"✓ DXF generated successfully: {output_file}")
            print(f"File size: {len(response.content)} bytes")
        else:
            print(f"✗ Error generating DXF: {response.status_code}")
            print(response.text)
        
        # Test preview functionality
        print("\\nTesting preview functionality...")
        response = requests.post(f"{base_url}/preview", data=sample_params, timeout=15)
        if response.status_code == 200:
            print("✓ Preview generated successfully")
        else:
            print(f"✗ Error generating preview: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to the application. Make sure it's running on http://127.0.0.1:5000")
    except Exception as e:
        print(f"✗ Error testing application: {e}")

if __name__ == "__main__":
    test_bridge_app_api()