import React, { useState,useEffect } from "react";
import JobCard from "./components/JobCard";
import "./App.css";
import MultiRangeSlider from "multi-range-slider-react";
import axios from "axios";
import { ThreeDots } from 'react-loader-spinner'


const App = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filters, setFilters] = useState({
    skills: [],
    locations: [],
    title:''
  });
  const [skillInput, setSkillInput] = useState("");
  const [locationInput, setLocationInput] = useState("");
  const [minValue, set_minValue] = useState(0);
  const [maxValue, set_maxValue] = useState(500000);
  const [fetchedJobs, setFetchedJobs] = useState([]);
  const [loader, setLoader] = useState(false);

  const sliderStyles = {
    border: "none",
    boxShadow: "none",
    backgroundColor: "none",
    height: "20px",
  };

   useEffect(() => {
    handleSearch();
  }, []);

  const handleInput = (e) => {
    set_minValue(e.minValue);
    set_maxValue(e.maxValue);
  };

  const handleSkillInput = (event) => {
    if (event.key === "Enter" && skillInput.trim() !== "") {
      if (!filters.skills.includes(skillInput.trim())) {
        setFilters((prev) => ({
          ...prev,
          skills: [...prev.skills, skillInput.trim()],
        }));
      }
      setSkillInput("");
    }
  };

  const removeSkill = (skill) => {
    setFilters((prev) => ({
      ...prev,
      skills: prev.skills.filter((s) => s !== skill),
    }));
  };

  const handleLocationInput = (event) => {
    if (event.key === "Enter" && locationInput.trim() !== "") {
      if (!filters.locations.includes(locationInput.trim())) {
        setFilters((prev) => ({
          ...prev,
          locations: [...prev.locations, locationInput.trim()],
        }));
      }
      setLocationInput("");
    }
  };

  const removeLocation = (location) => {
    setFilters((prev) => ({
      ...prev,
      locations: prev.locations.filter((loc) => loc !== location),
    }));
  };

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const handleSearch = async () => {
    const body = {
      skills : filters.skills || [],
      location: filters.locations || [],
      title: filters.title || '',
      salary: [minValue,maxValue]
    };
    body.text = `${filters.skills.join(", ")} ${filters.locations.join(", ")} ${filters.title || ''} ${minValue} ${maxValue}`;

    try {
      setLoader(true);
      setLoader(true);
      const response = await axios.post("http://localhost:5400/searchJobs", {
        body
      });
      setFetchedJobs(response.data.result || []);
      setLoader(false);
    } catch (error) {
      console.error("Error fetching jobs:", error);
    }
  };

  return (<>
    <div className="app-container flex bg-gray-100 p-4">
      {/* Left Sidebar for Filters */}
      <div className="filters-section w-1/4 p-4 bg-gray-200 rounded h-fit">
        {/* <h2 className="text-xl font-semibold mb-4 text-center">Filters</h2> */}

         {/* title */}
        <div className="filter-group mb-4">
          <h3 className="font-medium mb-2">Explore job opportunities</h3>
          <input
            type="text"
            placeholder="Search..."
            value={filters.title}
            onChange={(e) => handleFilterChange("title", e.target.value)}
            className="w-full p-2 border rounded"
          />
        </div>

        {/* Skills Input */}
        <div className="filter-group mb-4">
          <h3 className="font-medium mb-2">Skills</h3>
          <div className="skills-input">
            <input
              type="text"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              onKeyDown={handleSkillInput}
              placeholder="Type a skill and press Enter"
              className="w-full p-2 border rounded"
            />
            <div className="flex flex-wrap gap-2 mt-2">
              {filters.skills.map((skill) => (
                <div key={skill} className="flex items-center bg-violet-500 text-white px-3 py-1 rounded-full">
                  {skill}
                  <button onClick={() => removeSkill(skill)} className="ml-2 text-white font-bold"> × </button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Locations Input */}
        <div className="filter-group mb-4">
          <h3 className="font-medium mb-2">Locations</h3>
          <div className="locations-input">
            <input
              type="text"
              value={locationInput}
              onChange={(e) => setLocationInput(e.target.value)}
              onKeyDown={handleLocationInput}
              placeholder="Type a location and press Enter"
              className="w-full p-2 border rounded"
            />
            <div className="flex flex-wrap gap-2 mt-2">
              {filters.locations.map((location) => (
                <div key={location} className="flex items-center bg-violet-500 text-white px-3 py-1 rounded-full">
                  {location}
                  <button onClick={() => removeLocation(location)} className="ml-2 mt-1 text-white font-bold"> ×</button>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Salary Range Slider */}
        <div className="filter-group mb-4">
          <h3 className="font-medium">Salary range</h3>
          <MultiRangeSlider
            className="slider-custom-class"
            style={sliderStyles}
            ruler="false"
            min={0}
            max={500000}
            step={100}
            minValue={minValue}
            maxValue={maxValue}
            label="false"
            barInnerColor="black"
            onInput={(e) => {
              handleInput(e);
            }}
          />
        </div>
        <div className="filter-group mb-4 flex justify-between">
          <div>Min : ${minValue}</div>
          <div>Max : ${maxValue}</div>
        </div>
        <button
          onClick={handleSearch}
          className="w-full bg-violet-500 text-white py-2 px-4 rounded mt-4 hover:bg-violet-600 cursor-pointer"
        >
          Apply Filters
        </button>
      </div>

         {/* Right Section for Job Cards */}
        { loader ? 
        ( <div className="flex items-center justify-center h-screen w-3/4">
            <ThreeDots visible={true} height="80" width="80" color="#4fa94d" radius="9" ariaLabel="three-dots-loading" wrapperStyle={{}} wrapperClass=""/>
          </div>) : (
         <div className="job-results w-3/4 px-4">
            { fetchedJobs?.length ? (
            fetchedJobs.map((jobs, idx) => (
              <div className="" key={idx}>
                <JobCard job={jobs} />
              </div>
               )))  : (<div className="flex items-center justify-center w-full h-screen">No jobs Found</div>)
            }
         </div>)
        }
    </div>
    </>
  );
};

export default App;
