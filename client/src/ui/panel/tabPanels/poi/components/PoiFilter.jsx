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
                key={`poi-district-list-${_label}`}
                className='checkbox-container'
                label={_label}
                sx={{
                    fontSize: 14,
                    margin: 0,
                    paddingY: '5px',
                    width: '50%',
                    boxSizing: 'border-box',
                }}
                control={
                    <Checkbox
                        key={_key}
                        name={String(_name)}
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




const PoiFilterDistrict = (props) => {
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



const PoiFilterType = (props) => {
    const {filterData, setCheck, ...other} = props;

    const handleChange = (event) => {

        for (let i = 0; i < filterData.poiType.length; i++) {
            if (filterData.poiType[i].type == event.target.name) {
                filterData.poiType[i] = {
                    ...filterData.poiType[i],
                    "select": event.target.checked
                }
                break;
            }
        }
        setCheck({...filterData});
    };

    const filterList = filterData.poiType.map((item) => {
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
        <div className='poi-filter-section'>
            <div className='poi-filter-section-column'>
                {...filterList}
            </div>
        </div>
    );
};




export function PoiFilter(props) {
    const {poiFilterData, setPoiFilterData, ...other} = props;

    const [isPoiFilterDistrictOpen, setIsPoiFilterDistrictOpen] = useState(false);
    const [isPoiFilterTypeOpen, setIsPoiFilterTypeOpen] = useState(false);

    return (
        <>
            <div id="PoiFilter">
                <div id="poi-filter-title">
                    <span>
                        Фильтры мест
                    </span>
                </div>

                {/* district */}
                <div
                    className='section-title'
                    onClick={() => setIsPoiFilterDistrictOpen(!isPoiFilterDistrictOpen)}
                >
                    {isPoiFilterDistrictOpen && (<KeyboardArrowDownIcon/>)}
                    {!isPoiFilterDistrictOpen && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Район</span>

                    <hr />
                </div>

                {isPoiFilterDistrictOpen && (<PoiFilterDistrict filterData={poiFilterData} setCheck={setPoiFilterData} />)}

                {/* type */}
                <div
                    className='section-title'
                    onClick={() => setIsPoiFilterTypeOpen(!isPoiFilterTypeOpen)}
                >
                    {isPoiFilterTypeOpen && (<KeyboardArrowDownIcon/>)}
                    {!isPoiFilterTypeOpen && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Типы мест</span>

                    <hr />
                </div>

                {isPoiFilterTypeOpen && (<PoiFilterType filterData={poiFilterData} setCheck={setPoiFilterData} />)}
            </div>
        </>
    )
};