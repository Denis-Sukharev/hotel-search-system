import { useState } from 'react';
import envConfig from '../../env-config.json';
import axios from 'axios';

const config = {
    baseURL: `${envConfig.protocol}://${envConfig.serverHost}:${envConfig.serverPort}${envConfig.serverLocation}`,
    timeout: envConfig.timeout,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    withCredentials: true,
    method: "get",
}


export const sendAPI = async (urlAPI, setRes, body) => {
    let _config = {
        ...config,
        url: urlAPI
    }

    if (body) {
        _config.method = 'post';
        _config.data = JSON.stringify(body);
        _config.log(config.data);
    }
    
    await axios(_config)
    .then((response) => {
        setRes(response);
        // console.log(response);
    })
    .catch((error) => {
        console.log(error);
    })
}


export const getHolteAll = async (setHotels, setHotelsCount, body) => {
    let _config = {
        ...config,
        url: 'fragment' in body ?
        '/hotel/search_name/' :
        ('page' in body ? '/hotel/all/' : '/hotel/optimal/'),
        method: 'post',
        data: JSON.stringify(body)
    }
    
    await axios(_config)
    .then((response) => {
        setHotels(response.data.hotels);

        'count' in response.data ? 
            setHotelsCount(response.data.count) :
            setHotelsCount(0)
    })
    .catch((error) => {
        console.log(error);
        setHotels([]);
        setHotelsCount(0);
    })
}

export const getPoiAll = async (setPoi, setPoiCount, body) => {
    let _config = {
        ...config,
        url: 'fragment' in body ? '/poi/search_name/' : '/poi/all/',
        method: 'post',
        data: JSON.stringify(body)
    }
    
    await axios(_config)
    .then((response) => {
        setPoi(response.data.poi);

        'count' in response.data ? 
            setPoiCount(response.data.count) :
            setPoiCount(0)
    })
    .catch((error) => {
        console.log(error);
        setPoi([]);
        setPoiCount(0);
    })
}

export const getRouteSequence = async (setRouteSequence, body) => {
    let _config = {
        ...config,
        url: '/route/optimal/',
        method: 'post',
        data: JSON.stringify(body)
    }
    
    await axios(_config)
    .then((response) => {
        setRouteSequence(response.data);
    })
    .catch((error) => {
        console.log(error);
        setRouteSequence([]);
    })
}

export const getRoute = async (body) => {
    let _config = {
        ...config,
        baseURL: 'https://api.openrouteservice.org/v2/directions/driving-car',
        headers: {Authorization: envConfig.apiOsm},
        method: 'post',
        data: JSON.stringify(body)
    }

    await axios(_config)
    .then((response) => {
        console.log(response.data)
    })  
    .catch((error) => {
        console.log(error)
    })
};