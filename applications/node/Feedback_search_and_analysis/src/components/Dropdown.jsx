import React, { useState } from "react";
import { ChevronDown } from "lucide-react"; // For dropdown icon

const users = [
  { userId: "1", name: "Alice" },
  { userId: "2", name: "Bob" },
  { userId: "3", name: "Charlie" },
  { userId: "4", name: "David" },
  { userId: "5", name: "Robert" },
  { userId: "6", name: "Max" },
];

const Dropdown = ({ selectedUser, setSelectedUser }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative w-full">
      {/* Dropdown Button */}
      <button
        className="p-3 w-full border-2 border-slate-400 rounded-lg bg-slate-100 shadow-lg text-xl text-slate-900 
                   flex justify-between items-center hover:bg-slate-200 transition duration-300"
        onClick={() => setIsOpen(!isOpen)}
      >
        {selectedUser ? users.find((user) => user.userId === selectedUser)?.name : "Select Employee"}
        <ChevronDown className="w-6 h-6 text-slate-700" />
      </button>

      {/* Dropdown Menu */}
      {isOpen && (
        <div className="absolute w-full mt-2 bg-white shadow-xl rounded-lg border border-slate-300 z-10">
          {users.map((user) => (
            <div
              key={user.userId}
              className="p-3 hover:bg-slate-300 hover:text-white cursor-pointer transition duration-300"
              onClick={() => {
                setSelectedUser(user.userId);
                setIsOpen(false);
              }}
            >
              {user.name}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Dropdown;
