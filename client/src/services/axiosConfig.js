import { useState } from 'react';
import envConfig from '../../env-config.json';
import axios from 'axios';

const config = {
    baseURL: `${envConfig.protocol}://${envConfig.serverHost}:${envConfig.serverPort}`,
    timeout: envConfig.timeout,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
    withCredentials: true,
    method: "get",
}


export const sendAPI = async (urlAPI, setRes, body) => {
    config.url = urlAPI;
    if (body) {
        config.method = 'post';
        config.data = JSON.stringify(body);
        console.log(config.data);
    }
    
    await axios(config)
    .then((response) => {
        setRes(response);
        // console.log(response);
    })
    .catch((error) => {
        console.log(error);
    })
}


export const getHolteAll = async (setHotels, setHotelsCount, body) => {
    config.url = 'fragment' in body ? '/hotel/search_name/' : '/hotel/all/';
    config.method = 'post';
    config.data = JSON.stringify(body);
    
    await axios(config)
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
    config.url = 'fragment' in body ? '/poi/search_name/' : '/poi/all/';
    config.method = 'post';
    config.data = JSON.stringify(body);
    
    await axios(config)
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

export const getHotelOptimal = async (setRoutes, body) => {
    config.url = '/hotel/optimal/';
    config.method = 'post';
    config.data = JSON.stringify(body);
    
    await axios(config)
    .then((response) => {
        setRoutes(response.data);
    })
    .catch((error) => {
        console.log(error);
        setRoutes([]);
    })
}