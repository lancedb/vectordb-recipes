import lancedb
import librosa
import numpy as np
import tempfile
import streamlit as st
import soundfile as sf
from panns_inference import AudioTagging

# download weight from drive  https://drive.google.com/file/d/1WLvGG9Brz7EOztisuAvwOTTIPjg6RRFr/view?usp=sharing
# Initialize AudioTagging model
at = AudioTagging(checkpoint_path="panns_data/Cnn14_mAP=0.431.pth", device="cpu")

# Connect to LanceDB
db = lancedb.connect("data/audio-lancedb")
table_name = "audio-search-mp3"
tbl = db.open_table(table_name)

# Title of the app with a catchy tagline
st.title('🎶 Music Recommendation System using LanceDB')
st.markdown("**Discover similar songs based on what you're listening to!** 🎧")

# Sidebar for testing with sample audio files
st.sidebar.header('🎵 Select a Sample Audio or Upload Your Own')
sample1 = 'music_sample_data/mp3/reggae/0FbDJdw23B6gM7HbkiFG76.mp3'
sample2 = 'music_sample_data/mp3/reggae/0gU5j8IxuaMSb2dBoZfnBh.mp3'

# Option to select sample audio files from the sidebar
sample_choice = st.sidebar.radio(
    "Choose a sample audio or upload your own:",
    ('None', 'Sample 1: reggae 1', 'Sample 2: reggae 2', 'Upload your own'),
    index=0
)

# Add an informative message in the sidebar
st.sidebar.markdown("Choose a sample track to test or upload your own audio file (MP3 format only) to get music recommendations based on the song.")

# Upload audio feature
query_mp3_path = None  # Initialize it with None
if sample_choice == 'Upload your own':
    uploaded_file = st.file_uploader("Upload a music file (MP3 format)", type=["mp3"])

    if uploaded_file is not None:
        # Use the uploaded file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_file.write(uploaded_file.read())
        query_mp3_path = temp_file.name

if sample_choice == 'Sample 1: reggae 1':
    query_mp3_path = sample1
elif sample_choice == 'Sample 2: reggae 2':
    query_mp3_path = sample2

# Handle uploaded files and sample files
if query_mp3_path:
    # Load the MP3 file into an audio array using librosa
    query_audio_array, query_sr = librosa.load(query_mp3_path, sr=None)

    # Display a success message and play the query audio
    st.success('Audio file loaded successfully! 🔊')
    st.audio(query_mp3_path, format='audio/mp3')

    # Perform embedding inference for the query audio file
    (_, query_embedding) = at.inference(np.expand_dims(query_audio_array, axis=0))  # Add batch dimension

    # Perform a vector similarity search using the computed embedding
    st.subheader('🔍 Searching for similar tracks...')
    results = tbl.search(query_embedding[0]).limit(5).to_df()  # Fetch top 5 results

    # Display the search results with more interactive UI
    st.subheader('🎶 Recommended Tracks:')

    if len(results) > 0:
        for i, row in results.iterrows():
            # Display only text without album image
            st.markdown(f"**Track {i+1}: {row['name']}** by **{row['artist']}**")
            # Retrieve the result audio and play it
            result_audio_array = np.array(row['audio'])
            sampling_rate = row['sampling_rate']

            # Save the audio to a temporary file for playback
            result_wav_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            sf.write(result_wav_file.name, result_audio_array, sampling_rate)

            # Play the recommended audio
            st.audio(result_wav_file.name, format='audio/wav')

    else:
        st.warning("No recommendations found. Try another song!")

else:
    st.info("Please select a sample audio or upload your own.")


# Footer with a short description of how the app works
st.markdown("---")
st.markdown("**How It Works:** Upload a song or choose a sample, and we'll use Lancedb vectordb to find other tracks with similar audio features. Enjoy your personalized music recommendations! 🎧")
