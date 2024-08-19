import testHotelList from '../testData/testHotelList.json';
import testPoiHotelFilter from '../testData/testPoiHotelFilter.json';

import './HotelTabPanel.css';
import { HotelFilter } from './components/HotelFilter.jsx';
import { HotelCard } from './components/HotelCard.jsx';

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

function HotelsTabpanel(props) {
    const {selectPointsData, setSelectPointsData} = props;

    const [hotelData, setHotelData] = useState(testHotelList.hotels);
    const [hotelCount, setHotelCount] = useState(Math.floor(Number(testHotelList.count) / 20))

    const [hotelSearchValue, setHotelSearchValue] = useState('');
    const [hotelFilterData, setHotelFilterData] = useState(testPoiHotelFilter);

    const [hotelTabPanelData, setHotelTabPanelData] = useState({
        isHotelFilterVisible: false,
        isSelectHotelVisible: true,
        isAllHotelVisible: true,
        page: 1
    });
    

    const hotelList = hotelData.map((hotelItem) => {
        return(
            <HotelCard
                hotelId={hotelItem.id}
                hotelName={hotelItem.name}
                // hotelDescription={poiItem.description}
                // hotelImageUrl={poiItem.image}
                hotelType={hotelItem.type}
                hotelRating={hotelItem.rating}
                hotelCoordX={hotelItem.latitude}
                hotelCoordY={hotelItem.longitude}
                cardButton={() => {return(<AddLocationIcon fontSize='large'/>)}}
                cardButtonColor='success'
                changeHotel={() => {
                    if (selectPointsData.hotels.length < 3) {
                        let isHotelSelect = false;

                        selectPointsData.hotels.map((selectHotel) => {
                            if (selectHotel.id == hotelItem.id) {
                                isHotelSelect = true;
                            }
                        })

                        if (!isHotelSelect) {
                            setSelectPointsData({
                                ...selectPointsData,
                                hotels: [
                                    ...selectPointsData.hotels,
                                    {
                                        "id": hotelItem.id,
                                        "name": hotelItem.name,
                                        // "description": hotelItem.description,
                                        // "image": hotelItem.image,
                                        "type": hotelItem.type,
                                        "rating": hotelItem.rating,
                                        "latitude": hotelItem.latitude,
                                        "longitude": hotelItem.longitude
                                    }
                                ]
                            })
                        }
                    }
                }}
            />
        );
    });


    const selectHotelList = selectPointsData.hotels.map((hotelItem) => {
        return(
            <HotelCard
                hotelId={hotelItem.id}
                hotelName={hotelItem.name}
                // hotelDescription={poiItem.description}
                // hotelImageUrl={poiItem.image}
                hotelType={hotelItem.type}
                hotelRating={hotelItem.rating}
                hotelCoordX={hotelItem.latitude}
                hotelCoordY={hotelItem.longitude}
                cardButton={() => {return(<LocationOffIcon fontSize='large'/>)}}
                cardButtonColor='error'
                changeHotel={() => {
                    selectPointsData.hotels.forEach((item, index) => {
                        if (item.id == hotelItem.id) {
                            selectPointsData.hotels.splice(index, 1);   
                        };
                    });

                    setSelectPointsData({...selectPointsData});
                }}
            />
        );
    });

    return ( 
        <>
            <div id="HotelTabPanel">
                <div id="search-block">
                    <TextField
                        id="hotel-search-text-field"
                        size="small"
                        placeholder="Хочу посетить"
                        value={hotelSearchValue}
                        fullWidth
                        onChange={(event) => {
                            setHotelSearchValue(event.target.value);
                            //Запрос на сервер
                        }}
                    />

                    <IconButton
                        size="large"
                        onClick={() => {
                            setHotelTabPanelData({
                                ...hotelTabPanelData,
                                isHotelFilterVisible: !hotelTabPanelData.isHotelFilterVisible
                            });
                        }}
                    >
                        <FilterAltIcon
                            fontSize="inherit"
                        />
                    </IconButton>
                </div>
                
                {hotelTabPanelData.isHotelFilterVisible && (
                    <HotelFilter
                        hotelFilterData={hotelFilterData}
                        setHotelFilterData={setHotelFilterData}
                    />
                )}

                <div
                    className='section-title'
                    onClick={() => setHotelTabPanelData({
                        ...hotelTabPanelData,
                        isSelectHotelVisible: !hotelTabPanelData.isSelectHotelVisible
                    })}
                >
                    {hotelTabPanelData.isSelectHotelVisible && (<KeyboardArrowDownIcon/>)}
                    {!hotelTabPanelData.isSelectHotelVisible && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Выбранные отели</span>

                    <hr />

                    <span>{selectPointsData.hotels.length}/3</span> 
                </div>

                {hotelTabPanelData.isSelectHotelVisible && (
                    <>
                        {...selectHotelList}
                    </>
                )}

                <div
                    className='section-title'
                    onClick={() => setHotelTabPanelData({
                        ...hotelTabPanelData,
                        isAllHotelVisible: !hotelTabPanelData.isAllHotelVisible
                    })}
                >
                    {hotelTabPanelData.isAllHotelVisible && (<KeyboardArrowDownIcon/>)}
                    {!hotelTabPanelData.isAllHotelVisible && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Все отели</span>

                    <hr />
                </div>

                {hotelTabPanelData.isAllHotelVisible && (
                    <>
                        {...hotelList}

                        <div className='pagination-block'>
                            <Stack
                                spacing={2}
                                marginTop={'5px'}
                                alignItems={'center'}
                            > 
                                <Pagination
                                    size='small'
                                    count={hotelCount}
                                    defaultPage={hotelTabPanelData.page}
                                    siblingCount={1}
                                    boundaryCount={1}
                                    onChange={(event, value) => setHotelTabPanelData({
                                        ...hotelTabPanelData,
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

export default HotelsTabpanel;