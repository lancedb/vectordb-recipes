import React, {useState} from "react";
import Select from 'react-select';
import {setSelectedModelInStore} from './store'

function NavBar() {
    const options = [{
        value: 'gpt-4',
        label: 'GPT-4'
      },
      {
        value: 'gpt-4o-mini',
        label: 'GPT-4o-mini'
      },
    ];
    const [selectedModel, setSelectedModel] = useState(options[1]);
    const handleDropdownChange = (event) => {
      setSelectedModel(event);
      console.log("Selected model:", event.value);
      setSelectedModelInStore(event.value) // Dispatch the action to update the selected model
    }

  return (
    <div>
      <nav className="border-gray-200 bg-slate-950">
        <div className="flex flex-wrap  justify-between mx-auto p-4">
          <a
            href="https://flowbite.com/"
            className="flex space-x-3 rtl:space-x-reverse"
          >
            <img
              src = "./assets/logo.svg"
              className="h-8 p-1"
              alt="Flowbite Logo"
            />
          </a>
          <button
            data-collapse-toggle="navbar-default"
            type="button"
            className="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
            aria-controls="navbar-default"
            aria-expanded="false"
          >
            <span className="sr-only">Open main menu</span>
            <svg
              className="w-5 h-5"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 17 14"
            >
              <path
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M1 1h15M1 7h15M1 13h15"
              />
            </svg>
          </button>
          <div className="hidden w-full md:block md:w-auto" id="navbar-default">
            <ul className="font-medium flex flex-col p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:flex-row md:space-x-8 rtl:space-x-reverse md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700"></ul>
          </div>
          <div className="w-60">
            <Select
            value = {selectedModel}
            onChange = {handleDropdownChange}
            options={options}
          />
          </div>
        </div>
      </nav>
    </div>
  );
}

export default NavBar;
