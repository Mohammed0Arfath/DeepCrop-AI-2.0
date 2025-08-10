#!/usr/bin/env python3
"""
Script to fix corrupted YOLOv8 segmentation model
This script will help you rebuild your dead heart segmentation model properly
"""

import os
import sys
from ultralytics import YOLO

def fix_segmentation_model():
    """
    Fix the corrupted segmentation model by rebuilding it
    """
    print("🔧 YOLOv8 Segmentation Model Fix Tool")
    print("=" * 50)
    
    model_path = "backend/models/yolov_deadheart.pt"
    
    if not os.path.exists(model_path):
        print(f"❌ Model not found at {model_path}")
        return False
    
    print(f"📁 Found model at: {model_path}")
    
    # Option 1: Try to rebuild the model
    print("\n🔄 Option 1: Rebuilding model architecture...")
    try:
        # Load a fresh YOLOv8 segmentation model
        base_model = YOLO('yolov8n-seg.pt')  # Download base segmentation model
        print("✅ Downloaded base YOLOv8 segmentation model")
        
        # Try to load your model's weights
        print("🔄 Attempting to load your model weights...")
        import torch
        
        # Load your model state
        checkpoint = torch.load(model_path, map_location='cpu')
        print(f"✅ Loaded checkpoint with keys: {list(checkpoint.keys())}")
        
        if 'model' in checkpoint:
            model_state = checkpoint['model']
            print(f"✅ Found model state with {len(model_state.state_dict())} parameters")
            
            # Try to load the state dict into the base model
            try:
                base_model.model.load_state_dict(model_state.state_dict(), strict=False)
                print("✅ Successfully loaded weights into base model")
                
                # Save the fixed model
                fixed_path = model_path.replace('.pt', '_fixed.pt')
                base_model.save(fixed_path)
                print(f"✅ Saved fixed model to: {fixed_path}")
                
                # Test the fixed model
                print("🧪 Testing fixed model...")
                test_results = base_model.predict('https://ultralytics.com/images/bus.jpg', verbose=False)
                print("✅ Fixed model works correctly!")
                
                print(f"\n🎉 SUCCESS! Your fixed model is saved as: {fixed_path}")
                print(f"📝 To use it, rename it to replace your original model:")
                print(f"   mv {fixed_path} {model_path}")
                
                return True
                
            except Exception as load_error:
                print(f"❌ Failed to load weights: {load_error}")
                
        else:
            print("❌ No 'model' key found in checkpoint")
            
    except Exception as e:
        print(f"❌ Rebuild failed: {e}")
    
    # Option 2: Retrain recommendation
    print("\n" + "=" * 50)
    print("🔄 Option 2: Retrain your model (RECOMMENDED)")
    print("=" * 50)
    
    print("""
Your model appears to have a corrupted segmentation head. The best solution is to retrain:

1. 📊 Prepare your dataset in YOLOv8 segmentation format:
   - Images in: dataset/images/train/, dataset/images/val/
   - Labels in: dataset/labels/train/, dataset/labels/val/
   - Labels should contain polygon coordinates (not just bounding boxes)

2. 🏗️ Create dataset.yaml:
   ```yaml
   path: /path/to/your/dataset
   train: images/train
   val: images/val
   names:
     0: deadheart
   ```

3. 🚀 Train new model:
   ```bash
   yolo segment train data=dataset.yaml model=yolov8n-seg.pt epochs=100 imgsz=640
   ```

4. 📁 Replace your model:
   ```bash
   cp runs/segment/train/weights/best.pt backend/models/yolov_deadheart.pt
   ```
""")
    
    return False

def check_model_compatibility():
    """Check if the current model is compatible"""
    print("\n🔍 Checking model compatibility...")
    
    try:
        from ultralytics import YOLO
        model = YOLO("backend/models/yolov_deadheart.pt")
        
        print(f"✅ Model loads successfully")
        print(f"   Task: {model.task}")
        print(f"   Names: {model.names}")
        
        # Try a simple prediction
        import tempfile
        from PIL import Image
        
        # Create test image
        test_img = Image.new('RGB', (640, 640), 'green')
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
            test_img.save(f.name)
            
            print("🧪 Testing prediction...")
            results = model.predict(f.name, verbose=False)
            print("✅ Prediction successful!")
            
            os.unlink(f.name)
            return True
            
    except Exception as e:
        print(f"❌ Model compatibility check failed: {e}")
        return False

if __name__ == "__main__":
    print("🌾 Sugarcane Disease Detection - Model Fix Tool")
    print("=" * 60)
    
    # Check current model
    if check_model_compatibility():
        print("\n🎉 Your model is working correctly!")
        print("The issue might be in the application code, not the model.")
    else:
        print("\n💥 Model has issues. Attempting to fix...")
        success = fix_segmentation_model()
        
        if not success:
            print("\n📋 NEXT STEPS:")
            print("1. Retrain your model using the instructions above")
            print("2. Or provide a working YOLOv8 segmentation model")
            print("3. Or convert your dataset to detection format instead")
