import testRoutes from '../testData/testRoutes.json';

import './RoutesTabPanel.css';

import { useState } from "react";

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

    const [routeFilter, setRouteFilter] = useState({});
    const [routesData, setroutesData] = useState(testRoutes);

    return ( 
        <>
            <div id="RoutesTabPanel">
                <Section
                    title='Параметры маршрута'
                    sectionData={<RoutesFilter/>}
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