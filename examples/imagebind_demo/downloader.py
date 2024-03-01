import requests
import os
from pathlib import Path

# URL of the raw audio file on GitHub
audio_file_urls = ['https://github.com/raghavdixit99/assets/raw/main/bird_audio.wav',
                   'https://github.com/raghavdixit99/assets/raw/main/dragon-growl-37570.wav',
                   'https://github.com/raghavdixit99/assets/raw/main/car_audio.wav'
                   ]
image_urls = ['https://github.com/raghavdixit99/assets/assets/34462078/abf47cc4-d979-4aaa-83be-53a2115bf318',
              'https://github.com/raghavdixit99/assets/assets/34462078/93be928e-522b-4e37-889d-d4efd54b2112',
              'https://github.com/raghavdixit99/assets/assets/34462078/025deaff-632a-4829-a86c-3de6e326402f']

base_path = os.path.dirname(os.path.abspath(__file__))
# Local path where you want to save the .wav file
def dowload_and_save_audio():
    audio_pths=[]
    for url in audio_file_urls :
        filename=url.split('/')[-1]
        local_file_path = Path(f'{base_path}/test_inputs/{filename}')
        local_file_path.parent.mkdir(parents=True, exist_ok=True)
        # Perform the GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the content of the response to a local file
            with open(local_file_path, 'wb') as audio_file:
                audio_file.write(response.content)
                audio_pths.append(str(local_file_path))
            print(f"Audio file downloaded successfully and saved as '{local_file_path}'.")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    return audio_pths

def dowload_and_save_image():
    image_paths=[]
    for url in image_urls :
        filename=url.split('/')[-1]
        local_file_path = Path(f'{base_path}/test_inputs/{filename}.jpeg')

        local_file_path.parent.mkdir(parents=True, exist_ok=True)
        # Perform the GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Write the content of the response to a local file
            with open(local_file_path, 'wb') as image_file:
                image_file.write(response.content)
                image_paths.append(str(local_file_path))
            print(f"Image file downloaded successfully and saved as '{local_file_path}'.")
        else:
            print(f"Failed to download file. Status code: {response.status_code}")
    
    return image_paths