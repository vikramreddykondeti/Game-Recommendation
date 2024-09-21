# import streamlit as st
# import pickle
# import pandas as pd
# from PIL import Image
# import requests
# from     io import BytesIO

# # Load games data and similarity matrix with caching to improve performance
# @st.cache_data
# def load_games_data():
#     games_dict = pickle.load(open('new_df_dict.pkl', 'rb'))
#     return pd.DataFrame(games_dict)

# @st.cache_data
# def load_similarity_matrix():
#     return pickle.load(open('similarity.pkl', 'rb'))

# # Function to recommend games
# def recommend(game_name):
#     if game_name not in games['Name'].values:
#         return None, "Selected game not found in the dataset."
    
#     game_index = games[games['Name'] == game_name].index[0]
    
#     if game_index >= len(similarity):
#         return None, "Game index is out of bounds for the similarity matrix."
    
#     distances = similarity[game_index]
#     games_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:]
    
#     recommended_games = [games.iloc[i[0]]['Name'] for i in games_list]
#     return recommended_games, None

# # Function to load and display images
# def display_image(url, game_name):
#     if pd.notna(url):
#         try:
#             response = requests.get(url)
#             image = Image.open(BytesIO(response.content))
#             st.image(image, caption=game_name, use_column_width=True)
#         except Exception as e:
#             st.error(f"Error loading image: {e}")

# # Load the games data and similarity matrix
# games = load_games_data()
# similarity = load_similarity_matrix()

# if 'Name' not in games.columns:
#     st.error("The 'Name' column is missing from the games DataFrame.")
#     st.stop()

# st.title('Game Recommendation System')

# # Select a game from the available options
# selected_game_name = st.selectbox('Select your favorite game', games['Name'].unique())

# # Recommend games when the button is clicked
# if st.button("Recommend"):
#     recommendation, error_message = recommend(selected_game_name)
    
#     if error_message:
#         st.error(error_message)
#     elif recommendation:
#         num_games = len(recommendation)
#         num_pages = (num_games // 9) + (1 if num_games % 9 > 0 else 0)
        
#         # Add page navigation
#         page = st.selectbox('Select Page', range(1, num_pages + 1))
#         start_index = (page - 1) * 9
#         end_index = min(page * 9, num_games)
        
#         st.write(f"Showing results from index {start_index} to {end_index}")
        
#         for game in recommendation[start_index:end_index]:
#             st.write(game)
            
#             # Display additional game information
#             game_info = games[games['Name'] == game]
#             st.write(game_info[['Name', 'Release date', 'DLC count', 'Header image', 'Website', 'Screenshots', 'Tags']])
            
#             # Display game image
#             display_image(game_info['Header image'].values[0], game_info['Name'].values[0])
            
#             # Make websites clickable
#             website = game_info['Website'].values[0]
#             if website:
#                 st.markdown(f"[Website]({website})")
#     else:
#         st.error("No recommendations found.")


#         # Remove page navigation
#         st.write(f"Showing all recommendations")


#80k+ games in the dataset



import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import base64

# Load games data and similarity matrix with caching to improve performance
@st.cache_data
def load_games_data():
    games_dict = pickle.load(open('new_df_dict.pkl', 'rb'))
    return pd.DataFrame(games_dict)

@st.cache_data
def load_similarity_matrix():
    return pickle.load(open('similarity.pkl', 'rb'))

# Function to recommend games
def recommend(game_name, num_recommendations):
    if game_name not in games['Name'].values:
        return None, "Selected game not found in the dataset."
    
    game_index = games[games['Name'] == game_name].index[0]
    distances = similarity[game_index]
    games_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:]

    recommended_games = []
    for i in games_list[:num_recommendations]:
        recommended_games.append(games.iloc[i[0]])
    
    if not recommended_games:
        return None, "No recommendations for that game."
    
    return recommended_games, None

# Function to load and display images
def display_image(url, game_name):
    if pd.notna(url):
        try:
            response = requests.get(url)
            image = Image.open(BytesIO(response.content))
            st.image(image, caption=game_name, use_column_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")

# Load the games data and similarity matrix
games = load_games_data()
similarity = load_similarity_matrix()

# Function to load CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call the function to load the CSS
load_css()

# Rest of your Streamlit app code...
st.title('🎮 Game Recommendation System')

st.write("Discover new games based on your favorites! Enter a game name for personalized recommendations.")

# Select a game from the available options
selected_game_name = st.selectbox('Select your favorite game', games['Name'].unique())

# Slider to select number of recommendations
num_recommendations = st.slider("Number of Recommendations", min_value=1, max_value=20, value=5)

# Recommend games when the button is clicked
if st.button("Recommend"):
    with st.spinner("Generating recommendations..."):
        recommendation, error_message = recommend(selected_game_name, num_recommendations)
        
        if error_message:
            st.error(error_message)
        elif recommendation:
            st.write("Here are your recommended games:")
            
            for game in recommendation:
                st.subheader(game['Name'])
                
                # Create a markdown block for additional game information
                release_date = game['Release date'] if 'Release date' in game else "N/A"
                
                st.markdown(f"""
                    **Release Date:** {release_date}  
                    <p style="background-color: #e6e6fa; padding: 10px; border-radius: 5px;">
                    </p>
                """, unsafe_allow_html=True)
                
                # Display game image
                display_image(game['Header image'], game['Name'])
                
                # Make websites clickable
                website = game['Website']
                if website:
                    st.markdown(f"[Website]({website})")
                st.write("---")
        else:
            st.error("No recommendations found.")

# Additional styling for input
input_style = """
<style>
input[type="text"] {
    background-color: transparent;
    color: #a19eae; /* This changes the text color inside the input box */
}
div[data-baseweb="base-input"] {
    background-color: transparent !important;
}
</style>
"""
st.markdown(input_style, unsafe_allow_html=True)




