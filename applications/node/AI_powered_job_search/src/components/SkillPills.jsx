// SkillPill.js
import React from "react";
import "../App.css"

const SkillPill = ({ skill, onClick }) => {
  return (
    <button className="skill-pill bg-violet-500" onClick={onClick}>
      {skill}
    </button>
  );
};

export default SkillPill;