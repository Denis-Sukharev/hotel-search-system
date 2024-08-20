import './MapLayer.css';
import 'leaflet/dist/leaflet.css';
import '../ui/Ui.css';
import Info from '../ui/info/Info';
import Panel from '../ui/panel/Panel';
import { MapContainer, TileLayer, ZoomControl, Marker } from 'react-leaflet'

const SelectPointMarker = (props) => {
    const {selectPointsData, tabValue} = props;

    let markerList = [];

    if (tabValue == 0) {
        markerList = selectPointsData.poi.map((poi) => {
            return(
                <Marker
                    position={[poi.latitude, poi.longitude]}
                >
                    
                </Marker>
            )
        });
    }
    
    if (tabValue == 1) {
        markerList = selectPointsData.hotels.map((poi) => {
            return(
                <Marker
                    position={[poi.latitude, poi.longitude]}
                >
                    
                </Marker>
            )
        });
    }
    
    return(
        <>
            {...markerList}
        </>
    )
};

function MapLayer(props) {
    const {selectPointsData, setSelectPointsData, tabValue, setTabValue} = props;
    
    const mapConfig = {
        center: [55.75, 37.61],
        zoom: 13,
        zoomControl: false,
        preferCanvas: false,
    }

    return ( 
        <>
            <div id='MapLayer'>
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
                
                <div className='leaflet-control' id="Ui">
                    <Panel
                        selectPointsData={selectPointsData}
                        setSelectPointsData={setSelectPointsData}
                        tabValue={tabValue}
                        setTabValue={setTabValue}
                    />

                    <Info/>
                </div>

                <SelectPointMarker
                    selectPointsData={selectPointsData}
                    tabValue={tabValue}
                />

                </MapContainer>
            </div>
        </>
     );
}

export default MapLayer;