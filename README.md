# Nomad - AI Travel Planner ✈️

An intelligent travel itinerary planner powered by Groq's Llama 3-8B model, real-time web search, and Streamlit.

## 🌟 Features

- **Two-Stage AI Agent**:
  - **Stage A (Strategist)**: Analyzes your travel requirements and generates optimal search queries
  - **Stage B (Planner)**: Creates comprehensive, personalized itineraries using real-time data

- **Real-Time Web Search**: Uses DuckDuckGo to fetch current information about weather, events, and travel conditions

- **Comprehensive Itineraries**: Includes:
  - Trip overview (transportation, currency, language)
  - Accommodation recommendations
  - Day-by-day detailed itinerary
  - Budget breakdown
  - Packing and safety tips

- **Customizable**: Supports different budgets, travel groups, and trip durations

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Groq API key (get one free at [console.groq.com](https://console.groq.com))

### Installation

1. **Clone or download this project**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up your Groq API key** (choose one method):

   **Option A: Using Streamlit Secrets (Recommended for deployment)**
   
   Create `.streamlit/secrets.toml`:
   ```toml
   GROQ_API_KEY = "your-groq-api-key-here"
   ```

   **Option B: Enter in the app**
   
   Simply enter your API key in the sidebar when running the app.

4. **Run the application**:
```bash
streamlit run app.py
```

5. **Open your browser** to the URL shown in the terminal (usually `http://localhost:8501`)

## 📖 Usage

1. **Enter Travel Details**:
   - Destination (e.g., "Paris, France")
   - Date of travel
   - Duration (1-10 days)

2. **Set Preferences**:
   - Budget level (Student/Budget, Mid-Range, Luxury)
   - Travel group (Solo, Couple, Family, Friends)

3. **Click "Plan My Trip"**:
   - The AI will search for real-time information
   - Generate a personalized itinerary
   - Display results instantly

4. **Download Your Itinerary**:
   - Click the download button to save as Markdown

## 🏗️ Architecture

### Two-Stage Agent Logic

```
User Input → Stage A (Strategist) → Search Query
                                         ↓
                                   Web Search (DuckDuckGo)
                                         ↓
Real-time Data → Stage B (Planner) → Final Itinerary
```

### Technology Stack

- **LLM**: Groq API with Llama 3-8B-8192 model
- **Search**: DuckDuckGo Search API
- **Frontend**: Streamlit
- **Language**: Python 3.9+

## 📁 Project Structure

```
nomad-travel-planner/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .streamlit/
    └── secrets.toml   # API key configuration (create this)
```

## 🔧 Configuration

### Streamlit Secrets

Create `.streamlit/secrets.toml`:

```toml
GROQ_API_KEY = "gsk_your_api_key_here"
```

### Environment Variables

Alternatively, you can set environment variables:

```bash
export GROQ_API_KEY="your-api-key-here"
```

## 🎯 Key Functions

### `search_web(query)`
- Searches DuckDuckGo for real-time travel information
- Returns formatted results or fallback message
- Handles errors gracefully

### `get_search_query(client, ...)`
- **Stage A**: Uses LLM to generate optimal search query
- Considers destination, dates, budget, and travel group
- Returns focused search string

### `generate_itinerary(client, ..., search_data)`
- **Stage B**: Creates comprehensive itinerary
- Combines user inputs with real-time search data
- Formats output in structured Markdown

## 📋 Sample Output Sections

1. **Trip Overview**: Transportation, currency, language basics
2. **Accommodation**: Area recommendations with pricing
3. **Daily Itinerary**: Hour-by-hour breakdown for each day
4. **Budget Breakdown**: Detailed cost estimates
5. **Packing & Safety**: Weather-appropriate tips and warnings

## 🛡️ Error Handling

The app includes comprehensive error handling for:
- Missing API keys
- Failed web searches
- LLM API errors
- Invalid user inputs

## 🚀 Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Connect your repo to [Streamlit Community Cloud](https://streamlit.io/cloud)
3. Add `GROQ_API_KEY` to your app's secrets
4. Deploy!

### Local Network

```bash
streamlit run app.py --server.address 0.0.0.0
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Groq](https://groq.com) for ultra-fast LLM inference
- [DuckDuckGo](https://duckduckgo.com) for privacy-focused search
- [Streamlit](https://streamlit.io) for the amazing web framework
- [Meta AI](https://ai.meta.com) for Llama 3 model

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check the [Streamlit documentation](https://docs.streamlit.io)
- Visit [Groq documentation](https://console.groq.com/docs)

---

**Happy Travels!** 🌍✈️🎒
