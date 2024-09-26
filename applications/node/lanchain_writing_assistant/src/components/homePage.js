import React, { useState,useEffect } from "react";
import TextEditor from "./TextEditor";
import Suggestion from "./suggestion";
import NavBar from "./navBar";

function Homepage() {
  const [suggestions, setSuggestions] = useState([]);
  const [loader, setLoader] = useState(false);

  const handleProcess = (results) => {
    setSuggestions(results);
  };

  const handleLoading = (value) => {
    setLoader(value);
  };

  return (
    <>
      <NavBar></NavBar>
      <div className="flex justify-between p-24 pt-8">
        <div className="w-1/2">
          <TextEditor
            onProcess={handleProcess}
            onLoading={handleLoading}
          ></TextEditor>
        </div>
        <div className="w-1/2">
          <Suggestion suggestions={suggestions} loader={loader}></Suggestion>
        </div>
      </div>
    </>
  );
}

export default Homepage;
