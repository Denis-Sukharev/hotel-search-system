import testPoiFilter from '../testPoiFilter.json';

import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';

import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import { useState } from 'react';



const PoiFilterDistrict = (props) => {
    const {filterData, setCheck, ...other} = props;
    const handleChange = (event) => {
        setCheck({
            ...filterData,
            district: {
                ...filterData.district,
                [event.target.name]: event.target.checked,
            }
        });
    };

    const filterList = Object.entries(filterData.district).map((value) => {
        return(
            <FormControlLabel
                key={`poi-district-list-${value[0]}`}
                className='checkbox-container'
                label={value[0]} 
                control={
                    <Checkbox
                        key={`poi-district-list-checkbox-${value[0]}`}
                        name={value[0]}
                        size='small'
                        checked={value[1]}
                        onChange={handleChange}
                        defaultChecked
                    />
                }
            />
        );
    });

    return (
        <div className='poi-filter-section'>
            <div className='poi-filter-section-column'>
                {...filterList}
            </div>

            {/* <div className='poi-filter-section-column'>
                
            </div> */}
        </div>
    );
};



const PoiFilterType = (props) => {
    const {filterData, setCheck, ...other} = props;
    const handleChange = (event) => {
        setCheck({
            ...filterData,
            type: {
                ...filterData.type,
                [event.target.name]: event.target.checked,
            }
        });
    };

    const filterList = Object.entries(filterData.type).map((value) => {
        return(
            <FormControlLabel
                key={`poi-type-list-${value[0]}`}
                className='checkbox-container'
                label={value[0]} 
                control={
                    <Checkbox
                        key={`poi-type-list-checkbox-${value[0]}`}
                        name={value[0]}
                        size='small'
                        checked={value[1]}
                        onChange={handleChange}
                        defaultChecked
                    />
                }
            />
        );
    });

    return (
        <div className='poi-filter-section'>
            <div className='poi-filter-section-column'>
                {...filterList}
            </div>

            {/* <div className='poi-filter-section-column'>
                
            </div> */}
        </div>
    );
};



const PoiFilterCategory = (props) => {
    const {filterData, setCheck, ...other} = props;
    const handleChange = (event) => {
        setCheck({
            ...filterData,
            category: {
                ...filterData.category,
                [event.target.name]: event.target.checked,
            }
        });
    };

    const filterList = Object.entries(filterData.category).map((value) => {
        return(
            <FormControlLabel
                key={`poi-type-list-${value[0]}`}
                className='checkbox-container'
                label={value[0]} 
                control={
                    <Checkbox
                        key={`poi-type-list-checkbox-${value[0]}`}
                        name={value[0]}
                        size='small'
                        checked={value[1]}
                        onChange={handleChange}
                        defaultChecked
                    />
                }
            />
        );
    });

    return (
        <div className='poi-filter-section'>
            <div className='poi-filter-section-column'>
                {...filterList}
            </div>

            {/* <div className='poi-filter-section-column'>
                
            </div> */}
        </div>
    );
};

export function PoiFilter(props) {
    const {visible, ...other} = props;

    const [isPoiFilterDistrictOpen, setIsPoiFilterDistrictOpen] = useState('false');
    const [isPoiFilterTypeOpen, setIsPoiFilterTypeOpen] = useState('false');
    const [isPoiFilterCategoryOpen, setIsPoiFilterCategoryOpen] = useState('false');
        
    const [poiFilterData, setPoiFilterData] = useState(testPoiFilter);

    return (
        <>
            {visible === true && (
                <div id="PoiFilter">
                    <div id="poi-filter-title">
                        <span>
                            Фильтры мест
                        </span>
                    </div>

                    {/* district */}
                    <div
                        className='poi-filter-list-title'
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
                        className='poi-filter-list-title'
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
                        className='poi-filter-list-title'
                        onClick={() => setIsPoiFilterCategoryOpen(!isPoiFilterCategoryOpen)}
                    >
                        {isPoiFilterCategoryOpen && (<KeyboardArrowDownIcon/>)}
                        {!isPoiFilterCategoryOpen && (<KeyboardArrowUpIcon/>)}
                        
                        <span>Категории мест</span>

                        <hr />
                    </div>

                    {isPoiFilterCategoryOpen && (<PoiFilterCategory filterData={poiFilterData} setCheck={setPoiFilterData} />)}
                </div>
            )}
        </>
    )
};