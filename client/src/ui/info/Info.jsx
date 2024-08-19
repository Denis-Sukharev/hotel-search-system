import './Info.css';

import Box from '@mui/material/Box';

function Info() {
    return ( 
        <>
            <Box
                sx={{
                    boxSizing: 'border-box',
                    alignItems: 'end',
                    display: {
                        xs: 'none',
                        sm: 'flex'
                    }
                }}
            >
                <div id="info-qr">
                    <img id="logo-img" src="/logo/logo.png" alt="Logo" />

                    <img id="qr-img" src="/qr/mestechko.png" alt="QR code" />
                </div>
            </Box>
        </>
     );
}

export default Info;