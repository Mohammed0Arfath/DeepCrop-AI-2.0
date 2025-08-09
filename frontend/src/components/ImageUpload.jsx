/**
 * MIT License
 * 
 * Image upload component with preview functionality
 */

import React, { useRef, useState } from 'react';

const ImageUpload = ({ onImageUpload, imagePreview }) => {
  const fileInputRef = useRef(null);
  const [dragOver, setDragOver] = useState(false);

  // Handle file selection
  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        onImageUpload(file, e.target.result);
      };
      reader.readAsDataURL(file);
    } else {
      alert('Please select a valid image file (JPEG, PNG, etc.)');
    }
  };

  // Handle file input change
  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  // Handle drag and drop
  const handleDragOver = (e) => {
    e.preventDefault();
    setDragOver(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelect(files[0]);
    }
  };

  // Trigger file input click
  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="image-upload">
      <h2>Upload Sugarcane Image</h2>
      <p>Upload a clear image of the sugarcane plant for analysis:</p>
      
      <div
        className={`upload-area ${dragOver ? 'drag-over' : ''} ${imagePreview ? 'has-image' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        
        {imagePreview ? (
          <div className="image-preview">
            <img src={imagePreview} alt="Uploaded sugarcane" />
            <div className="image-overlay">
              <p>Click to change image</p>
            </div>
          </div>
        ) : (
          <div className="upload-placeholder">
            <div className="upload-icon">📷</div>
            <h3>Drop image here or click to upload</h3>
            <p>Supports JPEG, PNG, and other image formats</p>
            <p className="upload-hint">
              💡 <strong>Tip:</strong> Use clear, well-lit images for best results
            </p>
          </div>
        )}
      </div>
      
      {imagePreview && (
        <div className="image-info">
          <p>✅ Image uploaded successfully</p>
        </div>
      )}
    </div>
  );
};

export default ImageUpload;
