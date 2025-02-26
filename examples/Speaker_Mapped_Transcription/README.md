# Speaker Mapped Transcription  

This project enables speaker diarization and transcription by mapping detected speakers to their actual names using vector search. It uses diarization outputs, applies speaker-name mapping, and aligns timestamps with transcriptions.  

Colab -  https://colab.research.google.com/github/vectordb-recipes/blob/main/examples/Speaker_Mapped_Transcription/Speaker_Mapping.ipynb

### How are we doing this?
This high-level flow diagram will help you understand how we are building this. We are creating a known database of speakers, and when generating the transcription, we utilize this database to get the correct speaker names.

![image](https://github.com/user-attachments/assets/b586a210-b04c-46df-8939-8a5d41b48e60)


### Features  
- Speaker diarization and transcription  
- Mapping detected speakers to actual names 
- Forced alignment for accurate word timestamps (limited)  
- Updated RTTM File with correct speaker names 

### Usage  
Process audio files, generate diarization results, map speakers, and export transcriptions with speaker labels.  

### Notes  
Ensure proper speaker colab setup for accurate mapping. Adjust configurations based on the data and computation.  

Let me know if you need any refinements! 🚀
