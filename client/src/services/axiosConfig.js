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