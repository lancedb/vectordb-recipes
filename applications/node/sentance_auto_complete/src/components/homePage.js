import React, { useState } from "react";
import TextEditor from "./TextEditor";
import Suggestion from "./suggestion";
import NavBar from "./navBar";
import FileUploaderModal from "./fileUploaderModal";
import { ArrowUpTrayIcon } from '@heroicons/react/24/outline'; 
import {getFileName} from "./store"


function Homepage() {
  const [suggestions, setSuggestions] = useState([]);
  const [loader, setLoader] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);

   const openModal = () => {
     setIsModalOpen(true);
   };

   const closeModal = () => {
     setIsModalOpen(false);
   };

  const handleProcess = (results) => {
    setSuggestions(results);
  };

  const handleLoading = (value) => {
    setLoader(value);
  };

  return (
    <>
      <NavBar></NavBar>
      <div className="bg-slate-700 flex justify-center">
        <button className="shadow-[0_4px_15px_rgba(0,0,0,0.8)] flex bg-slate-950 text-white px-4 py-2 rounded mt-4"  onClick={openModal}><ArrowUpTrayIcon className="w-6 h-6 pr-1"/> Choose a data source </button>
       <div className="pt-6 pl-4 italic text-lime-300">
          {getFileName()=== "" ?  null : `uploaded file: ${getFileName()}`}
       </div>
      </div>
      <div className="flex justify-between p-24 pt-0 bg-slate-700">
        <div className="w-1/2">
          <TextEditor
            onProcess={handleProcess}
            onLoading={handleLoading}
          ></TextEditor>
        </div>
        <div className="w-1/2">
          <Suggestion suggestions={suggestions} loader={loader}></Suggestion>
        </div>
        <FileUploaderModal isOpen={isModalOpen} onClose={closeModal} />
      </div>
    </>
  );
}

export default Homepage;
