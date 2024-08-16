import './Panel.css';

import PoiTabPanel from './tabPanels/poi/PoiTabPanel';
import HotelsTabpanel from './tabPanels/hotels/HotelsTabPanel';
import RoutesTabPanel from './tabPanels/routes/RoutesTabPanel.jsx'

import { useState } from 'react';

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';

const TabPanel = (props) => {
    const {children, value, index, ...other} = props;

    return(
        <>
            {value === index && (
                <div id = "tab-panel">
                    {children}
                </div>
            )}
        </>
    );
};

function Panel() {
    const [selectPointsData, setSelectPointsData] = useState({
        poi: [

        ],

        hotels: [
            
        ]
    });


    const [tabValue, setTabValue] = useState(0);

    const tabChange = (event, newTabValue) => {
        setTabValue(newTabValue);
    };

    return ( 
        <>
            <div id="Panel">
                <div id="panel-content">
                    <div id="panel-city-block">
                        Город: <u>Москва</u>
                    </div>

                    <div id="Tabs">
                        <Tabs
                            value={tabValue}
                            onChange={tabChange}
                            variant='fullWidth'
                        >
                            <Tab
                                id="tab-0"
                                value={0}
                                label="Места"
                            />

                            <Tab
                                id="tab-1"
                                value={1}
                                label="Гостиницы"
                            />

                            <Tab
                                id="tab-2"
                                value={2}
                                label="Маршруты"
                            />
                        </Tabs>
                    </div>

                    <div id="tab-panel-container">
                        <TabPanel
                            value={tabValue}
                            index={0}
                        >
                            <PoiTabPanel
                                selectPointsData={selectPointsData}
                                setSelectPointsData={setSelectPointsData}
                            />
                        </TabPanel>

                        <TabPanel
                            value={tabValue}
                            index={1}
                        >
                            <HotelsTabpanel
                                selectPointsData={selectPointsData}
                                setSelectPointsData={setSelectPointsData}
                            />
                        </TabPanel>

                        <TabPanel
                            value={tabValue}
                            index={2}
                        >
                            <RoutesTabPanel />
                        </TabPanel>
                    </div>
                </div>
            </div>
        </>
     );
}

export default Panel;