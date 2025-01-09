import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { Briefcase} from "phosphor-react";


createRoot(document.getElementById('root')).render(
  <StrictMode>
     <div className='bg-violet-300 p-6 pt-6'>
           <img
              src = "./assets/logo.svg"
              className="h-10 p-1"
              alt="Flowbite Logo"
            />
            <span>
              <div className="flex justify-center text-violet-950 text-4xl -mt-8">
                AI Powered Job Search
                <Briefcase size={32} className="mt-1 ml-4" color="#4c1d95" />
              </div>
          </span>
      </div>
    <App />
  </StrictMode>,
)
