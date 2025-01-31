import { useState } from "react";
import axios from "axios";
import { Image} from "phosphor-react";
import { MagnifyingGlass} from "phosphor-react";

export default function SearchBar({ handleQuery }) {
  const [query, setQuery] = useState("");
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
    const [type, setType] = useState("text");

  return (
    <div className="sticky bottom-0 w-full p-2 flex items-center gap-4 h-16">
      <input
        type="text"
        placeholder="Search memes..."
        className="w-full p-2 rounded-lg text-black focus:outline-none border-2 text-gray-700"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <input
        type="file"
        accept="image/*"
        className="hidden"
        id="fileInput"
        onChange={(e) => {
            if (e.target.files === null) return;
            setQuery("");
            const file = e.target.files[0];
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onloadend = () => {
              const base64String = reader.result;
              const base64 = base64String?.toString().split(",")[1];
              handleQuery(base64, "image");
            };
          }}
      />
      <label htmlFor="fileInput" className="cursor-pointer px-4 py-2 bg-white rounded-lg text-white border-2">
        <Image size={24} color="black" />
      </label>
      <button
        onClick={() => handleQuery(query, type)}
        className="bg-red-400 px-4 py-2 rounded-lg text-white flex items-center justif-center"
        disabled={loading}
      >
        <MagnifyingGlass size={20} color="#e9e7e7"  className="mr-4"/>
        {loading ? "Searching..." : "Search"}
      </button>
    </div>
  );
}
