#!/bin/bash

# Example curl request for testing the sugarcane disease detection API
# Make sure the backend is running on localhost:8000

# Set the API endpoint
API_URL="http://localhost:8000"

# Example 1: Test dead heart disease detection
echo "Testing dead heart disease detection..."
curl -X POST "${API_URL}/predict/deadheart" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@sample_image.jpg" \
  -F "questions=$(cat sample_questions.json)" \
  | jq '.'

echo -e "\n" 

# Example 2: Test tiller disease detection
echo "Testing tiller disease detection..."
curl -X POST "${API_URL}/predict/tiller" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@sample_image.jpg" \
  -F "questions=$(cat sample_questions.json)" \
  | jq '.'

echo -e "\n"

# Example 3: Test health endpoint
echo "Testing health endpoint..."
curl -X GET "${API_URL}/health" | jq '.'

echo -e "\n"

# Instructions for use:
echo "Instructions:"
echo "1. Make sure you have a sample image file named 'sample_image.jpg' in this directory"
echo "2. Make sure the backend server is running on localhost:8000"
echo "3. Install jq for pretty JSON output: brew install jq (macOS) or apt-get install jq (Ubuntu)"
echo "4. Run this script: bash example_curl_request.sh"
