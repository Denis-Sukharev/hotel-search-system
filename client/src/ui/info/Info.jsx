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
                    },
                }}
            >
                <div id="info-qr">
                    <span>
                        Сервис планирования путешествий
                    </span>

                    <div id="info-img">
                        <img id="logo-img" src="/logo/logo.png" alt="Logo" />

                        <img id="qr-img" src="/qr/mestechko.png" alt="QR code" />
                    </div>
                   
                </div> 
                
            </Box>
        </>
     );
}

export default Info;