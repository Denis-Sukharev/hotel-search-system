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
                    fontSize: 14
                }}
                control={
                    <Checkbox
                        key={_key}
                        name={_name}
                        size='small'
                        checked={_checked}
                        onChange={_onChange}

                        sx={{
                            paddingTop: 0,
                            paddingBottom:0
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
        filterData.district.forEach((item, index) => {
            if (index == event.target.name) {
                filterData.district[event.target.name] = {
                    ...filterData.district[event.target.name],
                    "select": event.target.checked
                }
            };
        })

        setCheck({...filterData});
    };

    const filterList = filterData.district.map((item, index) => {
        return(
            <CheckboxElement
                _label={item.name}
                _key={index}
                _name={index}
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
        filterData.type.forEach((item, index) => {
            if (index == event.target.name) {
                filterData.type[event.target.name] = {
                    ...filterData.type[event.target.name],
                    "select": event.target.checked
                }
            };
        })

        setCheck({...filterData});
    };

    const filterList = filterData.type.map((item, index) => {
        return(
            <CheckboxElement
                _label={item.name}
                _key={index}
                _name={index}
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



const PoiFilterCategory = (props) => {
    const {filterData, setCheck, ...other} = props;
    const handleChange = (event) => {
        filterData.type.forEach((item, index) => {
            if (index == event.target.name) {
                filterData.type[event.target.name] = {
                    ...filterData.type[event.target.name],
                    "select": event.target.checked
                }
            };
        })

        setCheck({...filterData});
    };

    const filterList = filterData.category.map((item, index) => {
        return(
            <CheckboxElement
                _label={item.name}
                _key={index}
                _name={index}
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

    const [isPoiFilterDistrictOpen, setIsPoiFilterDistrictOpen] = useState('false');
    const [isPoiFilterTypeOpen, setIsPoiFilterTypeOpen] = useState('false');
    const [isPoiFilterCategoryOpen, setIsPoiFilterCategoryOpen] = useState('false');

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

                {/* category */}
                <div
                    className='section-title'
                    onClick={() => setIsPoiFilterCategoryOpen(!isPoiFilterCategoryOpen)}
                >
                    {isPoiFilterCategoryOpen && (<KeyboardArrowDownIcon/>)}
                    {!isPoiFilterCategoryOpen && (<KeyboardArrowUpIcon/>)}
                    
                    <span>Категории мест</span>

                    <hr />
                </div>

                {isPoiFilterCategoryOpen && (<PoiFilterCategory filterData={poiFilterData} setCheck={setPoiFilterData} />)}
            </div>
        </>
    )
};