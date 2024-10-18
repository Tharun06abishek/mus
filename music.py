import streamlit as st
import tidalapi

# Function to initialize the Tidal session
def initialize_session():
    session = tidalapi.Session()
    st.write("Please authenticate through your Tidal account.")
    session.login_oauth_simple()  # Opens a browser window for user login
    return session

# Function to search for artists by name
def search_artist(session, artist_name):
    try:
        # Search for the artist
        search_results = session.search('artists', artist_name)
        if search_results.artists:
            # Display the top result
            artist = search_results.artists[0]
            st.write(f"Artist found: {artist.name}")
            st.write(f"Artist ID: {artist.id}")
            st.write(f"Number of Albums: {artist.album_count}")
            st.write(f"Number of Tracks: {artist.track_count}")
        else:
            st.write("No artists found.")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Function to display albums of the artist
def display_albums(session, artist_id):
    try:
        # Fetch albums of the artist
        artist = session.artist(artist_id)
        albums = artist.get_albums()
        st.write(f"Albums by {artist.name}:")
        for album in albums:
            st.write(f"- {album.title} ({album.release_date})")
    except Exception as e:
        st.error(f"Error: {str(e)}")

# Streamlit UI
st.title("Tidal API Interface")

# Button to initialize Tidal session
if st.button("Connect to Tidal"):
    session = initialize_session()
    if session.check_login():
        st.success("Successfully connected to Tidal!")
        
        # Artist search input
        artist_name = st.text_input("Enter artist name:")
        if artist_name:
            search_artist(session, artist_name)
        
        # Optional: Enter artist ID to display albums
        artist_id = st.text_input("Enter artist ID to fetch albums (optional):")
        if artist_id:
            display_albums(session, artist_id)
    else:
        st.error("Failed to connect to Tidal. Please try again.")
