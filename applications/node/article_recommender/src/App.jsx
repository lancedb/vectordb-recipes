import { useState, useEffect } from 'react';
import axios from 'axios';

// Components
import SearchBar from './components/SearchBar';
import PillBar from './components/PillBar';
import ArticleCard from './components/ArticleCard';
import Loader from './components/Loader';

// Styles
import './App.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [articles, setArticles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchArticles = async () => {
      if (searchQuery.trim() !== '') {
        setIsLoading(true);
        try {
          const response = await axios.post('http://localhost:5300/api/articles', {
            text: searchQuery, // Send the search query in the body
          });
          setArticles(response.data.result || []); // Assuming the server returns `result` in the response
        } catch (error) {
          console.error('Error fetching articles:', error);
        }
        setIsLoading(false);
      }
    };

    fetchArticles();
  }, [searchQuery]); // Fetch articles when `searchQuery` changes

  return (
    <div className="App">
      <div className='bg-gray-100'>
        <img
              src = "./assets/logo.svg"
              className="h-10 p-1"
              alt="Flowbite Logo"
            />
      </div>
      <div className="bg-gray-100 h-screen flex flex-col items-center justify-center">
        <h1 className="text-3xl text-gray-800 text-center flex">
         <div className='mx-2'>
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-10 text-sky-400">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 7.5h1.5m-1.5 3h1.5m-7.5 3h7.5m-7.5 3h7.5m3-9h3.375c.621 0 1.125.504 1.125 1.125V18a2.25 2.25 0 0 1-2.25 2.25M16.5 7.5V18a2.25 2.25 0 0 0 2.25 2.25M16.5 7.5V4.875c0-.621-.504-1.125-1.125-1.125H4.125C3.504 3.75 3 4.254 3 4.875V18a2.25 2.25 0 0 0 2.25 2.25h13.5M6 7.5h3v3H6v-3Z" />
            </svg>
          </div>
          <div className="font-bold text-4xl">Article Recommender</div>
        </h1>
        <div className="relative z-10 w-full max-w-4xl px-4 sm:px-6 lg:px-8 overflow-auto mt-8">
          <SearchBar onSearch={setSearchQuery} externalQuery={searchQuery} />
          <PillBar onCategoryClick={setSearchQuery} />
          {isLoading ? (
            <Loader />
          ) : (
            <div className="mt-8 grid grid-cols-1 gap-6">
              {articles.map((article) => (
                <ArticleCard
                  url={article.url}
                  author={article.author}
                  key={article.id}
                  title={article.title}
                  content={article.content}
                  date={article.date}
                  publisher={article.publisher}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
