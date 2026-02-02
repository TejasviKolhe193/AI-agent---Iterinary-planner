# Usage Guide - Nomad AI Travel Planner

## Getting Started

### Step 1: Installation

```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 2: Get Your Groq API Key

1. Visit [console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_...`)

### Step 3: Configure API Key

**Method A: Using Streamlit Secrets (Recommended)**

1. Create directory: `.streamlit/` in your project root
2. Create file: `.streamlit/secrets.toml`
3. Add your key:
```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

**Method B: Enter in App**

Simply paste your API key in the sidebar when the app is running.

### Step 4: Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Using the Travel Planner

### Input Fields Explained

#### 🌍 Travel Details

**Destination**
- Format: "City, Country" (e.g., "Tokyo, Japan")
- Be specific for better results
- Can include regions (e.g., "Amalfi Coast, Italy")

**Date of Travel**
- Pick your departure date
- Affects seasonal recommendations and weather info
- Used to search for events during your visit

**Duration**
- Number of days you'll stay
- Range: 1-10 days
- Affects depth of itinerary

#### 💰 Preferences

**Budget Level**
- **Student/Budget**: Hostels, street food, free activities
- **Mid-Range**: 3-star hotels, casual dining, paid attractions
- **Luxury**: 5-star hotels, fine dining, premium experiences

**Travel Group**
- **Solo**: Individual traveler, freedom-focused
- **Couple**: Romantic spots, intimate experiences
- **Family**: Kid-friendly, safe, educational
- **Friends**: Social activities, nightlife, adventures

## Understanding the Output

### 1. Trip Overview Section

You'll get:
- **Transportation**: How to reach your destination (flights, trains)
- **Currency**: Local currency and exchange tips
- **Language**: Essential phrases to know
- **Weather**: What to expect during your dates

### 2. Accommodation Recommendations

Based on your budget:
- Specific neighborhoods or hotel names
- Price ranges per night
- Proximity to attractions
- Local character of each area

### 3. Daily Itinerary

For each day of your trip:
- **Morning**: Activities with timing (e.g., 9 AM - 12 PM)
- **Afternoon**: Activities with timing (e.g., 1 PM - 5 PM)
- **Evening**: Activities with timing (e.g., 6 PM - 10 PM)
- **Dining**: Restaurant recommendations or areas

Mix of:
- Popular tourist attractions
- Hidden gems and local favorites
- Dining recommendations
- Transportation between spots

### 4. Budget Breakdown

Estimated costs for:
- Accommodation (per night × total nights)
- Food (breakfast, lunch, dinner per day)
- Transportation (local + airport)
- Activities (entry fees, tours)
- **Total** with safety buffer

### 5. Packing & Safety

- **Weather-appropriate clothing** for your travel dates
- **Tourist trap alerts**: Common scams to avoid
- **Safety tips**: Emergency numbers, safe areas
- **Essential items**: Adapters, medications, etc.

## How the AI Agent Works

### Two-Stage Process

#### Stage A: The Strategist 🧠

1. Analyzes your travel requirements
2. Determines what real-time info is most valuable
3. Generates a focused search query
4. Example: "Paris December 2024 weather Christmas events"

You'll see this query displayed in the status panel.

#### Stage B: The Planner ✨

1. Takes the search results
2. Combines with your preferences
3. Generates a comprehensive itinerary
4. Formats everything in readable Markdown

### Real-Time Search

Uses DuckDuckGo to find:
- Current weather forecasts
- Upcoming events and festivals
- Travel advisories
- Seasonal pricing information
- Recent traveler experiences

## Tips for Best Results

### 1. Be Specific with Destinations

❌ "Europe"
✅ "Barcelona, Spain"

❌ "Asia"
✅ "Kyoto, Japan"

### 2. Choose Realistic Durations

- 1-3 days: City breaks
- 4-6 days: Explore a city thoroughly
- 7-10 days: Multiple cities or regions

### 3. Match Budget to Expectations

- **Budget**: $30-50/day
- **Mid-Range**: $100-200/day
- **Luxury**: $300+/day

### 4. Consider Your Group

- **Solo**: Flexibility in timing, solo activities
- **Couple**: Romantic settings considered
- **Family**: Kid-friendly with safety focus
- **Friends**: Group activities and social spots

## Downloading Your Itinerary

1. After generation, find the "Download Itinerary" button
2. Click to download as `.md` (Markdown) file
3. Open with any text editor
4. Or use Markdown viewers for formatted view

### Markdown Viewers

- **VS Code**: Built-in preview
- **Obsidian**: Great for travel planning
- **Notion**: Import Markdown files
- **Online**: dillinger.io, stackedit.io

## Troubleshooting

### "Please provide a Groq API key"

**Solution**: Add your API key in sidebar or secrets.toml

### "Search encountered an issue"

**Solution**: App will continue with general knowledge. Try:
- Running again (temporary network issue)
- Checking internet connection
- Using a different destination search

### "Error generating itinerary"

**Solutions**:
- Check API key is valid
- Ensure you have Groq API credits
- Try shorter duration or simpler destination
- Check error message for specifics

### Slow Performance

**Normal**: First query of a session may take 10-15 seconds
**Tips**:
- Groq is usually very fast (1-2 seconds)
- Web search adds 2-5 seconds
- Complex itineraries (10 days) take longer

## Advanced Usage

### Regenerating Itineraries

1. Change any input parameter
2. Click "Plan My Trip" again
3. New itinerary overwrites the old one

### Comparing Options

1. Generate itinerary for "Mid-Range" budget
2. Download it
3. Change to "Luxury" budget
4. Generate again and compare

### Multi-City Trips

For now, run separate queries:
1. "Paris, France" - 3 days
2. "Amsterdam, Netherlands" - 3 days
3. Combine downloaded itineraries manually

## Privacy & Data

- No user data is stored permanently
- API calls are encrypted (HTTPS)
- Search queries are anonymous via DuckDuckGo
- Session state cleared on browser close

## Best Practices

### 1. Plan Ahead

Run queries 2-4 weeks before travel for:
- Better accommodation availability
- Time to book flights
- Preparation for visas/documents

### 2. Cross-Reference

Use the itinerary as a starting point:
- Verify current hours of attractions
- Book tours/tickets in advance
- Check restaurant reservations

### 3. Customize Further

The AI gives you a framework:
- Swap activities you're not interested in
- Add personal interests
- Adjust timing to your pace

### 4. Local Insights

Once at destination:
- Ask locals for current recommendations
- Check if events/festivals changed
- Adapt to weather if needed

## Example Use Cases

### Weekend City Break
- Duration: 2-3 days
- Budget: Mid-Range
- Group: Couple
- Focus: Top attractions + food scene

### Family Vacation
- Duration: 7 days
- Budget: Mid-Range
- Group: Family
- Focus: Kid-friendly, educational, safe

### Backpacking Adventure
- Duration: 10 days
- Budget: Student/Budget
- Group: Solo or Friends
- Focus: Hostels, street food, free activities

### Luxury Getaway
- Duration: 4-5 days
- Budget: Luxury
- Group: Couple
- Focus: 5-star hotels, fine dining, spa

## Feedback & Improvement

The app gets better with use! If something doesn't work:

1. Note what went wrong
2. Try adjusting your inputs
3. Report issues (if sharing publicly)
4. Suggest features you'd like to see

## Next Steps After Planning

1. ✅ Review the itinerary thoroughly
2. 📅 Book flights and accommodation
3. 🎫 Pre-book popular attractions
4. 💳 Notify bank of travel plans
5. 📱 Download offline maps
6. 💉 Check visa/vaccination requirements
7. 📦 Start packing based on the guide

---

**Happy Planning!** Your adventure awaits! 🌍✈️
