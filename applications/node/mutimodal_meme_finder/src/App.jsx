import { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import MemeGrid from "./components/MemeGrid";
import TopBar from "./components/TopBar";
import { ThreeDots } from 'react-loader-spinner'


export default function App() {
  const [db, setDb] = useState("table_text");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [imgs, setImgs] = useState([]);

  function getSimilarImages(embedding) {
    fetch("http://localhost:5400/retrive-results", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: embedding, table: db }),
    }).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          setImgs(data.result);
          setLoading(false);
        });
      } else {
        setError("Failed to find similar images.");
      }
    });
  }

  // useEffect(() => {
  //   if (db === "") return;
  //   getSimilarImages(
  //     Array.from({ length: 512 }, () => Math.floor(Math.random() * 512))
  //   );
  // }, [db]);

  function search(query, type) {
    if(query==="") return;
    setLoading(true);
    if(type === 'image') {
      setDb('table');
    } else if (type === 'text') {
      setDb('table_text');
    }
    fetch("http://localhost:5400/get-embeddings", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: query, type: type }),
    }).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          getSimilarImages(data.result);
        });
      } else {
        setError("Failed to embed query.");
      }
    });
  }

  return (
    <div className="h-screen flex flex-col bg-gradient-to-r from-purple-500 via-purple-300 via-purple-200 via-pink-400 via-pink-300 via-pink-200 via-red-400 via-red-300 via-red-200 via-yellow-200 to-red-300">
      <TopBar />
      {error && <p className="text-red-500 mt-2">{error}</p>}
      { loading ? (
        <div className="flex flex-col items-center justify-center flex-1">
          <ThreeDots  visible={true}  height="80" width="50" color="red" radius="9" ariaLabel="three-dots-loading"/>
        </div>
      ) : imgs.length === 0 ? (
        <div className="flex flex-col items-center justify-center flex-1">
          <span className="text-red-600">Type or upload an image to find your memes...</span>
        </div>
      ) : (
        <div className="flex-1 overflow-auto px-24 pb-4 pt-0 mb-12 mt-0">
          <MemeGrid memes={imgs} error={error} />
        </div>
      )}
       <div className="sticky bottom-6 w-full flex justify-center">
          <div className="w-[70%]">
            {/* <SearchBar setMemes={setMemes} setError={setError} /> */}
            <SearchBar handleQuery={search} />
          </div>
        </div>
    </div>
  );
}


