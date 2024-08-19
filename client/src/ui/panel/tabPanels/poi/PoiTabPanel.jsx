import testPoiList from '../testData/testPoiList.json';
import testPoiHotelFilter from '../testData/testPoiHotelFilter.json';

import './PoiTabPanel.css';
import { PoiFilter } from './components/PoiFilter';
import { PoiCard } from './components/PoiCard.jsx';

import {useState} from 'react';  

import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';

import FilterAltIcon from '@mui/icons-material/FilterAlt';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import AddLocationIcon from '@mui/icons-material/AddLocation';
import LocationOffIcon from '@mui/icons-material/LocationOff';


function PoiTabPanel(props) {
    const {selectPointsData, setSelectPointsData} = props;

    const [poiData, setPoiList] = useState(testPoiList.poi);
    const [poiCount, setPoiCount] = useState(Math.floor(Number(testPoiList.count) / 20))

    const [poiSearchValue, setPoiSearchValue] = useState('');
    const [poiFilterData, setPoiFilterData] = useState(testPoiHotelFilter);


    const [poiTabPanelData, setPoiTabPanelData] = useState({
        isPoiFilterVisible: false,
        isSelectPoiVisible: true,
        isAllPoiVisible: true,
        page: 1
    });
    

    const poiList = poiData.map((poiItem) => {
        return(
            <PoiCard
                poiId={poiItem.id}
                poiName={poiItem.name}
                // poiDescription={poiItem.description}
                // poiImageUrl={poiItem.image}
                poiType={poiItem.type}
                poiCoordX={poiItem.latitude}
                poiCoordY={poiItem.longitude}
                cardButton={() => {return(<AddLocationIcon fontSize='large'/>)}}
                cardButtonColor='success'
                changePoi={() => {
                    if (selectPointsData.poi.length < 9) {
                        let isPoiSelect = false;

                        selectPointsData.poi.map((selectPoi) => {
                            if (selectPoi.id == poiItem.id) {
                                isPoiSelect = true;
                            }
                        })

                        if (!isPoiSelect) {
                            setSelectPointsData({
                                ...selectPointsData,
                                poi: [
                                    ...selectPointsData.poi,
                                    {
                                        "id": poiItem.id,
                                        "name": poiItem.name,
                                        // "description": poiItem.description,
                                        // "image": poiItem.image,
                                        "type": poiItem.type,
                                        "latitude": poiItem.latitude,
                                        "longitude": poiItem.longitude
                                    }
                                ]
                            })
                        }
                    }
                }}
            />
        );
    });


    const selectPoiList = selectPointsData.poi.map((poiItem) => {
        return(
            <PoiCard
                poiId={poiItem.id}
                poiName={poiItem.name}
                // poiDescription={poiItem.description}
                // poiImageUrl={poiItem.image}
                poiType={poiItem.type}
                poiCoordX={poiItem.latitude}
                poiCoordY={poiItem.longitude}
                cardButton={() => {return(<LocationOffIcon fontSize='large'/>)}}
                cardButtonColor='error'
                changePoi={() => {
                    selectPointsData.poi.forEach((item, index) => {
                        if (item.id == poiItem.id) {
                            selectPointsData.poi.splice(index, 1);
                        };
                    });

                    setSelectPointsData({...selectPointsData});
                }}
            />
        );
    });

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
                            setPoiTabPanelData({
                                ...poiTabPanelData,
                                isPoiFilterVisible: !poiTabPanelData.isPoiFilterVisible
                            });
                        }}
                    >
                        <FilterAltIcon
                            fontSize="inherit"
                        />
                    </IconButton>
                </div>
                
                {poiTabPanelData.isPoiFilterVisible && (
                    <PoiFilter
                    poiFilterData={poiFilterData}
                    setPoiFilterData={setPoiFilterData}
                    />
                )}

                <div
                    className='section-title'
                    onClick={() => setPoiTabPanelData({
                        ...poiTabPanelData,
                        isSelectPoiVisible: !poiTabPanelData.isSelectPoiVisible
                    })}
                >
                    {poiTabPanelData.isSelectPoiVisible && (<KeyboardArrowDownIcon/>)}
                    {!poiTabPanelData.isSelectPoiVisible && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Выбранные места</span>

                    <hr />

                    <span>{selectPointsData.poi.length}/9</span> 
                </div>

                {poiTabPanelData.isSelectPoiVisible && (
                    <>
                        {...selectPoiList}
                    </>
                )}

                <div
                    className='section-title'
                    onClick={() => setPoiTabPanelData({
                        ...poiTabPanelData,
                        isAllPoiVisible: !poiTabPanelData.isAllPoiVisible
                    })}
                >
                    {poiTabPanelData.isAllPoiVisible && (<KeyboardArrowDownIcon/>)}
                    {!poiTabPanelData.isAllPoiVisible && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Все места</span>

                    <hr />
                </div>

                {poiTabPanelData.isAllPoiVisible && (
                    <>
                        {...poiList}

                        <div className='pagination-block'>
                            <Stack
                                spacing={2}
                                marginTop={'5px'}
                                alignItems={'center'}
                            > 
                                <Pagination
                                    size='small'
                                    count={poiCount}
                                    defaultPage={poiTabPanelData.page}
                                    siblingCount={1}
                                    boundaryCount={1}
                                    onChange={(event, value) => setPoiTabPanelData({
                                        ...poiTabPanelData,
                                        page: value
                                    })}
                                />
                            </Stack>
                        </div>
                    </>
                )}
            </div>
        </>
     );
}

export default PoiTabPanel;