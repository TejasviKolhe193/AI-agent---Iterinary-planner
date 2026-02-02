#!/bin/bash

# Nomad Travel Planner - Setup Script
# This script helps you set up the travel planner application

echo "🌍 Nomad - AI Travel Planner Setup"
echo "===================================="
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 9) else 1)' 2>/dev/null; then
    echo "   ❌ Python 3.9+ is required. Please upgrade Python."
    exit 1
fi
echo "   ✅ Python version is compatible"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
if pip install -r requirements.txt; then
    echo "   ✅ Dependencies installed successfully"
else
    echo "   ❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Create .streamlit directory if it doesn't exist
echo "⚙️  Setting up configuration..."
if [ ! -d ".streamlit" ]; then
    mkdir .streamlit
    echo "   ✅ Created .streamlit directory"
fi

# Check if secrets.toml exists
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "   📝 Creating secrets.toml template..."
    cat > .streamlit/secrets.toml << 'EOF'
# Groq API Key
# Get your free API key at: https://console.groq.com
GROQ_API_KEY = "your_api_key_here"
EOF
    echo "   ✅ Created .streamlit/secrets.toml"
    echo ""
    echo "   ⚠️  IMPORTANT: Edit .streamlit/secrets.toml and add your Groq API key"
    echo "      Get your key at: https://console.groq.com"
else
    echo "   ✅ secrets.toml already exists"
fi
echo ""

echo "🎉 Setup complete!"
echo ""
echo "📖 Next steps:"
echo "   1. Get your Groq API key from https://console.groq.com"
echo "   2. Edit .streamlit/secrets.toml and add your API key"
echo "   3. Run the app with: streamlit run app.py"
echo ""
echo "📚 For detailed instructions, see README.md and USAGE_GUIDE.md"
echo ""
echo "Happy travels! ✈️"
