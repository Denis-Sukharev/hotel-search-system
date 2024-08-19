import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';

import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import { useState } from 'react';

const CheckboxElement = (props) => {
    const {_label, _key, _name, _checked, _onChange, ...other} = props;

    return(
        <>
            <FormControlLabel
                key={`hotel-district-list-${_label}`}
                className='checkbox-container'
                label={_label}
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




export function HotelFilter(props) {
    const {hotelFilterData, setHotelFilterData, ...other} = props;

    const [isHotelFilterDistrictOpen, setIsHotelFilterDistrictOpen] = useState(false);
    const [isHotelFilterTypeOpen, setIsHotelFilterTypeOpen] = useState(false);

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

                {isHotelFilterDistrictOpen && (<HotelFilterDistrict filterData={hotelFilterData} setCheck={setHotelFilterData} />)}

                {/* type */}
                <div
                    className='section-title'
                    onClick={() => setIsHotelFilterTypeOpen(!isHotelFilterTypeOpen)}
                >
                    {isHotelFilterTypeOpen && (<KeyboardArrowDownIcon/>)}
                    {!isHotelFilterTypeOpen && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Типы мест</span>

                    <hr />
                </div>

                {isHotelFilterTypeOpen && (<HotelFilterType filterData={hotelFilterData} setCheck={setHotelFilterData} />)}
            </div>
        </>
    )
};