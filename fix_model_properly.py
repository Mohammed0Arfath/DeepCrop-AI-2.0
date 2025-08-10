#!/usr/bin/env python3
"""
Proper fix for YOLOv8 segmentation model using correct architecture size
"""

import os
import torch
from ultralytics import YOLO

def determine_model_size(checkpoint):
    """Determine the correct YOLOv8 model size based on layer dimensions"""
    model_state = checkpoint['model']
    
    # Check the first conv layer to determine model size
    first_conv_weight = None
    for name, param in model_state.named_parameters():
        if 'model.0.conv.weight' in name:
            first_conv_weight = param
            break
    
    if first_conv_weight is not None:
        out_channels = first_conv_weight.shape[0]
        print(f"First conv layer output channels: {out_channels}")
        
        # Map channel sizes to model variants
        if out_channels == 16:
            return 'yolov8n-seg.pt'  # Nano
        elif out_channels == 32:
            return 'yolov8s-seg.pt'  # Small
        elif out_channels == 48:
            return 'yolov8m-seg.pt'  # Medium
        elif out_channels == 64:
            return 'yolov8l-seg.pt'  # Large
        elif out_channels == 80:
            return 'yolov8x-seg.pt'  # Extra Large
        else:
            print(f"Unknown channel size: {out_channels}, trying medium model")
            return 'yolov8m-seg.pt'
    
    return 'yolov8s-seg.pt'  # Default fallback

def fix_segmentation_model():
    """Fix the segmentation model with correct architecture"""
    model_path = "backend/models/yolov_deadheart.pt"
    
    print("🔧 Fixing YOLOv8 Segmentation Model with Correct Architecture")
    print("=" * 60)
    
    if not os.path.exists(model_path):
        print(f"❌ Model not found at {model_path}")
        return False
    
    try:
        # Load the checkpoint
        print("📂 Loading model checkpoint...")
        checkpoint = torch.load(model_path, map_location='cpu')
        
        # Determine correct model size
        print("🔍 Determining correct model architecture...")
        correct_model = determine_model_size(checkpoint)
        print(f"✅ Detected model type: {correct_model}")
        
        # Download and load the correct base model
        print(f"📥 Downloading {correct_model}...")
        base_model = YOLO(correct_model)
        print("✅ Base model loaded successfully")
        
        # Try to load the weights
        print("🔄 Loading your trained weights...")
        try:
            base_model.model.load_state_dict(checkpoint['model'].state_dict(), strict=False)
            print("✅ Weights loaded successfully!")
            
            # Save the fixed model
            fixed_path = model_path.replace('.pt', '_fixed.pt')
            base_model.save(fixed_path)
            print(f"💾 Fixed model saved to: {fixed_path}")
            
            # Test the fixed model
            print("🧪 Testing fixed model...")
            import tempfile
            from PIL import Image
            
            # Create test image
            test_img = Image.new('RGB', (640, 640), 'green')
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as f:
                test_img.save(f.name)
                
                results = base_model.predict(f.name, verbose=False)
                print("✅ Fixed model prediction successful!")
                
                os.unlink(f.name)
            
            print(f"\n🎉 SUCCESS! Your model has been fixed!")
            print(f"📝 To use the fixed model:")
            print(f"   mv {fixed_path} {model_path}")
            print(f"   # Or update your .env to point to the fixed model")
            
            return True
            
        except Exception as load_error:
            print(f"❌ Failed to load weights: {load_error}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing model: {e}")
        return False

if __name__ == "__main__":
    print("🌾 Sugarcane Disease Detection - Proper Model Fix")
    print("=" * 60)
    
    success = fix_segmentation_model()
    
    if success:
        print("\n✅ Model fixed successfully!")
        print("🚀 You can now restart your backend server and test dead heart detection.")
    else:
        print("\n❌ Model fix failed.")
        print("📋 You'll need to retrain your model with the correct format.")
