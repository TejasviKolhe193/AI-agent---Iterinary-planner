# Technical Documentation - Nomad AI Travel Planner

## Architecture Overview

### System Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│  (User Interface + Session State Management)                 │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                  Two-Stage Agent Pipeline                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Stage A: Strategist                                         │
│  ┌──────────────────────────────────────────┐              │
│  │ Input: User travel requirements           │              │
│  │ Process: LLM generates search query       │              │
│  │ Output: Optimized search string           │              │
│  └──────────────┬───────────────────────────┘              │
│                  │                                            │
│                  ▼                                            │
│  ┌──────────────────────────────────────────┐              │
│  │      DuckDuckGo Web Search API           │              │
│  │  (Fetches real-time travel information)  │              │
│  └──────────────┬───────────────────────────┘              │
│                  │                                            │
│                  ▼                                            │
│  Stage B: Planner                                            │
│  ┌──────────────────────────────────────────┐              │
│  │ Input: User requirements + Search data    │              │
│  │ Process: LLM generates itinerary          │              │
│  │ Output: Formatted Markdown itinerary      │              │
│  └──────────────────────────────────────────┘              │
│                                                               │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              External Services                                │
├─────────────────────────────────────────────────────────────┤
│  • Groq API (Llama 3-8B-8192)                               │
│  • DuckDuckGo Search                                         │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. `search_web(query)` Function

**Purpose**: Fetch real-time travel information from the web.

**Parameters**:
- `query` (str): Search query string

**Returns**:
- `str`: Formatted search results or fallback message

**Implementation Details**:
```python
def search_web(query):
    try:
        results = DDGS().text(query, max_results=4)
        # Format and return results
    except Exception as e:
        # Graceful fallback
```

**Error Handling**:
- Catches all exceptions
- Provides user-friendly warnings
- Returns fallback message instead of failing
- Logs issues without breaking the flow

**Performance**:
- Typical response time: 2-5 seconds
- Returns top 4 results for relevance
- Extracts title and body from each result

### 2. `get_search_query()` Function

**Purpose**: Stage A - Generate optimal search query using LLM.

**Parameters**:
- `client`: Groq client instance
- `destination`: Travel destination string
- `date_of_travel`: datetime object
- `duration`: Number of days (int)
- `budget_level`: Budget category string
- `travel_group`: Group type string

**Returns**:
- `str`: Optimized search query

**LLM Configuration**:
```python
model="llama3-8b-8192"
temperature=0.7      # Balanced creativity
max_tokens=100       # Short, focused queries
```

**Prompt Engineering**:
- Clear role definition: "travel research assistant"
- Specific task: Generate ONE search query
- Context: Full travel details provided
- Output format: Plain text query only
- Focus areas: Weather, events, advisories, pricing

**Fallback Behavior**:
- If LLM fails, generates basic query
- Format: "{destination} travel guide {month} weather events"

### 3. `generate_itinerary()` Function

**Purpose**: Stage B - Create comprehensive travel itinerary.

**Parameters**:
- `client`: Groq client instance
- User travel parameters (destination, date, duration, budget, group)
- `search_data`: Real-time information from web search

**Returns**:
- `str`: Complete Markdown-formatted itinerary

**LLM Configuration**:
```python
model="llama3-8b-8192"
temperature=0.8      # More creative for variety
max_tokens=4000      # Long-form content
```

**Prompt Structure**:
1. Role definition: "expert travel planner"
2. User requirements section
3. Real-time data injection
4. Detailed output structure requirements
5. Specific Markdown formatting instructions

**Output Sections** (enforced via prompt):
1. Trip Overview
2. Accommodation Recommendations
3. Daily Itinerary (day-by-day)
4. Budget Breakdown
5. Packing & Safety Tips

## Data Flow

### Request Lifecycle

```
1. User Inputs
   ↓
2. Validation
   ↓
3. Groq Client Initialization
   ↓
4. Stage A: get_search_query()
   ├→ LLM Call #1 (Query generation)
   └→ Search Query String
   ↓
5. search_web()
   ├→ DuckDuckGo API Call
   └→ Formatted Search Results
   ↓
6. Stage B: generate_itinerary()
   ├→ LLM Call #2 (Itinerary generation)
   └→ Complete Itinerary
   ↓
7. Display & Download
```

### Session State Management

```python
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None
```

**Purpose**:
- Persist itinerary across reruns
- Allow UI updates without regeneration
- Enable download functionality

**Lifecycle**:
- Initialized on first load
- Updated after successful generation
- Persists until browser close/refresh
- Cleared manually via New Trip button

## API Integration

### Groq API

**Endpoint**: Chat Completions
**Model**: `llama3-8b-8192`

**Authentication**:
```python
client = Groq(api_key=api_key)
```

**Request Format**:
```python
response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."}
    ],
    temperature=0.7,
    max_tokens=1000
)
```

**Rate Limits** (Free Tier):
- 30 requests per minute
- 14,400 tokens per minute

**Error Handling**:
- API key validation
- Rate limit handling
- Network error recovery
- Graceful degradation

### DuckDuckGo Search API

**Library**: `duckduckgo-search`
**Class**: `DDGS`

**Usage**:
```python
from duckduckgo_search import DDGS

results = DDGS().text(query, max_results=4)
```

**Response Format**:
```python
[
    {
        "title": "Article Title",
        "body": "Description text...",
        "href": "https://example.com"
    },
    ...
]
```

**No API Key Required**: Anonymous, privacy-focused

## Streamlit Configuration

### Page Config

```python
st.set_page_config(
    page_title="Nomad - AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)
```

### Custom CSS

