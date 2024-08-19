const poiDecrypt = (id, pointList) => {
    let name = id;
    
    for (let i = 0; i < pointList.length; i++) {
        if (id == pointList[i].id) {
            name = pointList[i].name;
            break;
        }
    }

    return(
        name
    )
};

const Point = (props) => {
    const {num, title, hotel, ...other} = props;

    let time = '1 ч.';

    return(
        <>
            <div className="route-point">
                <div className="route-point-num">
                    {num}
                </div>
                
                <div className="route-point-title">
                    {title}

                    {time && !hotel && (
                        <div className="route-point-time">
                            {time}
                        </div>)
                    }
                </div>
            </div>
        </>
    )
};


const Road = () => {
    return(
        <>
            <div class="route-road">
                <div class="route-road-line">

                </div>
            </div>
        </>
    )
};


const Route = (props) => {
    const {route, hotel, pointList, ...other} = props;

    let routeList = route.map((id, index) => {
        return(
            <>
                <Point
                    num={index + 1}
                    title={((index==0) || (index == (route.length-1)))? hotel : poiDecrypt(id, pointList)}
                    hotel={((index==0) || (index == (route.length-1)))? true : false}
                />

                {index < (route.length -1) && (<Road/>)}
            </>
        )
    });

    return(
        <>
            {...routeList}
        </>
    )
};


export function RouteCard(props) {
    const {
        routeData,
        pointList,
        ...other
    } = props;

    return ( 
        <>
            <div id="Routecard">
                <div id="route-params">
                    <span>
                        Общее время: {routeData.time} ч.
                    </span>

                    <span>
                        Дистанция: {routeData.distance} м.
                    </span>

                    <span>
                        Неучтённые места: {
                            routeData.unsatisfied_points.map((item, index) => {
                                return(
                                    (poiDecrypt(item, pointList) + String((index != (routeData.unsatisfied_points.length - 1))? ', ' : ''))
                                )
                            })
                        }
                    </span>
                </div>

                <div id="route">
                    <Route
                        pointList={pointList}
                        hotel={routeData.hotel}
                        route={routeData.route}
                    />
                </div>
            </div>
        </>
     );
}

export default RouteCard;