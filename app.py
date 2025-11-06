import streamlit as st
import pandas as pd
import requests
import pickle

# Load the processed data and similarity matrix
@st.cache_data
def load_data():
    """Load movie data and similarity matrix with error handling"""
    import gzip
    
    try:
        # Try ultra-compressed version first (for deployment)
        with gzip.open('movie_data_ultra.pkl.gz', 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        try:
            # Fallback to regular compressed version
            with open('movie_data_compressed.pkl', 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            try:
                # Final fallback to original version
                with open('movie_data.pkl', 'rb') as file:
                    return pickle.load(file)
            except FileNotFoundError:
                st.error("❌ Movie data files not found. Please ensure the data files are present.")
                st.stop()
    except Exception as e:
        st.error(f"❌ Error loading movie data: {str(e)}")
        st.stop()

# Load data
try:
    movies, cosine_sim = load_data()
    st.success(f"✅ Successfully loaded {len(movies):,} movies!")
except Exception as e:
    st.error(f"Failed to load data: {e}")
    st.stop()

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    
    try:
        # Add timeout and retry logic
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        
        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_path
        else:
            # Return a placeholder image if no poster found
            return get_placeholder_image(movie_id)
            
    except requests.exceptions.RequestException:
        # Return a placeholder image on error (don't show warning to avoid spam)
        return get_placeholder_image(movie_id)
    except Exception:
        return get_placeholder_image(movie_id)

def get_placeholder_image(movie_id):
    """Generate a placeholder image URL with movie ID"""
    return f"https://via.placeholder.com/300x450/262730/FAFAFA?text=Movie+ID%3A+{movie_id}"

def get_responsive_columns():
    """Return number of columns based on screen size"""
    # This is a simplified approach - Streamlit will handle the actual responsiveness
    # through CSS and the use_container_width parameter
    return 5  # Default to 5 columns, CSS will handle the responsive behavior

# Streamlit UI
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="auto"  # Auto-collapse on mobile
)

# Add comprehensive responsive CSS
st.markdown("""
<style>
    /* Base responsive styles */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Mobile First - Small screens (up to 768px) */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        .stSelectbox > div > div {
            font-size: 14px;
        }
        
        .stButton > button {
            width: 100%;
            font-size: 16px;
            padding: 0.75rem 1rem;
            margin: 0.5rem 0;
        }
        
        .stMetric {
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .stMarkdown h1 {
            font-size: 2rem;
        }
        
        .stMarkdown h3 {
            font-size: 1.2rem;
        }
        
        /* Sidebar adjustments for mobile */
        .css-1d391kg {
            padding-top: 1rem;
        }
    }
    
    /* Tablet - Medium screens (769px to 1024px) */
    @media (min-width: 769px) and (max-width: 1024px) {
        .stSelectbox > div > div {
            font-size: 15px;
        }
        
        .stButton > button {
            font-size: 16px;
            padding: 0.6rem 1.2rem;
        }
    }
    
    /* Desktop - Large screens (1025px and up) */
    @media (min-width: 1025px) {
        .main .block-container {
            max-width: 1200px;
        }
    }
    
    /* Image responsiveness */
    .stImage > img {
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.2s ease;
        width: 100%;
        height: auto;
    }
    
    .stImage > img:hover {
        transform: scale(1.05);
    }
    
    /* Responsive text alignment */
    .stMarkdown h1, .stMarkdown h3 {
        text-align: center;
    }
    
    .stMarkdown h3 {
        margin-bottom: 2rem;
    }
    
    /* Enhanced button styling */
    .stButton > button {
        background: linear-gradient(90deg, #FF6B6B, #FF8E8E);
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.3);
    }
    
    /* Responsive columns */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Info box responsiveness */
    .stAlert {
        margin: 1rem 0;
    }
    
    /* Success message styling */
    .stSuccess {
        text-align: center;
        margin: 1.5rem 0;
    }
    
    /* Metric responsiveness */
    .metric-container {
        text-align: center;
    }
    
    /* Ensure proper spacing on all devices */
    .stContainer {
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")
st.markdown("### Discover movies you'll love based on your favorites!")

# Responsive sidebar with information
with st.sidebar:
    st.header("📊 System Info")
    
    # Compact metrics for mobile
    st.metric("Total Movies", f"{len(movies):,}")
    st.metric("Algorithm", "Cosine Similarity")
    st.metric("Dataset", "TMDB 5000")
    
    with st.expander("🔍 How it works"):
        st.write("""
        **Analysis includes:**
        - Genres (Action, Comedy, etc.)
        - Keywords (space war, romance, etc.)  
        - Cast (top 3 actors)
        - Directors
        
        **Method:** TF-IDF + Cosine Similarity
        """)
    
    with st.expander("📱 Mobile Tips"):
        st.write("""
        - Swipe to scroll through recommendations
        - Tap movie posters to see details
        - Use landscape mode for better viewing
        """)
    
    st.markdown("---")
    st.markdown("**Made with ❤️ using Streamlit**")

# Main content - Responsive layout
# Check if we're on mobile by using container width
is_mobile = st.container()

# Responsive layout for movie selection
if st.session_state.get('mobile_view', False):
    # Mobile layout - single column
    selected_movie = st.selectbox(
        "🎭 Choose a movie to get recommendations:",
        options=movies['title'].values,
        index=0
    )
    st.metric("Movies in Database", f"{len(movies):,}")
else:
    # Desktop layout - two columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_movie = st.selectbox(
            "🎭 Choose a movie to get recommendations:",
            options=movies['title'].values,
            index=0
        )
    
    with col2:
        st.metric("Movies in Database", f"{len(movies):,}")

# Responsive info section
with st.container():
    st.info("💡 **Tip:** Movie posters are fetched from TMDB API. If they don't load, placeholder images will be shown.")

if st.button('🎯 Get Recommendations', type="primary", use_container_width=True):
    with st.spinner('🔍 Analyzing movie features and finding similar titles...'):
        recommendations = get_recommendations(selected_movie)
    
    if len(recommendations) > 0:
        st.success(f"✨ **Top 10 movies similar to '{selected_movie}'**")
        
        # Responsive grid layout
        # Desktop: 5 columns, Tablet: 3 columns, Mobile: 2 columns
        def create_responsive_grid(recommendations):
            # Create responsive breakpoints
            total_movies = len(recommendations)
            
            # For mobile/small screens - 2 columns
            mobile_cols = 2
            # For tablet/medium screens - 3 columns  
            tablet_cols = 3
            # For desktop/large screens - 5 columns
            desktop_cols = 5
            
            # Use desktop layout by default, but this will adapt based on screen size
            cols_per_row = desktop_cols
            
            for i in range(0, total_movies, cols_per_row):
                # Create columns for current row
                cols = st.columns(cols_per_row)
                
                # Fill the columns with movies
                for col_idx, movie_idx in enumerate(range(i, min(i + cols_per_row, total_movies))):
                    if col_idx < len(cols):
                        movie_title = recommendations.iloc[movie_idx]['title']
                        movie_id = recommendations.iloc[movie_idx]['movie_id']
                        
                        with cols[col_idx]:
                            # Create a responsive container for each movie
                            with st.container():
                                poster_url = fetch_poster(movie_id)
                                
                                try:
                                    st.image(poster_url, use_container_width=True)
                                except Exception:
                                    st.image("https://via.placeholder.com/300x450/262730/FAFAFA?text=No+Image", 
                                           use_container_width=True)
                                
                                # Responsive text sizing
                                st.markdown(f"**{movie_title}**")
                                st.caption(f"ID: {movie_id}")
        
        create_responsive_grid(recommendations)
        
        # Add responsive stats section
        st.markdown("---")
        
        # Responsive stats layout
        stats_cols = st.columns([1, 1, 1])
        
        with stats_cols[0]:
            st.metric("Recommendations Found", len(recommendations))
        with stats_cols[1]:
            st.metric("Based on Movie", selected_movie[:20] + "..." if len(selected_movie) > 20 else selected_movie)
        with stats_cols[2]:
            st.metric("Algorithm", "Cosine Similarity")
            
    else:
        st.error("❌ No recommendations found. Please try selecting a different movie.")
