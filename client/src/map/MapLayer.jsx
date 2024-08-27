import './MapLayer.css';
import 'leaflet/dist/leaflet.css';
import '../ui/Ui.css';

import { getRoute } from '../services/axiosConfig';
import envConfig from '../../env-config.json';

import Info from '../ui/info/Info';
import Panel from '../ui/panel/Panel';

import { MapContainer, TileLayer, ZoomControl, Marker, Polyline } from 'react-leaflet'
import L from 'leaflet';
import { useEffect, useState } from 'react';
import Box from '@mui/material/Box';



const SelectPointMarker = (props) => {
    const {markerCoordList} = props;

    let markerList = [];

    
    markerList = markerCoordList.map((item, index)  => {
        let icon
        
        if(index == 0) {
            icon = L.divIcon({
                className: "empty",
                html:
                `
                    \u003cdiv style=\u0027
                        background-color: white;
                        border-radius: 50%;
                        width: 25px;
                        height: 25px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-size: 16px;
                        border: 3px solid #757ce8;
                        \u0027\u003e
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                height="20px"
                                viewBox="0 0 24 24"
                                width="20px"
                                fill="#717171"
                            >
                                    <path
                                        d="M0 0h24v24H0z"
                                        fill="none"
                                    />
                                    <path
                                        d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"
                                    />
                            </svg>
                    \u003c/div\u003e`,
                    iconSize: [30,30]
            });
        } else {
            icon = L.divIcon({
                className: "empty",
                html:
                `
                    \u003cdiv style=\u0027
                        background-color: white;
                        border-radius: 50%;
                        width: 25px;
                        height: 25px;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        font-size: 16px;
                        border: 3px solid #757ce8;
                        \u0027\u003e
                        ${index}
                    \u003c/div\u003e`,
                    iconSize: [30,30]
            });
        }

        return(
            <Marker
                position={[item[1], item[0]]}
                icon={icon}
            />
        )
    })
    
    return(
        <>
            {...markerList}
        </>
    )
};

const SelectPointLine = (props) => {
    const {selectPointsData} = props;

    let lineCoord = selectPointsData.routeLine[selectPointsData.selectRouteIndex].map((item) => {
        return [item[1], item[0]]
    })
    lineCoord.push(lineCoord[0])

    return(
        <>
            <Polyline
                pathOptions={{
                    color: '#757ce8',
                    weight: 4,
                }}
                positions={lineCoord}
            />
        </>
    )
};

function MapLayer(props) {
    const {selectPointsData, setSelectPointsData, tabValue, setTabValue} = props;
    const [markerCoordList, setMarkerCoordList] = useState([])
    
    const mapConfig = {
        center: [55.75, 37.61],
        zoom: 13,
        zoomControl: false,
        preferCanvas: false,
    }

    useEffect(() => {
        let ml = [];

        if (tabValue == 0) {
            ml = selectPointsData.poi.map((poi) => {
                return([Number(poi.latitude), Number(poi.longitude)])
            });
        }
        
        if (tabValue == 1) {
            ml = selectPointsData.hotels.map((poi) => {
                return([Number(poi.latitude), Number(poi.longitude)])
            });
        }

        if (tabValue == 2 && selectPointsData.selectRouteIndex != -1) {
            ml = selectPointsData.routeCoord[selectPointsData.selectRouteIndex];
        }

        setMarkerCoordList(ml);
    }, [tabValue, selectPointsData])

    return ( 
        <>
            <div id='MapLayer'>
                {/* <div  id="Ui"> */}
                <Box
                    // id='Ui'
                    sx={{
                        justifyContent: {
                            xs: 'center',
                            sm: 'space-between'
                        },  
                        width: '100%',
                        height: '100%',
                        boxSizing: 'border-box',

                        padding: '15px',

                        display: 'inline-flex',

                        pointerEvents: 'none',
                        position: 'absolute !important',
                        zIndex: '1000 !important'
                    }}
                >
                    <Panel
                        selectPointsData={selectPointsData}
                        setSelectPointsData={setSelectPointsData}
                        tabValue={tabValue}
                        setTabValue={setTabValue}
                    />

                    <Info/>
                </Box>
                {/* </div> */}
                    
                <MapContainer
                    center={mapConfig.center}
                    zoom={mapConfig.zoom}
                    zoomControl={mapConfig.zoomControl}
                    preferCanvas={mapConfig.preferCanvas}
                >
                    <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />

                    <ZoomControl
                        position='topright'
                        
                    />


                    <SelectPointMarker
                        markerCoordList={markerCoordList}
                    />


                    {tabValue == 2 && selectPointsData.routeLine.length > 0 && (
                        <SelectPointLine
                            selectPointsData ={selectPointsData}
                        />
                    )}
                </MapContainer>
            </div>
        </>
     );
}

export default MapLayer;