import testRoutes from '../testData/testRoutes.json';
import { getRouteSequence, getRoute } from '../../../../services/axiosConfig.js';


import './RoutesTabPanel.css';

import { useState, useEffect } from "react";
import axios from 'axios';
import envConfig from '../../../../../env-config.json'

import { RoutesFilter } from './components/RoutesFilter.jsx';
import { RouteCard } from './components/RouteCard.jsx';

import Skeleton from '@mui/material/Skeleton';

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
    const {title, sectionData, setSelectPointsData, selectPointsData, index, ...other} = props;

    return(
        <>
            <div
                className='section-title'
                onClick={() => {
                    if (selectPointsData.selectRouteIndex != index) {
                        setSelectPointsData({
                            ...selectPointsData,
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














async function run(body) {
    const query = new URLSearchParams({
        key: envConfig.apiGh
    }).toString();
    
    const resp = await fetch(
        `https://graphhopper.com/api/1/route?${query}`,
        {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            profile: 'bike',
            points: body,
            points_encoded: false,  
            // point_hints: [
            // 'Lindenschmitstraße',
            // 'Thalkirchener Str.'
            // ],
            snap_preventions: [
            'motorway',
            'ferry',
            'tunnel'
            ],
            details: ['road_class', 'surface']
        })
        }
    );
    
    const data = await resp.json();
    return(data.paths[0].points.coordinates);
  }
  








function RoutesTabPanel(props) {
    const {selectPointsData, setSelectPointsData} = props;

    const [routesData, setroutesData] = useState([]);
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


    


    useEffect(() => {
        let routeParse = {
            id: [],
            coord: []
        }
        let routeLineParse = []

        
        routesData.map(async (routeItem) => {
            let tmpRouteId = [];
            let tmpRouteCoord = [];

            for (let i = 0; i < selectPointsData.hotels.length; i++) {
                if (selectPointsData.hotels[i].id == routeItem.route[0]) {
                    tmpRouteId.push(routeItem.route[0]);
                    tmpRouteCoord.push([
                        Number(selectPointsData.hotels[i].longitude),
                        Number(selectPointsData.hotels[i].latitude),
                    ]);
                    break;
                }
            }

            for (let i = 1; i < routeItem.route.length - 1; i++) {
                for (let j = 0; j < selectPointsData.poi.length; j++) {
                    if (selectPointsData.poi[j].id == routeItem.route[i]) {
                        tmpRouteId.push(routeItem.route[i]);

                        tmpRouteCoord.push([
                            Number(selectPointsData.poi[j].longitude),
                            Number(selectPointsData.poi[j].latitude),
                        ]);
                        break;
                    }
                }
            }

            
            // let _config = {
            //     method: 'post',
            //     timeout: 600000,
            //     withCredentials: true,

            //     // url: 'https://api.openrouteservice.org/v2/directions/driving-car',
            //     // data: {
            //     //     'coordinates': tmpRouteCoord,
            //     //     "radiuses": [8000],
            //     // },
            //     // headers: {
            //     //     // 'Accept': 'application/json, text/plain, */*',
            //     //     'Content-Type': 'application/json',
            //     //     'Authorization': envConfig.apiOsm,
            //     // },

            //     url: `https://graphhopper.com/api/1/route?key=${envConfig.apiGh}`,
            //     data: {
            //         elevation: false,
            //         points: [[-0.087891,51.534377],[-0.090637,51.467697]],//tmpRouteCoord,
            //         profile: "car",
            //     },
            //     headers: {
            //         // 'Accept': 'application/json, text/plain, */*',
            //         "Content-Type": 'application/json'
            //     },
            // }   

            // axios(_config)
            // .then((response) => {
            //     // routeLineParse.push(response.features.geometry.coordinates);
            //     // routeLineParse.push(response);
            //     console.log(response)
            // })  
            // .catch((error) => {
            //     console.log(error)
            // })

            routeLineParse.push(await run(tmpRouteCoord))

            
            routeParse.id.push(tmpRouteId);
            routeParse.coord.push(tmpRouteCoord);
        })

        setSelectPointsData({
            ...selectPointsData,
            route: routeParse.id,
            routeCoord: routeParse.coord,
            routeLine: routeLineParse,
        })
    }, [routesData])

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

                {routesData.length > 0 ? (
                    <Routes
                        pointList={selectPointsData.poi}
                        routesData={routesData}
                        setSelectPointsData={setSelectPointsData}
                        selectPointsData={selectPointsData}
                    />
                ) : <><Skeleton variant="rectangular" fullWidth height={150} /><Skeleton variant="rectangular" fullWidth height={150} /></>}
                
            </div>
        </>
     );
}

export default RoutesTabPanel;