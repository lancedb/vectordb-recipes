import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import {FeedbackProvider} from "./context/FeedBack.context"
createRoot(document.getElementById('root')).render(
  <StrictMode>
     <div className='bg-slate-300 p-6 pt-6'>
           <img
              src = "./assets/logo.svg"
              className="h-10 p-1"
              alt="Flowbite Logo"
            />
            <span>
              <div className="flex justify-center text-slate-950 text-3xl -mt-8">
                AI Powered Feedback-search and Analysis
              </div>
          </span>
      </div>
      <FeedbackProvider>
         <App />
      </FeedbackProvider>
  </StrictMode>,
)
