import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import testPoiHotelFilter from '../../testData/testPoiHotelFilter.json';

const RenderType = (typeData) => {
    let typeList = typeData.typeData.map((typeDataItem) => {
        let typeTitle = typeDataItem;
        
        for (let i = 0; i < testPoiHotelFilter.poiType.length; i++) {
            if (testPoiHotelFilter.poiType[i].type == typeDataItem) {
                typeTitle = testPoiHotelFilter.poiType[i].name;
                break;
            }
        }

        return(
            <Chip
                label={typeTitle}
                variant='outlined'
                size='small'
            />
        )
    })

    return(
        <>
            {...typeList}
        </>
    )
};

export function PoiCard(props) {
    const {
        poiId,
        poiName,
        // poiDescription,
        // poiImageUrl,
        poiType,
        poiCoordX,
        poiCoordY,
        cardButton,
        cardButtonColor,
        changePoi,
        ...other
    } = props;

    let poiImageUrl  = '/logo/logo-img.png';
    
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
                            color={cardButtonColor}
                            onClick={changePoi}
                        >   
                            {cardButton()}             
                        </IconButton>
                    </div>

                    <div className="poi-card-description">
                        {/* <div>
                            <p>
                                {poiDescription}
                            </p>
                        </div> */}
                        
                        <div id="poi-chip">
                            <RenderType
                                typeData={poiType}
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