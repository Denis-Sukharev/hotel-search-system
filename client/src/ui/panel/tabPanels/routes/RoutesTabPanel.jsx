import testRoutes from '../testData/testRoutes.json';

import './RoutesTabPanel.css';

import { useState, useEffect } from "react";

import { RoutesFilter } from './components/RoutesFilter.jsx';
import { RouteCard } from './components/RouteCard.jsx';

import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';


const routeDecrypt = (id, pointList) => {
    let name = id;
    
    for (let i = 0; i < pointList.length; i++) {
        if (id == pointList[i].id) {
            name = pointList[i].name;
            break;
        }
    }

    return(
        name
    )
};


const Section = (props) => {
    const {title, sectionData, ...other} = props;
    const [isSectionopen, setIsSectionOpen] = useState(false);

    return(
        <>
            <div
                className='section-title'
                onClick={() => setIsSectionOpen(!isSectionopen)}
            >
                {isSectionopen && (<KeyboardArrowDownIcon/>)}
                {!isSectionopen && (<KeyboardArrowUpIcon/>)}
                
                <span>{title}</span>

                <hr />
            </div>

            {isSectionopen && ({...sectionData})}
        </>
    )
}



const Routes = (props) => {
    const {routesData, pointList, ...other} = props;
    
    let routesList = routesData.map((route, index) => {
        return(
            <>
                <Section
                    title={'Маршрут ' + Number(Number(index)+1)}
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

    const [routesData, setroutesData] = useState(testRoutes);
    const [routeFilterData, setRouteFilterData] = useState({
        time_limit: 7,
        days: 1
    });


    useEffect(() => {
        let body = {
            data: {
                time_limit: routeFilterData.time_limit,
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
        
        console.log(body)
    }, [routeFilterData])


    return ( 
        <>
            <div id="RoutesTabPanel">
                <Section
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
                />
            </div>
        </>
     );
}

export default RoutesTabPanel;