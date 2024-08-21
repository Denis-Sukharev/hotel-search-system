import './Panel.css';

import PoiTabPanel from './tabPanels/poi/PoiTabPanel';
import HotelsTabpanel from './tabPanels/hotels/HotelsTabPanel';
import RoutesTabPanel from './tabPanels/routes/RoutesTabPanel.jsx'

import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Button from '@mui/material/Button';

const BackToTabButton = (props) => {
    const {tabValue, setTabValue} = props;
    
    let button, title;
    
    if (tabValue == 0) {
        button = 'Выбрать места';
        title = 'Места для посещения пока не выбраны(';
    } else {
        button = 'Выбрать Гостиницы';
        title = 'Гостиницы пока не выбраны(';
    }

    return(
        <>
            <div id="back-to-tab-content">
                <div id="back-to-tab-title">
                    {title}
                </div>

                <Button
                    variant="contained"
                    onClick={() => setTabValue(tabValue)}
                >
                    {button}
                </Button>
            </div>
        </>
    )
};

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

function Panel(props) {
    const {selectPointsData, setSelectPointsData, tabValue, setTabValue} = props;

    const tabChange = (event, newTabValue) => {
        setTabValue(newTabValue);
    };


    let routesTabContent = (<RoutesTabPanel
                                selectPointsData={selectPointsData}
                                setSelectPointsData={setSelectPointsData}
                            />)

    if (selectPointsData.poi.length <= 0) {
        routesTabContent = (<BackToTabButton
                                tabValue={0}
                                setTabValue={setTabValue}
                            />)
    } else if (selectPointsData.hotels.length <= 0) {
        routesTabContent = (<BackToTabButton
                                tabValue={1}
                                setTabValue={setTabValue}
                            />)
    }

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
                            
                            {routesTabContent}
                        </TabPanel>
                    </div>
                </div>
            </div>
        </>
     );
}

export default Panel;