import './App.css';
import MapLayer from './map/MapLayer.jsx';
// import Ui from './ui/Ui.jsx'

import { useState } from 'react';

function App() {
  const [tabValue, setTabValue] = useState(0);

  const [selectPointsData, setSelectPointsData] = useState({
    poi: [],
    hotels: [],
    routes: [],
  });

  return (
    <>
      <div id="App">
        {/* <Ui /> */}
        <MapLayer
          selectPointsData={selectPointsData}
          setSelectPointsData={setSelectPointsData}
          tabValue={tabValue}
          setTabValue={setTabValue}
          
        />
      </div>
    </>
  );
}

export default App;
