import React, { useState, useEffect } from 'react';
import logo from './assets/searchLogo.png';
import './App.css';
import Checkbox from './components/Checkbox';
import SearchBar from './components/SearchBar';

function App() {

  const [query, setQuery] = useState('');
  const [stopwords, setStopwords] = useState(false);
  const [stemming, setStemming] = useState(false);
  const [fetching, setFetching] = useState(false);

  const [data, setData] = useState(null);

  const updateInput = async (input) => {
    setQuery(input);
 }

 const onSubmit = async (event) => {
   event.preventDefault();
   console.log(query);
   console.log(stopwords);
   console.log(stemming);
      
   // reset 
   setQuery("");
   setStopwords(false);
   setStemming(false);
 }

  return (
    <div className="App">
      <div className="background">
        <div className="inner-header">
          <img src={logo} className="logo" alt="Logo " />
          <h1>CACM Search Engine</h1>
          <div className="search-box">
            <SearchBar 
              query={query}
              setQuery={updateInput}
              onSubmit={onSubmit}
            />
            <Checkbox 
              label="Stop Words" 
              isChecked={stopwords}
              setIsChecked={setStopwords}
            />
            <Checkbox
              label="Stemming" 
              isChecked={stemming}
              setIsChecked={setStemming}
            />
          </div>
        </div>
        <div className="loading-indicator">

        </div>
      </div>
    </div>
  );
}

export default App;
