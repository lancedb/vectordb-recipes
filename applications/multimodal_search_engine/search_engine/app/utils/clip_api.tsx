
import axios from "axios";

export async function embedText(text: string) {
    const response = await axios({
        method: "POST",
        url: "https://infer.roboflow.com/clip/embed_text",
        params: {
            api_key: process.env.RF_API_KEY
        },
        data: {
            clip_version_id: "ViT-B-16",
            text: text
        },
        headers: {
            "Content-Type": "application/json"
        }
    });

    return response.data.embeddings[0];
}

export async function embedImage(file: string) {
    const response = await axios({
        method: "POST",
        url: `https://infer.roboflow.com/clip/embed_image`,
        params: {
            api_key: process.env.RF_API_KEY
        },
        data: {
            clip_version_id: "ViT-B-16",
            image: [
                {
                  type: "base64",
                  value: file
                }
              ]
        },
        headers: {
            "Content-Type": "application/json"
        }
    });

    return response.data.embeddings[0];
}