Applied via `st.markdown()` with `unsafe_allow_html=True`:
- Custom title styling
- Subtitle formatting
- Improved visual hierarchy

### Secrets Management

**Development**:
```toml
# .streamlit/secrets.toml
GROQ_API_KEY = "gsk_..."
```

**Production** (Streamlit Cloud):
- Add secrets via dashboard
- Environment variable injection
- Automatic encryption

**Access**:
```python
api_key = st.secrets["GROQ_API_KEY"]
```

## Error Handling Strategy

### Levels of Error Handling

**1. Input Validation**:
```python
if not destination:
    st.error("Please enter a destination!")
    return
```

**2. API Key Validation**:
```python
if not api_key:
    st.warning("Please provide a Groq API key...")
    return
```

**3. Try-Except Blocks**:
```python
try:
    # API calls
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.code(traceback.format_exc())
```

**4. Graceful Degradation**:
- Search fails → Use general knowledge
- LLM slow → Show spinner
- Network issues → Retry logic

## Performance Optimization

### Response Times

**Target**: < 15 seconds total
**Breakdown**:
- Stage A LLM: 1-2 seconds
- Web Search: 2-5 seconds
- Stage B LLM: 5-8 seconds
- UI Rendering: < 1 second

### Optimization Techniques

1. **Efficient Prompts**:
   - Concise system messages
   - Clear output requirements
   - Minimal token usage in Stage A

2. **Parallel Processing Potential**:
   ```python
   # Future enhancement: Run multiple searches
   # with concurrent.futures.ThreadPoolExecutor()
   ```

3. **Caching**:
   ```python
   # Future: Use @st.cache_data for repeated searches
   @st.cache_data(ttl=3600)
   def search_web(query):
       # ...
   ```

## Security Considerations

### API Key Protection

**Best Practices**:
- Never commit secrets to git
- Use `.gitignore` for secrets.toml
- Environment variables in production
- Streamlit secrets in deployment

**.gitignore**:
```
.streamlit/secrets.toml
.env
*.pyc
__pycache__/
```

### Input Sanitization

**Current**:
- Streamlit handles basic XSS
- No SQL injection risk (no database)
- File downloads use safe MIME types

**Future Enhancements**:
- Rate limiting per user
- Input length validation
- Suspicious pattern detection

## Testing Strategy

### Manual Testing Checklist

**Functional Tests**:
- [ ] All input fields accept valid data
- [ ] API key validation works
- [ ] Search functionality returns results
- [ ] Itinerary generation completes
- [ ] Download button works
- [ ] Error messages display correctly

**Edge Cases**:
- [ ] Empty destination input
- [ ] Invalid API key
- [ ] Network failure during search
- [ ] LLM timeout
- [ ] Very long durations (10 days)
- [ ] Obscure destinations

**UI/UX Tests**:
- [ ] Responsive design on mobile
- [ ] Loading states display
- [ ] Status updates show progress
- [ ] Download works on all browsers

### Automated Testing (Future)

```python
# Unit tests
def test_search_web():
    result = search_web("Paris travel")
    assert isinstance(result, str)
    assert len(result) > 0

# Integration tests
def test_full_pipeline():
    # Mock Groq API
    # Test complete flow
    pass
```

## Deployment Guide

### Streamlit Community Cloud

**Prerequisites**:
- GitHub repository
- Streamlit account

**Steps**:
1. Push code to GitHub
2. Connect repo to Streamlit Cloud
3. Add secrets in dashboard
4. Deploy

**Configuration**:
```toml
# .streamlit/config.toml
[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

### Docker Deployment

**Dockerfile** (future):
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

### Environment Variables

```bash
export GROQ_API_KEY="your-key"
streamlit run app.py
```

## Future Enhancements

### Planned Features

1. **Multi-City Support**:
   - Sequential itineraries
   - Travel time between cities
   - Transportation recommendations

2. **PDF Export**:
   - Better formatting than Markdown
   - Printable itineraries
   - Images and maps

3. **User Accounts**:
   - Save multiple itineraries
   - Favorite destinations
   - Trip history

4. **Real-Time Pricing**:
   - Flight price integration
   - Hotel availability checks
   - Activity booking links

5. **Map Integration**:
   - Folium or Google Maps
   - Plot daily routes
   - Distance calculations

6. **Collaborative Planning**:
   - Share itineraries
   - Multi-user editing
   - Comments and suggestions

### Technical Debt

1. Add comprehensive unit tests
2. Implement proper logging
3. Add monitoring/analytics
4. Optimize prompt templates
5. Implement caching layer
6. Add user feedback mechanism

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'groq'"
**Solution**: Run `pip install -r requirements.txt`

**Issue**: Slow performance
**Solution**: Check internet connection, Groq API status

**Issue**: Empty itinerary
**Solution**: Check API key, review error messages

**Issue**: Search fails repeatedly
**Solution**: DuckDuckGo might be rate-limiting, wait and retry

## Contributing Guidelines

### Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Comment complex logic

### Pull Request Process

1. Fork the repository
2. Create feature branch
3. Make changes with tests
4. Update documentation
5. Submit PR with description

### Areas for Contribution

- Additional search providers
- Enhanced prompt engineering
- UI/UX improvements
- Performance optimization
- Test coverage
- Documentation

## Resources

### Documentation Links

- [Streamlit Docs](https://docs.streamlit.io)
- [Groq API Docs](https://console.groq.com/docs)
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)
- [Llama 3 Model Card](https://github.com/meta-llama/llama3)

### Related Projects

- Streamlit Travel Apps
- LangChain Travel Agents
- CrewAI Multi-Agent Systems

---

**Version**: 1.0.0
**Last Updated**: January 2026
**Maintainer**: Open Source Community
