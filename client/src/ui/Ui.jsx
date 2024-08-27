import './Ui.css';

import Panel from './panel/Panel.jsx'
import Info from './info/Info.jsx';
import Box from '@mui/material/Box';

function Ui() {
    return ( 
        <Box
            // id='Ui'
            sx={{
                justifyContent: {
                    xs: 'center',
                    sm: 'space-between'
                },
                backgroundColor: 'yellow',
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
            {/* <div id="Ui"> */}
                <Panel />
                <Info/>
            {/* </div> */}
        </Box>
     );
}

export default Ui;