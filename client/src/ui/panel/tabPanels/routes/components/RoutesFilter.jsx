import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { useState } from 'react';


export function RoutesFilter(props) {
    const { routeFilterData, setRouteFilterData, ...other } = props;

    const [routeFilter, setRouteFilter] = useState({
        time_limit: Number(routeFilterData.time_limit),
        days: Number(routeFilterData.days)
    });

    return ( 
        <>
            <div id="RoutesFilter">
                <FormControlLabel
                    key={`route-filter-days-label`}
                    label={
                        <Typography fontSize={14} >
                            Ограничение по дням (в днях)
                        </Typography>
                    }
                    sx={{
                        fontSize: 14,
                        margin: 0,
                        boxSizing: 'border-box',
                    }}
                    control={
                        <TextField
                            id="route-filter-days"
                            size="small"
                            value={Number(routeFilter.days)}
                            type='number'
                            disabled={true}
                            sx={{
                                width: 70,
                                marginRight: '5px',
                                fontSize: 14,
                            }}
                            onChange={(event, value) => 
                                setRouteFilter({
                                    ...routeFilter,
                                    days: Number(value)
                                })
                            }
                        />
                    }
                />



                <FormControlLabel
                    key={`route-filter-time_limit-label`}
                    label={
                        <Typography fontSize={14} >
                            Ограничение по времени (в часах)
                        </Typography>
                    }
                    sx={{
                        fontSize: 14,
                        margin: 0,
                        boxSizing: 'border-box',
                    }}
                    control={
                        <TextField
                            id="route-filter-time_limit"
                            size="small"
                            value={Number(routeFilter.time_limit)}
                            type='number'
                            disabled={true}
                            sx={{
                                width: 70,
                                marginRight: '5px',
                                fontSize: 14,
                            }}
                            onChange={(event, value) => 
                                setRouteFilter({
                                    ...routeFilter,
                                    time_limit: Number(value)
                                })
                            }
                        />
                    }
                />


                <Button
                    onClick={() => {
                        setRouteFilterData({
                        ...routeFilterData,
                        time_limit: Number(routeFilter.time_limit),
                        days: Number(routeFilter.days)
                        })
                    }}
                    variant='contained'
                    size='small'
                    fullWidth
                    disabled={true}
                    sx={{
                        marginTop: 1,
                    }}
                >
                    Применить фильтры
                </Button>
            </div>
        </>
     );
}

export default RoutesFilter;