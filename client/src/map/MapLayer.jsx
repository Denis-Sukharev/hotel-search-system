import './MapLayer.css';
import 'leaflet/dist/leaflet.css';
import '../ui/Ui.css';

import { getRoute } from '../services/axiosConfig';
import envConfig from '../../env-config.json';

import Info from '../ui/info/Info';
import Panel from '../ui/panel/Panel';

import HomeIcon from '@mui/icons-material/Home';

import { MapContainer, TileLayer, ZoomControl, Marker, Polyline, SVGOverlay  } from 'react-leaflet'
import L from 'leaflet';
import { useEffect, useState } from 'react';

const SelectPointMarker = (props) => {
    const {markerCoordList, tabValue} = props;

    let markerList = [];

    markerList = markerCoordList.map((item, index)  => {
        if (tabValue == 2) {
            let icon = L.divIcon({
                className: "empty",
                html: `
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
                        ${index+1}
                    \u003c/div\u003e`,
                    iconSize: [30,30]
            });
            return(
                <Marker
                    position={item}
                    icon={icon}
                />
            )
        } else {
            return(
                <Marker
                    position={item}
                />
            )
        }
    })
    
    return(
        <>
            {...markerList}
        </>
    )
};

const SelectPointLine = (props) => {
    const {markerCoordList} = props;

    let lineList = markerCoordList;
    lineList.push(markerCoordList[0]);

    // try {
    //     getRoute(markerCoordList);
    // } catch {

    // }
    // for (let i = 0; i< markerCoordList.length - 1; i++) {
        let coord = [];
        // getRoute(`https://api.openrouteservice.org/v2/directions/driving-car?api_key=${envConfig.apiOsm}&start=${markerCoordList[i][1]},${markerCoordList[i][0]}&end=${markerCoordList[i+1][1]},${markerCoordList[i+1][0]}`)
        // .then((res) => {coord = res})
        
        // console.log(coord);
        // if (!coord.error) {
        //     lineList.push(
        //         <Polyline pathOptions={{color: "red"}} positions={coord.data} />
        //     )
        // }
    // }
    
    return(
        <>
            {/* {...lineList} */}
            <Polyline pathOptions={{color: '#757ce8', weight: 4,}} positions={lineList} />
        </>
    )
};

function MapLayer(props) {
    const {selectPointsData, setSelectPointsData, tabValue, setTabValue} = props;
    const [markerCoordList, setMarkerCoordList] = useState([]);
    
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
            for (let i = 0; i < selectPointsData.hotels.length; i++) {
                if (selectPointsData.hotels[i].id == selectPointsData.route[0]) {
                    ml.push([
                        Number(selectPointsData.hotels[i].latitude),
                        Number(selectPointsData.hotels[i].longitude)
                    ]);
                    break;
                }
            }

            for (let i = 1; i < selectPointsData.route.length - 1; i++) {
                for (let j = 0; j < selectPointsData.poi.length; j++) {
                    if (selectPointsData.poi[j].id == selectPointsData.route[i]) {
                        ml.push([
                            Number(selectPointsData.poi[j].latitude),
                            Number(selectPointsData.poi[j].longitude)
                        ]);
                        break;
                    }
                }
            }
        }

        setMarkerCoordList(ml);
    }, [tabValue, selectPointsData])

    return ( 
        <>
            <div id='MapLayer'>
                <div  id="Ui">
                    <Panel
                        selectPointsData={selectPointsData}
                        setSelectPointsData={setSelectPointsData}
                        tabValue={tabValue}
                        setTabValue={setTabValue}
                    />

                    <Info/>
                </div>
                    
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

                    {markerCoordList.length > 0 && (tabValue != 2 || (tabValue == 2 && selectPointsData.route.length > 0)) && (<SelectPointMarker
                        markerCoordList={markerCoordList}
                        tabValue={tabValue}
                    />)}

                    {tabValue == 2 && markerCoordList.length > 0 && selectPointsData.route.length > 0 && (
                        <SelectPointLine
                            markerCoordList ={markerCoordList}
                        />
                    )}
                </MapContainer>
            </div>
        </>
     );
}

export default MapLayer;