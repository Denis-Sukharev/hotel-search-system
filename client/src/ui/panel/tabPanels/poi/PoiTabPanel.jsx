import './PoiTabPanel.css';
import { PoiFilter } from './components/PoiFilter';
import { PoiCard } from './components/PoiCard.jsx';
import testPoiList from './testPoiLis.json';

import {useState, useEffect} from 'react';  

import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';

import FilterAltIcon from '@mui/icons-material/FilterAlt';

function PoiTabPanel() {
    const [poiSearchValue, setPoiSearchValue] = useState('');
    const [poiFilterVisible, setPoiFilterVisible] = useState(false);

    return ( 
        <>
            <div id="PoiTabPanel">
                <div id="search-block">
                    <TextField
                        id="poi-search-text-field"
                        size="small"
                        placeholder="Хочу посетить"
                        value={poiSearchValue}
                        fullWidth
                        onChange={(event) => {
                            setPoiSearchValue(event.target.value);
                            //Запрос на сервер
                        }}
                        
                    />

                    <IconButton
                        size="large"
                        onClick={() => {
                            setPoiFilterVisible(!poiFilterVisible);
                        }}
                    >
                        <FilterAltIcon
                            fontSize="inherit"
                        />
                    </IconButton>
                </div>

                <PoiFilter
                    visible={poiFilterVisible}
                />

                <div id="select-poi-list">
                        
                </div>

                <div id="all-poi-list">
                    <PoiCard
                        poiId={testPoiList[0].id}
                        poiName={testPoiList[0].name}
                        poiDescription={testPoiList[0].description}
                        poiImageUrl={testPoiList[0].image}
                        poiType={testPoiList[0].type}
                        poiCoordX={testPoiList[0].x}
                        poiCoordY={testPoiList[0].y}
                        poiSet={false}
                    />
                </div>
            </div>
        </>
     );
}

export default PoiTabPanel;