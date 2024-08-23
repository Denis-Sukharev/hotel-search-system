import { useState } from 'react';

import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import Slider from '@mui/material/Slider';
import Chip from '@mui/material/Chip';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';

const CheckboxElement = (props) => {
    const {_label, _key, _name, _checked, _onChange, ...other} = props;

    return(
        <>
            <FormControlLabel
                key={`hotel-district-list-${_label}`}
                className='checkbox-container'
                label={
                    <Typography
                        fontSize={14}
                    >
                       {_label}
                    </Typography>
                }
                sx={{
                    fontSize: 14,
                    margin: 0,
                    paddingY: '5px',
                    width: '50%',
                    boxSizing: 'border-box',
                    lineHeight: '100%',
                }}
                control={
                    <Checkbox
                        key={_key}
                        name={_name}
                        size='medium'
                        checked={_checked}
                        onChange={_onChange}

                        sx={{
                            padding: 0
                        }}
                    />
                }
            />
        </>
    );
};




const HotelFilterDistrict = (props) => {
    const {filterData, setCheck, ...other} = props;

    const handleChange = (event) => {
        for (let i = 0; i < filterData.district.length; i++) {
            if (filterData.district[i].id == event.target.name) {
                filterData.district[i] = {
                    ...filterData.district[i],
                    "select": event.target.checked
                }
                break;
            }
        }
        setCheck({...filterData});
    };

    const filterList = filterData.district.map((item) => {
        return(
            <CheckboxElement
                _label={item.name}
                _key={item.id}
                _name={item.id}
                _checked={item.select}
                _onChange={handleChange}
            />
        )
    });

    return (
        <div className='poi-filter-section'>
            <div className='poi-filter-section-column'>
                {...filterList}
            </div>
        </div>
    );
};



const HotelFilterType = (props) => {
    const {filterData, setCheck, ...other} = props;

    const handleChange = (event) => {
        for (let i = 0; i < filterData.hotelType.length; i++) {
            if (filterData.hotelType[i].type == event.target.name) {
                filterData.hotelType[i] = {
                    ...filterData.hotelType[i],
                    "select": event.target.checked
                }
                break;
            }
        }
        setCheck({...filterData});
    };

    const filterList = filterData.hotelType.map((item) => {
        return(
            <CheckboxElement
                _label={item.name}
                _key={item.type}
                _name={item.type}
                _checked={item.select}
                _onChange={handleChange}
            />
        )
    });

    return (
        <div className='hotel-filter-section'>
            <div className='hotel-filter-section-column'>
                {...filterList}
            </div>
        </div>
    );
};





const HotelFilterRating = (props) => {
    const {filterData, setCheck, ...other} = props;
    const [value, setValue] = useState(filterData.hotelRating)

    const sliderChange = (event, newValue) => {
        setValue(newValue);
        setCheck({
            ...filterData,
            hotelRating : [Number(newValue[0]), Number(newValue[1])]
        });
    };

    return (
        <div className='hotel-filter-section'>
            <div className='hotel-filter-section-column hotel-filter-section-column-padding'>
                <Chip
                    label={String(filterData.hotelRating[0])}
                    variant="outlined"
                />

                <Slider
                    getAriaLabel={() => 'Temperature range'}
                    value={value}
                    step={1}
                    min={0}
                    max={10}
                    onChange={sliderChange}
                    valueLabelDisplay="auto"
                    getAriaValueText={() => value}
                    // marks={[
                    //     {value: 0, label: "0"}, {value: 1, label: "1"},
                    //     {value: 2, label: "2"}, {value: 3, label: "3"},
                    //     {value: 4, label: "4"}, {value: 5, label: "5"},
                    //     {value: 6, label: "6"}, {value: 7, label: "7"},
                    //     {value: 8, label: "8"}, {value: 9, label: "9"},
                    //     {value: 10, label: "10"}
                    // ]}
                />

                <Chip
                    label={String(filterData.hotelRating[1])}
                    variant="outlined"
                />
            </div>
        </div>
    );
};





export function HotelFilter(props) {
    const {
        hotelFilterData,
        setHotelFilterData,
        hotelTabPanelData,
        setHotelTabPanelData,
        ...other} = props;

    const [hotelFilter, setHotelFilter] = useState({
        district: hotelFilterData.district,
        hotelType: hotelFilterData.hotelType,
        hotelRating: hotelFilterData.hotelRating
    })

    const [isHotelFilterDistrictOpen, setIsHotelFilterDistrictOpen] = useState(false);
    const [isHotelFilterTypeOpen, setIsHotelFilterTypeOpen] = useState(false);
    const [isHotelFilterRatingOpen, setIsHotelFilterRatingOpen] = useState(false);

    return (
        <>
            <div id="HotelFilter">
                <div id="hotel-filter-section">
                    <span>
                        Фильтры мест
                    </span>
                </div>

                {/* district */}
                <div
                    className='section-title'
                    onClick={() => setIsHotelFilterDistrictOpen(!isHotelFilterDistrictOpen)}
                >
                    {isHotelFilterDistrictOpen && (<KeyboardArrowDownIcon/>)}
                    {!isHotelFilterDistrictOpen && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Район</span>

                    <hr />
                </div>

                {isHotelFilterDistrictOpen && (<HotelFilterDistrict filterData={hotelFilter} setCheck={setHotelFilter} />)}

                {/* type */}
                <div
                    className='section-title'
                    onClick={() => setIsHotelFilterTypeOpen(!isHotelFilterTypeOpen)}
                >
                    {isHotelFilterTypeOpen && (<KeyboardArrowDownIcon/>)}
                    {!isHotelFilterTypeOpen && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Типы гостиниц</span>

                    <hr />
                </div>

                {isHotelFilterTypeOpen && (<HotelFilterType filterData={hotelFilter} setCheck={setHotelFilter} />)}

                {/* rating */}
                <div
                    className='section-title'
                    onClick={() => setIsHotelFilterRatingOpen(!isHotelFilterRatingOpen)}
                >
                    {isHotelFilterRatingOpen && (<KeyboardArrowDownIcon/>)}
                    {!isHotelFilterRatingOpen && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Рейтинг гостиниц</span>

                    <hr />
                </div>

                {isHotelFilterRatingOpen && (<HotelFilterRating filterData={hotelFilter} setCheck={setHotelFilter} />)}

                <Button
                    onClick={() => {
                        setHotelFilterData({
                        ...hotelFilterData,
                        district: hotelFilter.district,
                        hotelType: hotelFilter.hotelType,
                        hotelRating: hotelFilter.hotelRating
                        })
                        
                        setHotelTabPanelData({
                            ...hotelTabPanelData,
                            page: 1
                        })
                    }}
                    variant='contained'
                    size='small'
                    fullWidth
                    sx={{
                        marginTop: 1,
                    }}
                >
                    Применить фильтры
                </Button>
            </div>
        </>
    )
};