import React, { useState } from "react";
import {setFileName} from "./store"

function FileUploader({ onClose }) {
  const [uploadStatus, setUploadStatus] = useState(null); // "success", "error", or null
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);  // Track loading state


 const handleFileChange = async (event) => {
   const file = event.target.files[0];
   setFile(file);
   setFileName(file.name)
   if (file) {
     // Perform file upload logic here
     // For now, we'll simulate a successful upload after 1 second
     setUploadStatus("success");
    //  setTimeout(() => setUploadStatus(null), 3000); // Reset status after 3 seconds
   } else {
     setUploadStatus("error");
   }
 };

 // Handle file upload
 const handleFileUpload = async () => {
   if (!file) {
     alert("Please select a file first.");
     return;
   }
   setLoading(true);
   const formData = new FormData();
   formData.append("file", file);

   try {
     const response = await fetch("http://localhost:5300/upload-file", {
       method: "POST",
        body: formData
     });
     const data = await response.json();
     console.log("File processed:", data);
     if(data) {
        setLoading(false); // Stop the loader
        onClose();
     }

   } catch (error) {
     console.error("Error uploading file:", error);
   }
 };


  const borderColor =
    uploadStatus === "success" ? "border-green-500" : "border-gray-300";
  const bgColor = uploadStatus === "success" ? "bg-green-50" : "bg-gray-50";
  const textColor =
    uploadStatus === "success" ? "text-green-600" : "text-gray-500";

  return (
    <div className="items-center justify-center w-full p-4">
      <label
        htmlFor="dropzone-file"
        className={`flex flex-col items-center justify-center w-full h-64 border-2 ${borderColor} border-dashed rounded-lg cursor-pointer ${bgColor} dark:${bgColor} hover:bg-gray-100 dark:hover:bg-gray-300`}
      >
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          <svg
            className={`w-8 h-8 mb-4 ${textColor}`}
            aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 20 16"
          >
            <path
              stroke="currentColor"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
            />
          </svg>
          <p className={`mb-2 text-sm ${textColor}`}>
            <span className="font-semibold">Upload your data source</span> or drag and
            drop
          </p>
          <p className={`text-xs ${textColor}`}>.txt types file only</p>
          {uploadStatus === "success" && (
            <p className="text-sm text-green-600">Upload successful!</p>
          )}
          {uploadStatus === "error" && (
            <p className="text-sm text-red-600">Upload failed!</p>
          )}
          {file?.name && (
            <p className="mt-2 text-sm text-gray-600">
              Selected file: {file.name}
            </p>
          )}
        </div>
        <input
          id="dropzone-file"
          type="file"
          accept=".txt"
          className="hidden"
          onChange={handleFileChange}
        />
      </label>
        <div className="mt-8 flex justify-end">
          { !loading ? (<button className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-700" onClick={handleFileUpload}>Upload File</button>) : ( <button className="bg-gray-300 text-white px-4 py-2 rounded" disabled={loading} onClick={handleFileUpload}>uploading...</button>)}
        </div>
    </div>
  );
}

export default FileUploader;

