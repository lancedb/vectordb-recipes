## RAG Fusion - The New Star of Search Technology

### Overview
This repository contains code and implementation for RAG Fusion. 
The main feature of this repo is RRF(Reciprocal Rank Fusion) Algorithm implemented which reranks the
documents based on the queries generated from original query given by user. It uses LanceDB as vector 
database to store and retrieve documents related to queries via OPENAI Embeddings. It can be used in 
any fields where we need to get the most information out of the box.

### Examples
Question | Define Doppler Effect in Wave optics |
--- | --- 
RAG Retrieval | The Doppler Effect in wave optics refers to the shift in frequency and wavelength of a wave caused by the relative motion between the source of the wave and the observer. When the source of the wave is moving towards the observer, the wavelength of the wave appears shorter and the frequency appears higher, known as a blue shift. When the source of the wave is moving away from the observer, the wavelength appears longer and the frequency appears lower, known as a red shift. This effect is applicable to both sound waves and light waves. 

Question | Huygens Principle |
--- | ---
RAG Retrieval | Huygens' principle is a principle of wave propagation that states that each point on a wavefront can be thought of as a source of secondary wavelets that spread out in all directions. These secondary wavelets combine together to form the shape of the wavefront at a later time. It can be used to explain phenomena such as reflection, refraction, interference, diffraction, and polarization.
### CODE
Colab Demo for the RAG Fusion <a href="https://colab.research.google.com/github/lancedb/vectordb-recipes/blob/main/examples/RAG_Fusion/main.ipynb"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"></a>
