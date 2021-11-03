import logo from './assets/searchLogo.png';
import './App.css';

function App() {
  return (
    <div className="App">
      <div className="background">
        <div className="inner-header">
          <img src={logo} className="logo" alt="Logo " />
          <div className="search-box">
            <p>Hello World</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
