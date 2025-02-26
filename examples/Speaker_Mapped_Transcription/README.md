# Speaker Mapped Transcription  

This project enables speaker diarization and transcription by mapping detected speakers to their actual names using vector search. It uses diarization outputs, applies speaker-name mapping, and aligns timestamps with transcriptions.  

Colab -  https://colab.research.google.com/github/vectordb-recipes/blob/main/examples/Speaker_Mapped_Transcription/Speaker_Mapping.ipynb

### Creating Known Database of Speakers using LanceDB
We first create a known database of speakers (say employees in a company). This database is used to get correct speaker names based on audio similarity.

![image](https://github.com/user-attachments/assets/4536d069-dde9-478d-bb07-a008f02aebe4)

### Transcription and Diarization
Next we take the input audio and create a transcript using OpenAI's Whisper Model. We also utilize Nemo-MSDD model by Nvidia for diarization.

![image](https://github.com/user-attachments/assets/a5f63055-b2ee-48a3-b71a-c58761e0361a)

### How are we doing this together?
This high-level flow diagram will help you understand how we are building this together. We are creating a known database of speakers, and when generating the transcription, we utilize this database to get the correct speaker names.

![image](https://github.com/user-attachments/assets/b586a210-b04c-46df-8939-8a5d41b48e60)

### Features  
- Speaker diarization and transcription  
- Mapping detected speakers to actual names using LanceDB vector search.
- Forced alignment for accurate word timestamps (limited)  
- Updated RTTM File with correct speaker names.

### Usage  
Process audio files, generate diarization results, map speakers using vector search, and export transcriptions with speaker labels. Note that we are saving our embeddings on **Azure Blob Storage** in this example. You can chose to switch to local or any other object store as per your preference.

### Notes  
Ensure proper speaker colab setup for accurate mapping. Adjust configurations based on the data and computation.  

Let me know if you need any refinements! 🚀
