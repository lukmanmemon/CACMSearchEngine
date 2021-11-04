import React, { useState } from 'react';
import logo from './assets/searchLogo.png';
import loading from './assets/loading.gif'
import './App.css';
import Checkbox from './components/Checkbox';
import SearchBar from './components/SearchBar';

function App() {

  const [query, setQuery] = useState('');
  const [stopwords, setStopwords] = useState(false);
  const [stemming, setStemming] = useState(false);
  const [fetching, setFetching] = useState(false);

  const [data, setData] = useState(null);

  const colours = ['#D1E7FE','#F3D9FF','#C4D0FB','#BAF1E3']

  const updateInput = async (input) => {
    setQuery(input);
 }

 const fetchData = (toggleStop, toggleStem) => {
   const fetchString = "http://localhost:8000/search/?query=" + query + "&stemming=" + toggleStem + "&stopwords=" + toggleStop; 
   console.log(fetchString);
  fetch(fetchString, {mode: 'cors'})
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      setData(data);
    })
    .catch((error) => {
      console.log(error);
    })
    .finally(() => {
      setFetching(false);
    });
};

 const onSubmit = async (event) => {
   event.preventDefault();
   setFetching(true);
   setData(null);
   const toggleStop = stopwords ? "ON" : "OFF";
   const toggleStem = stemming ? "ON" : "OFF";
   fetchData(toggleStop, toggleStem);
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
        { fetching && 
           <div className="loading-indicator">
           <img src={loading} className="logo" alt="Logo " />
          </div>
        }
        {data !== null && 
          <p>Top 10 Results ({data['Time']} seconds)</p>
        }
        {data !== null &&
         Object.keys(data).map((type) => {
           if (type !== "Time") {
            console.log(type)
            console.log(colours[(type % (colours.length - 1))])
            return (
                <div className="data-card" style={{"background": colours[(type % (colours.length - 1))]}}>
                  <p>Rank: {data[type]["Rank"]}</p>
                  <p>Title: {data[type]["Title"]}</p>
                  <p>Author(s): {data[type]["Author(s)"]}</p>
                  <p>Document: {data[type]["Document"]}</p>
                  <p>Score: {data[type]["Score"]}</p>
                </div>
            ) 
           }
      })
        }
      </div>
    </div>
  );
}

export default App;
