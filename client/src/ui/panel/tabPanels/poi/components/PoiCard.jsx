import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';

import AddLocationIcon from '@mui/icons-material/AddLocation';
import LocationOffIcon from '@mui/icons-material/LocationOff';

export function PoiCard(props) {
    const {
        poiId,
        poiName,
        poiDescription,
        poiImageUrl,
        poiType,
        poiCoordX,
        poiCoordY,
        changePoi,
        cardButton,
        ...other
    } = props;
    
    return (
        <>
            <div className='PoiCard' id={"poi-card"+poiId}>
                <img src={poiImageUrl} alt={poiName}/>

                <div className="poi-card-content">
                    <div className="poi-card-header">
                        <div className="poi-card-name">
                            <span>{poiName}</span>
                        </div>

                        <IconButton
                            size='large'
                            onClick={changePoi}
                        >   
                            {cardButton()}             
                        </IconButton>
                    </div>

                    <div className="poi-card-description">
                        <div>
                            <p>
                                {poiDescription}
                            </p>
                        </div>
                        
                        <div>
                            <Chip
                                label={poiType}
                                variant='outlined'
                                size='small'
                            />
                        </div>
                        
                        <div>
                            <p>
                            X: {poiCoordX} Y: {poiCoordY} 
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};