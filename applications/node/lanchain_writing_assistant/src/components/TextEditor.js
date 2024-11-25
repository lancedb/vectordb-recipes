import React, {
  useState,
  useEffect
} from "react";
import ReactQuill from "react-quill";
import "react-quill/dist/quill.snow.css"; // Import Quill styles
import "./../App.css"; // Import your custom styles
import { useDebounce } from "./useDebounce";
import {PencilIcon} from '@heroicons/react/24/solid';

function TextEditor({ onProcess, onLoading }) {
  const modules = {
    toolbar: [
      [
        {
          header: "1",
        },
        {
          header: "2",
        },
        {
          font: [],
        },
      ],
      [
        {
          size: [],
        },
      ],
      ["bold", "italic", "underline", "strike", "blockquote"],
      [
        {
          list: "ordered",
        },
        {
          list: "bullet",
        },
      ],
      ["link", "image"],
      ["clean"],
    ],
  };

  const formats = [
    "header",
    "font",
    "size",
    "bold",
    "italic",
    "underline",
    "strike",
    "blockquote",
    "list",
    "bullet",
    "link",
    "image",
  ];

  const [input, setInput] = useState("");
  const debouncedInput = useDebounce(input, 500);

  const handleProcess = async (text) => {
    try {
      const response = await fetch("http://localhost:5300/process-text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: text,
        }),
      });
      const data = await response.json();
      onProcess(data.result);
      onLoading(false); // Pass the result to the Suggestion component
    } catch (error) {
      console.error("Error processing text:", error);
    }
  };

  const handleChange = (e) => {
    setInput(e);
  };

  // Function to get the last 10 words
  const getLastWords = (text, wordCount = 7) => {
    // Split the text into words
    const words = text.trim().split(/\s+/);
    // Extract the last `wordCount` words or fewer if the total words are less
    const lastWords = words.slice(-wordCount).join(" ");
    return lastWords;
  };

 useEffect(() => {
   if (debouncedInput) {
     const lastWords = getLastWords(debouncedInput, 7);
     onLoading(true);
     handleProcess(lastWords); // Call the API when user stops typing
   }
 }, [debouncedInput]);

  return (
    <>
      <div className="max-w-3xl mx-auto">
        < h2 className = "text-1xl font-semibold text-center text-gray-800 mb-6 bg-gradient-to-r from-blue-500 via-blue-500 to-red-500 text-transparent bg-clip-text flex items-center justify-center" >
          Pen Down Your Genius
          <PencilIcon className = "h-5 w-6 text-blue-500" style={{ marginLeft: '6px' }}/>
        </h2>
        <ReactQuill
          value={input}
          className = "h-[75vh] bg-white rounded shadow-md rounded-lg border-2 border-gray-300 my-6 bg-white shadow-lg transition-shadow hover:shadow-2xl suggestion-box mr-4"
          onChange={handleChange}
          theme="snow"
          placeholder="Start typing..."
          modules={modules}
          formats={formats}
        />{" "}
      </div>
    </>
  );
}
export default TextEditor;
