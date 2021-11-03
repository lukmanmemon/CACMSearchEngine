
import React from 'react';
import './Searchbar.scss'

const SearchBar = ({query,setQuery,onSubmit}) => {
  return (
  <form type="search" onSubmit={onSubmit} role="search">
    <input id="search" type="search" value={query} placeholder="Search Query..." onChange={(e) => setQuery(e.target.value)} autoFocus required />
    <button type="search">Go</button>    
</form>
  );
}

export default SearchBar