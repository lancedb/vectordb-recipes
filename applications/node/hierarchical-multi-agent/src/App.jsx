import { useState, useRef } from "react";
import ReactHtmlParser from "html-react-parser";
import DOMPurify from "dompurify";
import "./App.css";
import { CheckCircle,Pen ,Scales} from "phosphor-react";
import { Comment } from 'react-loader-spinner';
import GavelRoundedIcon from '@mui/icons-material/GavelRounded';

export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [finalResult, setFinalResult] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);
  let sanitizedContent;

  const handleQuery = async () => {
    if (!query.trim()) return;
    setLoading(true);

    try {
      const res = await fetch("http://localhost:5400/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();
      let lastMessageIndex = -1;
       setMessages([]);
       setFinalResult('');
      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          const chunk = decoder.decode(value, { stream: true });
          if (chunk.includes("Final result")) {
            sanitizedContent = DOMPurify.sanitize(chunk);
             sanitizedContent = sanitizedContent.replace(" ```html", "").trim();
            setFinalResult(sanitizedContent.replace("Final result:", "").trim());
          } else {
            messages.push({ text: chunk, sender: "bot" });
                setMessages((prev) =>
                    prev.map((msg, idx) =>
                        idx === lastMessageIndex ? { ...msg, status: "completed" } : msg
                    )
                );
                setMessages((prev) => {
                    lastMessageIndex = prev.length; // Update the last message index
                    return [...prev, { text: chunk, sender: "bot", status: "in-progress" }];
                });
          }
        }
      }
    } catch (error) {
      messages.push({ text: error, sender: "bot" });
      setMessages([...messages]);
    }
    setLoading(false);
  };

  return (
  <div className="bg-zinc-800 h-screen">
     <header className="w-full p-4 flex items-center justify-between">
      <img src="/assets/logo.svg" alt="Logo" className="h-10 p1" />
      <div className="w-10"></div> {/* Spacer */}
    </header>
   <div className="flex flex-col h-5/6 garamond-results garamond-corners garamond-corners-bottom mx-96 rounded-2xl">
        <div className="flex-1 overflow-y-auto p-6">
           <div className="garamond-results garamond-corners garamond-corners-bottom">
             <div className="garamond-content">
               <div className="garamond-title flex justify-center"><GavelRoundedIcon className="mr-6 gavel-color mt-1" fontSize="large" />AI Powered Law Assistant <Scales className="ml-4 mt-1" size={42} color="#8f4500" /></div>
              { finalResult !== '' ? (<>
                 <div className="garamond-ornament">——⚖️——</div>
                  {ReactHtmlParser(finalResult)} 
                   <div className="garamond-ornament">———○———</div>
                   </>
              ) : (
               <>
               {messages.map((msg, index) => (
                 <div key={index} className={`message p-2 rounded-md flex ${msg.status === "completed" ? "text-green-600" : "text-yellow-700"}`}>
                     {msg.status === "in-progress" && 
                     <span className="mr-3">
                         <Comment visible={true} height="30" width="30" ariaLabel="comment-loading" wrapperStyle={{}} wrapperClass="comment-wrapper" color="#000000" backgroundColor="#cb701a"/>
                     </span>}  
                      {msg.status === "completed" && <span><CheckCircle className="mr-4" size={24} color="#027a00" weight="bold" /> </span>}
                      {msg.text}
                 </div>
               ))}
              </>
               )
               }
             </div>
           </div>
        </div>

      {/* Input Box */}
        <div className="p-4 border-t border-zinc-600 bg-zinc-600 flex items-center rounded-2xl">
        <input
          type="text"
          className="flex-1 p-3 bg-zinc-600 text-white rounded-lg outline-none border border-zinc-600 focus:ring-2 focus:ring-zinc-600"
          placeholder="Send a message..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleQuery()}
        />
        <button
          onClick={handleQuery}
          disabled={loading}
          className="ml-3 px-4 py-2 bg-zinc-800 text-white rounded-lg disabled:opacity-50 hover:bg-zinc-900 cursor-pointer"
        >
          {loading ? "..." : "Search"}
        </button>
        </div>
    </div>
  </div>
  );
}
