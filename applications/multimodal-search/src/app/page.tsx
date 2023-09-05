"use client";
import { useState, useEffect } from "react";
import SearchBar from "./components/SearchBar";
import Gallery from "./components/Gallery";

export default function Home() {
  const [db, setDb] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [imgs, setImgs] = useState([]);

  function getSimilarImages(embedding: Array<number>) {
    fetch("api/retrieve", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: embedding, table: db }),
    }).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          setImgs(data);
        });
      } else {
        setError("Failed to find similar images.");
      }
    });
  }

  useEffect(() => {
    fetch("api/context", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    }).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          setDb(data.table);
        });
        setLoading(false);
      } else {
        setError("Failed to load data into LanceDB");
      }
    });
  }, []);

  useEffect(() => {
    if (db === "") return;
    getSimilarImages(
      Array.from({ length: 512 }, () => Math.floor(Math.random() * 512))
    );
  }, [db]);

  function search(query: string, type: "text" | "image") {
    fetch("/api/embed", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: query, type: type }),
    }).then((response) => {
      if (response.ok) {
        response.json().then((data) => {
          getSimilarImages(data.embedding);
        });
      } else {
        setError("Failed to embed query.");
      }
    });
  }

  return (
    <main className="flex min-h-screen flex-col dark dark:bg-gray-800 dark:text-gray-200">
      <div>
        {loading || imgs.length == 0 ? (
          <div className="flex flex-col items-center justify-center flex-1">
            loading...
            {error}
          </div>
        ) : (
          <div className="flex flex-col flex-1">
            <SearchBar handleQuery={search} />
            <Gallery imgs={imgs} />
          </div>
        )}
      </div>
    </main>
  );
}
