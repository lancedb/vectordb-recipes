"use client";

import { Result } from '@/node_modules/postcss/lib/postcss';
import Image from 'next/image'
import { embedText, embedImage } from './utils/clip_api'
import { useState } from 'react';

async function getEmbedding(input: string, type: "text" | "image") {
  if ( type === "text") {
    return await embedText(input);
  } else {
    return await embedImage(input);
  }
}

export default function Home() {
  const [text, setText] = useState<string>("");
  const [image, setImage] = useState<string>("");

  return (

    <div>
        <div>
            <div className="flex border border-purple-200 rounded">
                <input
                    type="text"
                    className="block w-full px-4 py-2 text-purple-700 bg-white border rounded-md focus:border-purple-400 focus:ring-purple-300 focus:outline-none focus:ring focus:ring-opacity-40"
                    placeholder="Search..."
                />
                <button className="px-4 text-white bg-purple-600 border-l rounded ">
                    Search
                </button>
            </div>
        </div>
    </div>

  )
}
