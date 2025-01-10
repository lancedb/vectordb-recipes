import React, { useState } from "react";
import { Buildings ,ArrowSquareOut} from "phosphor-react";


const JobCard = ({ job }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const jobDescription = job["Job Description"];
  const website = job["Company Profile"] ? JSON.parse(job["Company Profile"]) : null;
  const fullUrl = website?.Website.startsWith('http') ? website?.Website : `http://${website?.Website}`;

  const toggleDescription = () => {
    setIsExpanded((prev) => !prev);
  };

  return (
    <div className="border rounded-lg shadow-sm hover:shadow-lg p-4 flex flex-row items-start space-y-2 bg-gray-200">
      {/* Left Section: Company Logo */}
      <div className="w-1/5 mt-12">
        <Buildings size={32} color="#6d28d9"/>
        <p>{job["Company"]}</p>
      </div>

      {/* Middle Section: Job Details */}
      <div className="w-3/5">
        <h2 className="text-xl font-semibold">{job["Job Title"]}</h2>

        {/* Job Description */}
        <div className="text-gray-600 text-sm mb-2">
          <strong className="text-black">Description:</strong>
          <span
            className={isExpanded ? "" : "line-clamp-3"}
            dangerouslySetInnerHTML={{
              __html: jobDescription,
            }}
          />
          {job["Responsibilities"]}
          <button
            onClick={toggleDescription}
            className="text-blue-500 text-sm font-medium mt-2 flex justify-end"
          >
          </button>
        </div>
         <p className="text-gray-600">
          <strong className="text-black">Skills:</strong> {job.skills}, {job.Country}
        </p>
         <p className="text-gray-600">
          <strong className="text-black">Experience:</strong> {job.Experience}
        </p>

        <p className="text-gray-600">
          <strong className="text-black">Location:</strong> {job.location}, {job.Country}
        </p>
        <p className="text-gray-600">
          <strong className="text-black">Salary:</strong> {job["Salary Range"]}
        </p>
        <div className="flex flex-wrap gap-2 mt-2">{job.Categories}</div>
      </div>

      {/* Right Section: Apply Button */}
      <div className="w-1/5">
        { !(website === null) ? (
           <a
          href={fullUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 bg-violet-500 text-white text-sm font-medium py-2 px-4 cursor-pointer rounded hover:bg-violet-600 flex items-center justify-center gap-2 w-8/12"
        >
          <span>Apply Now</span>
          <ArrowSquareOut size={16} color="white" />
        </a>
        ) : (<p className="mt-4 bg-violet-500 text-white text-sm font-medium py-2 px-4 cursor-pointer rounded hover:bg-violet-600 flex items-center justify-center gap-2 w-8/12"><span>No Link</span></p>)
        }
      </div>
    </div>
  );
};

export default JobCard;
