import { NextResponse } from 'next/server'
import axios from 'axios'

export async function POST(req: Request) {
  const { data, type } = await req.json()
  try {
    if (type === 'text')
    {
      return NextResponse.json({ embedding : await embedText(data)}); 
    } else if (type === 'image')
    {
      return NextResponse.json({ embedding: await embedImage(data) });
    }
  } catch (e) {
    console.log(e)
    return NextResponse.json(e, {
      status: 400
    })
  }
}

async function embedText(text: string) {
    const response = await axios({
        method: "POST",
        url: "https://infer.roboflow.com/clip/embed_text",
        params: {
            api_key: process.env.RF_API_KEY || ""
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
  
  async function embedImage(file: string) {

    const response = await axios({
        method: "POST",
        url: `https://infer.roboflow.com/clip/embed_image`,
        params: {
          api_key: process.env.RF_API_KEY || ""
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
  
  
  