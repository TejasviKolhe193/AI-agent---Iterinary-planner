import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from datetime import datetime
import traceback

# Page configuration
st.set_page_config(
    page_title="Nomad - AI Travel Planner",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None


def search_web(query):
    """
    Search the web using DuckDuckGo and return formatted results.
    
    Args:
        query (str): Search query string
        
    Returns:
        str: Formatted search results or fallback message
    """
    try:
        # Perform the search
        results = DDGS().text(query, max_results=4)
        
        if not results:
            return "No specific search results found. Please provide general recommendations based on common knowledge."
        
        # Format the results
        formatted_results = []
        for idx, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            body = result.get('body', 'No description')
            formatted_results.append(f"**Result {idx}: {title}**\n{body}\n")
        
        return "\n".join(formatted_results)
    
    except Exception as e:
        st.warning(f"Search encountered an issue: {str(e)}")
        return "Search temporarily unavailable. Providing recommendations based on general travel knowledge."


def get_search_query(client, destination, date_of_travel, duration, budget_level, travel_group):
    """
    Stage A: The Strategist - Generate an effective search query.
    
    Args:
        client: Groq client instance
        destination, date_of_travel, duration, budget_level, travel_group: User inputs
        
    Returns:
        str: Search query string
    """
    # Format the date nicely
    travel_date = date_of_travel.strftime("%B %Y")
    
    strategist_prompt = f"""You are a travel research assistant. Based on the following travel request, write ONE effective search query to find the most important real-time information for this specific trip.

Travel Details:
- Destination: {destination}
- Travel Date: {travel_date}
- Duration: {duration} days
- Budget: {budget_level}
- Travel Group: {travel_group}

Focus your search on finding current information about:
- Weather conditions during the travel period
- Special events or festivals happening during that time
- Current travel advisories or important updates
- Seasonal pricing or deals

Output ONLY the search query string, nothing else."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful travel research assistant."},
                {"role": "user", "content": strategist_prompt}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        search_query = response.choices[0].message.content.strip()
        # Remove quotes if LLM added them
        search_query = search_query.strip('"').strip("'")
        return search_query
    
    except Exception as e:
        st.error(f"Error generating search query: {str(e)}")
        # Fallback search query
        return f"{destination} travel guide {travel_date} weather events"


def generate_itinerary(client, destination, date_of_travel, duration, budget_level, travel_group, search_data):
    """
    Stage B: The Planner - Generate the complete travel itinerary.
    
    Args:
        client: Groq client instance
        destination, date_of_travel, duration, budget_level, travel_group: User inputs
        search_data: Real-time search results
        
    Returns:
        str: Complete formatted itinerary in Markdown
    """
    travel_date = date_of_travel.strftime("%B %d, %Y")
    
    final_prompt = f"""You are an expert travel planner. Create a comprehensive and detailed travel itinerary based on the following information.

**User's Travel Request:**
- Destination: {destination}
- Travel Date: {travel_date}
- Duration: {duration} days
- Budget Level: {budget_level}
- Travel Group: {travel_group}

**Real-Time Information:**
{search_data}

**Instructions:**
Generate a complete travel itinerary in Markdown format with EXACTLY these sections:

# Trip to {destination}

## 1. Trip Overview
- **Transportation**: Best ways to reach {destination} (flights, trains, etc.) and estimated costs
- **Local Currency**: Currency name, current exchange rate tips, and best places to exchange money
- **Language**: Main language(s) spoken and 2-3 essential phrases (Hello, Thank you, How much?, etc.)
- **Best Time to Visit**: Brief note on weather during the travel period

## 2. Accommodation Recommendations
Based on the {budget_level} budget, suggest 2-3 specific areas or types of hotels/accommodations:
- Include area names and why they're good choices
- Estimated price range per night
- Proximity to main attractions

## 3. Daily Itinerary
Create a day-by-day breakdown for all {duration} days:

**Day 1: [Theme/Focus]**
- **Morning**: Specific activity or location with timing
- **Afternoon**: Specific activity or location with timing
- **Evening**: Specific activity or location with timing
- **Dining Suggestion**: Restaurant type or area for meals

[Repeat for each day, mixing tourist spots and hidden gems]

## 4. Budget Breakdown
Provide estimated costs in local currency and USD:
- **Accommodation**: Cost per night × {duration} nights
- **Food**: Daily budget for breakfast, lunch, dinner
- **Transportation**: Local transport, airport transfers
- **Activities**: Entry fees, tours, experiences
- **Total Estimated Cost**: Sum with buffer

## 5. Packing & Safety Tips
- **Weather-Appropriate Clothing**: What to pack based on the season
- **Tourist Trap Alerts**: 2-3 common scams or overpriced tourist traps to avoid
- **Safety Tips**: Local emergency numbers, safe areas, health precautions
- **Essential Items**: Must-have items for this specific destination

Make the itinerary practical, specific, and tailored to the {travel_group} group traveling on a {budget_level} budget. Include local insights and insider tips where possible."""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an experienced travel planner who creates detailed, practical itineraries."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        itinerary = response.choices[0].message.content
        return itinerary
    
    except Exception as e:
        st.error(f"Error generating itinerary: {str(e)}")
        raise


def main():
    # Header
    st.markdown('<h1 class="main-title">✈️ Nomad - AI Travel Planner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your intelligent travel companion powered by AI</p>', unsafe_allow_html=True)
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key_input = st.text_input(
            "Groq API Key",
            type="password",
            help="Enter your Groq API key or configure it in Streamlit secrets"
        )
        
        # Use API key from input or secrets
        if api_key_input:
            api_key = api_key_input
        elif "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
        else:
            api_key = None
        
        st.divider()
        
        st.markdown("""
        ### 📋 How it works:
        1. Enter your travel details
        2. AI searches for real-time info
        3. Get a personalized itinerary
        
        ### 🔑 API Key:
        Get your free Groq API key at [console.groq.com](https://console.groq.com)
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🌍 Travel Details")
        
        destination = st.text_input(
            "Destination",
            placeholder="e.g., Paris, France",
            help="Enter the city and country you want to visit"
        )
        
        date_of_travel = st.date_input(
            "Date of Travel",
            min_value=datetime.now(),
            help="When do you plan to travel?"
        )
        
        duration = st.slider(
            "Duration (days)",
            min_value=1,
            max_value=10,
            value=5,
            help="How many days will you stay?"
        )
    
    with col2:
        st.subheader("💰 Preferences")
        
        budget_level = st.selectbox(
            "Budget Level",
            options=["Student/Budget", "Mid-Range", "Luxury"],
            help="Select your budget category"
        )
        
        travel_group = st.radio(
            "Travel Group",
            options=["Solo", "Couple", "Family", "Friends"],
            horizontal=True,
            help="Who are you traveling with?"
        )
        
        st.write("")  # Spacing
        st.write("")  # Spacing
    
    # Plan button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        plan_button = st.button("🚀 Plan My Trip", type="primary", use_container_width=True)
    
    # Process the request
    if plan_button:
        # Validate inputs
        if not destination:
            st.error("❌ Please enter a destination!")
            return
        
        if not api_key:
            st.warning("⚠️ Please provide a Groq API key in the sidebar or configure it in Streamlit secrets.")
            return
        
        try:
            # Initialize Groq client
            client = Groq(api_key=api_key)
            
            # Stage A: The Strategist
            with st.status("🔍 Analyzing your travel requirements...", expanded=True) as status:
                st.write("🧠 AI is determining what information to search for...")
                search_query = get_search_query(
                    client, destination, date_of_travel, duration, budget_level, travel_group
                )
                st.write(f"📝 Search query generated: *{search_query}*")
                
                # Search the web
                st.write("🌐 Searching the web for real-time information...")
                search_data = search_web(search_query)
                st.write("✅ Real-time data retrieved!")
                
                status.update(label="✅ Research complete!", state="complete")
            
            # Stage B: The Planner
            with st.spinner("✨ Generating your personalized itinerary..."):
                itinerary = generate_itinerary(
                    client, destination, date_of_travel, duration, 
                    budget_level, travel_group, search_data
                )
                st.session_state.itinerary = itinerary
            
            st.success("🎉 Your itinerary is ready!")
        
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            st.code(traceback.format_exc())
            return
    
    # Display the itinerary
    if st.session_state.itinerary:
        st.divider()
        st.markdown("## 📄 Your Travel Itinerary")
        
        # Add download button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="📥 Download Itinerary",
                data=st.session_state.itinerary,
                file_name=f"itinerary_{destination.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        # Display the itinerary
        st.markdown(st.session_state.itinerary)


if __name__ == "__main__":
    main()
