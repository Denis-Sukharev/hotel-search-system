import { getHolteAll } from '../../../../services/axiosConfig.js';
import testHotelList from '../testData/testHotelList.json';
import testPoiHotelFilter from '../testData/testPoiHotelFilter.json';

import './HotelTabPanel.css';
import { HotelFilter } from './components/HotelFilter.jsx';
import { HotelCard } from './components/HotelCard.jsx';

import { useState, useEffect, useMemo } from 'react';  

import TextField from '@mui/material/TextField';
import IconButton from '@mui/material/IconButton';
import Pagination from '@mui/material/Pagination';
import Stack from '@mui/material/Stack';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';
import Typography from '@mui/material/Typography';
import Skeleton from '@mui/material/Skeleton';

import FilterAltIcon from '@mui/icons-material/FilterAlt';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import AddLocationIcon from '@mui/icons-material/AddLocation';
import LocationOffIcon from '@mui/icons-material/LocationOff';

function HotelsTabpanel(props) {
    const {selectPointsData, setSelectPointsData} = props;

    const [hotelData, setHotelData] = useState([]);
    const [hotelCount, setHotelCount] = useState(0)

    const [hotelSearchValue, setHotelSearchValue] = useState('');
    const [hotelFilterData, setHotelFilterData] = useState(testPoiHotelFilter);
    const [hotelFilterOptimal, setHotelFilterOptimal] = useState(false);

    const [hotelTabPanelData, setHotelTabPanelData] = useState({
        isHotelFilterVisible: false,
        isSelectHotelVisible: false,
        isAllHotelVisible: true,
        page: 1
    });



    useEffect(() => {
        let body = {
            district: hotelFilterData.district.flatMap((item) => (item.select ? item.id : [])),
            type: hotelFilterData.hotelType.flatMap((item) => (item.select ? item.type : [])),
            rateMin: hotelFilterData.hotelRating[0],
            rateMax: hotelFilterData.hotelRating[1]
        }

        if (hotelFilterOptimal) {
            body.time_limit = 7;
            body.days = 1;
            body.points_sequence = selectPointsData.poi.map((item) => item.id);
            setHotelData([]);
            
        } else {
            body.page = hotelTabPanelData.page - 1;
            if (hotelSearchValue != '') {
                body.fragment = hotelSearchValue;
            }
        }

        getHolteAll(setHotelData, setHotelCount, body)
    }, [hotelTabPanelData.page, hotelFilterData, hotelSearchValue]);



    const hotelList = hotelData.map((hotelItem) => {
        return(
            <HotelCard
                hotelId={hotelItem.id}
                hotelName={hotelItem.name}
                // hotelDescription={poiItem.description}
                hotelImageUrl={hotelItem.photo != '' ? hotelItem.photo : '/logo/logo-img.png'}
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
                                        "photo": hotelItem.photo,
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
                hotelImageUrl={hotelItem.photo != '' ? hotelItem.photo : '/logo/logo-img.png'}
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
                        disabled={hotelFilterOptimal}
                        fullWidth
                        onChange={(event) => setHotelSearchValue(event.target.value)}
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
                

                <div>
                    <FormControlLabel
                        key={`hotel-optimal-switch`}
                        label={
                            <Typography fontSize={14} >
                                Подобрать на основе выбранных мест
                            </Typography>
                        }
                        sx={{
                            fontSize: 14,
                            margin: 0,
                            boxSizing: 'border-box',
                        }}
                        
                        control={
                            <Switch
                                size='medium'
                                checked={hotelFilterOptimal}
                                onChange={() => {
                                    if ((!hotelFilterOptimal && selectPointsData.poi.length > 0) || hotelFilterOptimal) {
                                        setHotelFilterOptimal(!hotelFilterOptimal);
                                        setHotelTabPanelData({
                                            ...hotelTabPanelData,
                                            isHotelFilterVisible: !hotelFilterOptimal ? true : hotelTabPanelData.isHotelFilterVisible,
                                            isAllHotelVisible: true,
                                            // 
                                    });
                                    }
                                }}
                            />
                        }
                    />
                </div>
                

                    
                {hotelTabPanelData.isHotelFilterVisible && (
                    <HotelFilter
                        hotelFilterData={hotelFilterData}
                        setHotelFilterData={setHotelFilterData}
                        hotelTabPanelData={hotelTabPanelData}
                        setHotelTabPanelData={setHotelTabPanelData}
                        hotelFilterOptimal={hotelFilterOptimal}
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
                
                {hotelList.length > 0 ? (<>
                    {hotelTabPanelData.isAllHotelVisible && (
                        <>
                            {...hotelList}

                            {hotelCount > 20 && !hotelFilterOptimal && (<div className='pagination-block'>
                                <Stack
                                    spacing={2}
                                    marginTop={'5px'}
                                    alignItems={'center'}
                                > 
                                    <Pagination
                                        size='small'
                                        count={Math.ceil(Number(hotelCount) / 20)}
                                        defaultPage={hotelTabPanelData.page}
                                        siblingCount={1}
                                        boundaryCount={1}
                                        onChange={(event, value) => {
                                            setHotelTabPanelData({
                                            ...hotelTabPanelData,
                                            page: value
                                            })
                                        }}
                                    />
                                </Stack>
                            </div>)}
                        </>
                    )}
                </>) : <><Skeleton variant="rectangular" fullWidth height={150} /><Skeleton variant="rectangular" fullWidth height={150} /></>}
            </div>
        </>
     );
}

export default HotelsTabpanel;