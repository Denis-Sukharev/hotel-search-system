import './PoiTabPanel.css';
import testPoiList from './testPoiLis.json';

import {useState, useEffect} from 'react';  

import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Chip from '@mui/material/Chip';

import FilterAltIcon from '@mui/icons-material/FilterAlt';
import AddLocationIcon from '@mui/icons-material/AddLocation';
import LocationOffIcon from '@mui/icons-material/LocationOff';

// const [poiList, setPoiList] = useState([{}]);

const PoiCard = (props) => {
    const {poiId, poiName, poiDescription, poiImageUrl, poiType, poiCoordX, poiCoordY, poiSet} = props;
    
    return (
        <>
            <div className='PoiCard' id={"poi-card"+poiId}>
                <img src={poiImageUrl} alt={poiName}/>

                <div className="poi-card-content">
                    <div className="poi-card-header">
                        <div className="poi-card-name">
                            <span>{poiName}</span>
                        </div>

                        <IconButton
                            size='large'
                        >   
                            {poiSet && <AddLocationIcon fontSize='inherit'/>}
                            {!poiSet && <LocationOffIcon fontSize='inherit'/>}                            
                        </IconButton>
                    </div>

                    <div className="poi-card-description">
                        <div>
                            <p>
                                {poiDescription}
                            </p>
                        </div>
                        
                        <div>
                            <Chip
                                label={poiType}
                                variant='outlined'
                                size='small'
                            />
                        </div>
                        
                        <div>
                            <p>
                            X: {poiCoordX} Y: {poiCoordY} 
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};

const PoiFilter = (props) => {
    const {visible, ...other} = props;

    return (
        <>
            {visible === true && (
                <div if="Poifilter">
                    фильтр
                </div>
            )}
        </>
    )
};

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
                            console.log(testPoiList);
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