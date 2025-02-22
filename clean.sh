find . -name "__pycache__" -type d -exec rm -rf {} +

find . -name "*.pyc" -delete
find . -name "*.pyo" -delete

echo "cleaned cache"
