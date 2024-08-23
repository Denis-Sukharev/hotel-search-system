import Chip from '@mui/material/Chip';
import IconButton from '@mui/material/IconButton';
import StarIcon from '@mui/icons-material/Star';
import testPoiHotelFilter from '../../testData/testPoiHotelFilter.json';

const RenderType = (typeData) => {
    let typeList = typeData.typeData?.map((typeDataItem) => {
        return(
            <Chip
                label={typeDataItem}
                variant='outlined'
                size='small'
            />
        )
    })

    if (typeList) {
        return(
            <>
                {...typeList}
            </>
        )
    }
};

export const HotelCard = (props) => {
    const {
        hotelId,
        hotelName,
        // hotelDescription,
        // hotelImageUrl,
        hotelType,
        hotelRating,
        hotelCoordX,
        hotelCoordY,
        cardButton,
        cardButtonColor,
        changeHotel,
        ...other
    } = props;

    let hotelImageUrl  = '/logo/logo-img.png';
    
    return (
        <>
            <div className='HotelCard' id={"hotel-card"+hotelId}>
                <img src={hotelImageUrl} alt={hotelName}/>

                <div className="hotel-card-content">
                    <div className="hotel-card-header">
                        <div className="hotel-card-name">
                            <span>{hotelName}</span>
                        </div>

                        <IconButton
                            size='large'
                            color={cardButtonColor}
                            onClick={changeHotel}
                        >   
                            {cardButton()}             
                        </IconButton>
                    </div>

                    <div className="hotel-card-description">
                        {/* <div>
                            <p>
                                {poiDescription}
                            </p>
                        </div> */}
                        
                        <div id="hotel-chip">
                            <div id="hotel-rating">
                                <StarIcon
                                    sx={{
                                        color: '#ffc107'
                                    }}
                                />
                                <span>
                                    {hotelRating}
                                </span>
                            </div>

                            <RenderType
                                typeData={hotelType}
                            />
                        </div>
                        
                        <div>
                            <p>
                            X: {hotelCoordX} Y: {hotelCoordY} 
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};