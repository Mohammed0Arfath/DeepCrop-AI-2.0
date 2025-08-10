#!/usr/bin/env python3
"""
Test script to isolate the segmentation issue
"""

import sys
import os
sys.path.append('backend')

from ultralytics import YOLO
import tempfile
from PIL import Image
import numpy as np

def test_segmentation_model():
    """Test the dead heart segmentation model directly"""
    
    print("🔍 Testing Dead Heart Segmentation Model...")
    
    # Load model
    model_path = "backend/models/yolov_deadheart.pt"
    if not os.path.exists(model_path):
        print(f"❌ Model not found at {model_path}")
        return False
    
    try:
        model = YOLO(model_path)
        print(f"✅ Model loaded successfully")
        print(f"   Model task: {model.task}")
        print(f"   Model type: {type(model)}")
        
        # Create a test image
        test_image = Image.new('RGB', (640, 640), color='green')
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            test_image.save(temp_file.name)
            temp_path = temp_file.name
        
        print(f"📸 Created test image: {temp_path}")
        
        # Test prediction
        print("🚀 Running prediction...")
        results = model.predict(source=temp_path, verbose=True)
        
        print(f"✅ Prediction successful!")
        print(f"   Results type: {type(results)}")
        print(f"   Number of results: {len(results)}")
        
        # Examine first result
        if results:
            result = results[0]
            print(f"   First result type: {type(result)}")
            print(f"   Result attributes: {[attr for attr in dir(result) if not attr.startswith('_')]}")
            
            # Check for masks
            if hasattr(result, 'masks') and result.masks is not None:
                print(f"   ✅ Has masks: {type(result.masks)}")
                print(f"   Masks attributes: {[attr for attr in dir(result.masks) if not attr.startswith('_')]}")
                
                # Check masks data
                if hasattr(result.masks, 'data'):
                    masks_data = result.masks.data
                    print(f"   Masks data shape: {masks_data.shape}")
                
                # Check masks xy
                if hasattr(result.masks, 'xy'):
                    masks_xy = result.masks.xy
                    print(f"   Masks XY type: {type(masks_xy)}")
                    print(f"   Masks XY length: {len(masks_xy) if masks_xy else 0}")
            else:
                print("   ❌ No masks found")
            
            # Check for boxes
            if hasattr(result, 'boxes') and result.boxes is not None:
                print(f"   ✅ Has boxes: {type(result.boxes)}")
                if hasattr(result.boxes, 'conf'):
                    scores = result.boxes.conf
                    print(f"   Confidence scores: {scores}")
            else:
                print("   ❌ No boxes found")
        
        # Clean up
        os.unlink(temp_path)
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_segmentation_model()
    if success:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n💥 Test failed!")
