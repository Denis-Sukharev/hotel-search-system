import testRoutes from '../testData/testRoutes.json';
import { getRouteSequence, getRoute } from '../../../../services/axiosConfig.js';

import './RoutesTabPanel.css';

import { useState, useEffect } from "react";

import { RoutesFilter } from './components/RoutesFilter.jsx';
import { RouteCard } from './components/RouteCard.jsx';

import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';


const SectionFilter = (props) => {
    const {title, sectionData, ...other} = props;
    const [isSectionopen, setIsSectionOpen] = useState(false);

    return(
        <>
            <div
                className='section-title'
                onClick={() => {
                    setIsSectionOpen(!isSectionopen);
                }}
            >
                {isSectionopen && (<KeyboardArrowDownIcon/>)}
                {!isSectionopen &&  (<KeyboardArrowUpIcon/>)}
                
                <span>{title}</span>

                <hr />
            </div>

            {isSectionopen && ({...sectionData})}
        </>
    )
}


const Section = (props) => {
    const {title, sectionData, setSelectPointsData, selectPointsData, index, route, ...other} = props;

    return(
        <>
            <div
                className='section-title'
                onClick={() => {
                    if (selectPointsData.selectRouteIndex != index) {
                        setSelectPointsData({
                            ...selectPointsData,
                            route: route.route,
                            selectRouteIndex: index
                        })
                    }
                }}
            >
                {selectPointsData.selectRouteIndex == index && (<KeyboardArrowDownIcon/>)}
                {selectPointsData.selectRouteIndex != index &&  (<KeyboardArrowUpIcon/>)}
                
                <span>{title}</span>

                <hr />
            </div>

            {selectPointsData.selectRouteIndex == index && ({...sectionData})}
        </>
    )
}



const Routes = (props) => {
    const {routesData, pointList, setSelectPointsData, selectPointsData, ...other} = props;
    
    let routesList = routesData.map((route, index) => {
        return(
            <>
                <Section
                    title={route.hotel}
                    setSelectPointsData={setSelectPointsData}
                    selectPointsData={selectPointsData}
                    route={route}
                    index={index}
                    sectionData={
                        <RouteCard
                            pointList={pointList}
                            routeData={route}
                        />
                    }
                />
            </>
        )
    })

    return(
        <>
            {...routesList}
        </>
    )
}



function RoutesTabPanel(props) {
    const {selectPointsData, setSelectPointsData} = props;

    const [routesData, setroutesData] = useState([]);
    const [route, setRoute] = useState([]);
    const [routeTabIndex, setRouteTabIndex] = useState(-1);
    const [routeFilterData, setRouteFilterData] = useState({
        time_limit: 7,
        days: 1
    });


    useEffect(() => {
        let body = {
            data: {
                time_limit: (routeFilterData.time_limit - selectPointsData.poi.length) >= 0 ? (routeFilterData.time_limit - selectPointsData.poi.length) : 0,
                days: routeFilterData.days,
                points_sequence: selectPointsData.poi.map((item) => item.id)
            },
            hotel: {
                hotels: selectPointsData.hotels.map((item) => ({
                    hotel_id: item.id,
                    name: item.name,
                    latitude: item.latitude,
                    longitude: item.longitude,
                    district_id: 0
              }))
            }
        };

        getRouteSequence(setroutesData, body);
    }, [routeFilterData])

    return ( 
        <>
            <div id="RoutesTabPanel">
                <SectionFilter
                    title='Параметры маршрута'
                    sectionData={
                        <RoutesFilter
                            routeFilterData={routeFilterData}
                            setRouteFilterData={setRouteFilterData}
                        />
                    }
                />

                <Routes
                    pointList={selectPointsData.poi}
                    routesData={routesData}
                    setSelectPointsData={setSelectPointsData}
                    selectPointsData={selectPointsData}
                />
            </div>
        </>
     );
}

export default RoutesTabPanel;