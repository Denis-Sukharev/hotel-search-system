import os
import requests
import subprocess
import yaml
from concurrent.futures import ThreadPoolExecutor
import random
import string

def get_proxy_ip(proxy):
    try:
        response = requests.get('http://httpbin.org/ip', proxies=proxy)
        if response.status_code == 200:
            data = response.json()
            return data['origin']
        else:
            print("Failed to retrieve IP. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", str(e))
        return None

def update_params_file(params_file, api_key):
    with open(params_file, 'r') as file:
        params = yaml.safe_load(file)
    
    params['api_key'] = api_key

    with open(params_file, 'w') as file:
        yaml.dump(params, file)

def create_params_file(proxy_data):
    proxy = {"http": proxy_data['http']}
    proxy_ip = get_proxy_ip(proxy)
    
    if proxy_ip:
        print(f"proxy ip", proxy_ip)

        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        params_file = f"params/params_proxy_{proxy_ip.replace('.', '_')}_{suffix}.yaml"

        params = {
            'output_format': 'geojson',
            'profile': 'driving-car', #foot-walking, cycling-regular
            'units': 'm',
            'api_key': proxy_data["api_key"]
        }

        with open(params_file, 'w') as file:
            yaml.dump(params, file)

        return params_file

def execute_script_through_proxy(script_path, input_file, output_file, params_file, type_arg, proxy, start_index):
    try:
        command = f'python "{script_path}" -i "{input_file}" -o "{output_file}" -p "{params_file}" -t "{type_arg}" -s {start_index}'
        os.environ['HTTP_PROXY'] = proxy["http"]
        subprocess.run(command, shell=True)
        print(f"Выполнение скрипта через прокси {params_file} успешно")
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        del os.environ['HTTP_PROXY']

if __name__ == "__main__":
    proxy_list = [
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf62488d0e2117bf47450eae44a5305aed924b"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf6248701d7d42934f4645a332d8874d065a61"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf62482c0997000b5d40f7ab497596cb1ec777"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248ad28d11a7ae1445db5ec3be45d6ab0f4"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf624827a2df637b8943859a9441cc7f22d691"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248cb110debfca2436892779165dd78a9e5"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf62484729708b3a024d11b99306f4a0e40759"}, 

        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf6248552fa6f857a44bfe816ad621c49d5d83"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf6248a02a15f1e7134ebe86d7a9778e453fbd"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf6248bc1c3e4073244768b5699a606158515e"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf62488ddb94e886e741318a628a09f6527850"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf6248d886bf3f8b5d41fbb028916d6eaceb1a"},

        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf6248effa4ea589944a8a82a97861c39172c7"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf62480bfd413497e74733af92a261544c73ba"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf6248c8b070b7d863436b91ee86241632ad88"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf62488e0890b5a8a5426d9c5ed4da4d64e583"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf62489b2f562632314334b7fbb45198c5d388"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf624870934324319c4948968a8895a907c2c8"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf6248a129116c40e14011ae90fdb77d6e2671"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf62483a702d46e73d43c485c8812ffbe39367"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf6248c8ba1cb38a024d518afb7c8d288e3d8a"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf6248150ec27f186943e2a554aa7e5173b3aa"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf62482808e37949ad4065a321c93df21bc48d"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf624850ca460ae2774805a03f5f0f53c656f1"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf62489e96b612e11f463ab3227313b936f956"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf624835e7a719caf04ecdad3a695296da0d76"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf62489569c7bd6991461ab65ae2b9882bf89f"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf6248f3983fcde9534781bf4f2ad91c9108b4"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf6248d8a360fb074e4a239eb252d732f44a6c"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf6248964907a804d5426cbabf956836e6ae15"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf6248215fb6fe0b924fd5b6c5788abd8c76d2"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf62486af87ee576c24b55ae0c80877fa686cd"},
        
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf6248550f383fe4de4ec2a279c918260acedc"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf6248ca7dae7a291a411183781414dfced9bf"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf6248dbd0d7224b0e444281485db01d6abc16"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf6248a30960a8ef4b4dcb82b43b308b123a45"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf624841cacc1024f54c7d9391602a87793eeb"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248cc60c720a2de4bb4b7ccdd7c4ec1f798"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248dd6044753b03465387be0ced7d4d69bc"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf62484341ceae7be5438393b4ec93acf92a99"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf624829770b0244da4adca2503763f38bbf6a"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248173f7df2a7fb46f7bfd39d1e49788f7a"},


# --------------------------------------------------------------

        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf6248741efa83878d4535aa40c7da7bbf07ba"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf6248c0e57b3c61ab4de9ae0d9047d04cb157"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf6248792c976316804b6f8494ef4ee767f54c"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf62485104cd8471af4584af87aa5ef098032a"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf62483c4c05d014c841199ca44c9d7694a30f"},

        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf6248540030b9cca946ca8055d97271e84873"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf6248fd865737f2f345f6af5f9bb9a50aafbc"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf6248fc3d4ed7c50247c8bfd08ebd58575a48"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf624880fdc4ef60a5486c92afbfd26801311b"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf6248e729dcce6d8142ec9412330bd68f6245"},

        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf624824d538a19ce64eb88e94efce76e9d45a"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248c0fe5b942cd044079813bb74d8743409"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248e9014d5c4cba4babba6733f485a6eedf"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248227dc4c9c02d45a5ae19b22a2e79397b"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248e7914511c30a4575b1527de53e867b7e"}, 

        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf6248d2d901e28b5941ec83c6ea284501463e"},
        {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf624868353ad4f1704be88e8412ff6f416e45"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf62480e68960d630f4ca4b0ae49addf9947ff"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf624829c92f670f6242d6b27501e35252f697"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf6248baff694be1ee482fb25ab8b35427a342"},

        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf6248c5501833e367493b985b1a4499852553"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf6248a6023292484d44ebb6c49132033f9fe4"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf62485906982420b247e3b7c0b27e2a8f569a"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf6248e2241aa205214dce8674752181d9b1bc"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf6248d48bb73d564848439524465e80f3cc8a"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf6248c94992dcf4a2452b87e9587ad2ae4760"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf62481e760f10d9fe4c3098e03a71acfa0415"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf6248026ed3f602a94b45b39b8562fc357953"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf62488d5f723088f542fa9faab80738ce499c"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf6248f069afbe56984bde9e632b0bbfd23957"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf62487b029d9e0bab42b1ab5f76e8136e6f17"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf6248fb8b7f659c864e14889ecc4709266f1a"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf6248ae14ba9b01684c1582936bfeb5b04d51"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf6248c0972830dfbf4aabaa6460ee25bcdbdd"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf62480e4970b8a2824659a4da59997b71951f"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf6248a855327dddb7494fb6abeacf03bd390f"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf62482ccdec22b7e04b9fa3ee201be9694a47"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf62486a4e5ef559ed49efacc1832a5fdf881d"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf6248b6dd0b9a3bd341e5a81883bbdc3f1e0b"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf62486589ca047a8e4230b59a514265ff3363"},
        
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf62484b84e07ca4aa413ba407f3dd1dc010bc"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf6248e303e28424e34cf9ac8f926ea01c2601"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf624891a83d924d904b4994bf1191bb828f14"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf6248c68a312fee81406fbae27cc2082b4767"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf6248b2c61426c27c438ab2ca8b6187a77939"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf624839d70636b8954161b9c0a95c72da705a"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248c572a7f59fe242e5b981b323eca52e43"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf62481f43d67c689a42c6bc931e8dc6270ee1"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248415e5406336d4787824117fe023a2908"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248b4c0d7de605946718631f6cf5db85d85"},

        # {"http": "http://PAUBax:EK3sMk@31.44.191.78:9116", "api_key": "5b3ce3597851110001cf62481e9eacb96a974079bd175652efd9a0cb"},
        # {"http": "http://PAUBax:EK3sMk@31.44.191.78:9116", "api_key": "5b3ce3597851110001cf62487af38c04a44a460cb59e5a0274fb516c"},
        # {"http": "http://PAUBax:EK3sMk@31.44.191.78:9116", "api_key": "5b3ce3597851110001cf6248f59421460dd841e185ef1000d0f7e819"},
       

# ---------------------------------------------------------------------------

        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf624809ecbb364fa948238384e28fc646c1f6"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf62486cc28d27be6b4e2c9f1ac299a9f80726"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf62487380638765524bf1be7ea3f288d8adac"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf624868b9411330de489496743820c314b700"},
        # {"http": "http://05RHeL:Ypuj1X@185.191.142.8:9072", "api_key": "5b3ce3597851110001cf6248ab160f6af1e54cec8be87a0761f0da6a"},

        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248e96625bc830a43e9aa89667866dc3caf"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248fdad25d0132d4d0ab1d5f945f7277ef3"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf62483038c0942055491884f83cfecda1081a"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248e7ac9c52896740cc85c55346d4e026c0"},
        # {"http": "http://05RHeL:Ypuj1X@185.200.170.168:9481", "api_key": "5b3ce3597851110001cf6248dcfcf61f48294782a2c5b73c009c29f2"}, 

        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf62481df2a896077142b383c282327a4f8d4f"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf62488b5067ecaf5f49da8dd0af4948602c06"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf6248acb0b866a67d4c07a3b9cc55ac3d6c49"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf62486932045340b2438ebed369aa64a19545"},
        # {"http": "http://05RHeL:Ypuj1X@185.184.78.50:9631", "api_key": "5b3ce3597851110001cf624809d585f734f840008e0bead2e03da3a2"},

        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf62481bc692734ef949f98857fb7edc9bcf5a"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf62485875db9461e940049d2e293f4c3b2623"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf624849ff2636a3c848b7b57b9624c15751b0"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf624802f8051ea2074d02990bdb12f217af7c"},
        # {"http": "http://05RHeL:Ypuj1X@185.147.129.83:9202", "api_key": "5b3ce3597851110001cf62486f2e914873a44bfe840b002af262ee1b"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf6248de86ae2c4b144ec690260dcc94acc5b2"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf624829a3ae8cf3744469ace193cd149c5eec"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf62489c026e82dea34ad1afdcfb9c0feb9953"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf6248665f74829a75470d9b9863167b37ded5"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.215:9580", "api_key": "5b3ce3597851110001cf6248da9b43771cfa4d288b658a9ee2c89f3b"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf6248265ba9842e2143198b8ebb5b7310692b"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf62483eb0ec2f06194d8a9b030ed14248912d"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf62487a9c2fbb109149c992026a83a47245db"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf62488b5f9d03eb84494e8a198a8b5822877d"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.94:9717", "api_key": "5b3ce3597851110001cf624855101e4a66bd4a728e426b8558827e63"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf62485ee15974c671414eaecf64685fc9533e"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf624832da76560632437b91048458f5d665c1"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf6248e356f45757de4a6c9738f31e02aa8c82"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf6248079a959b5b2641ccb3854b3ec36be868"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.208.252:9233", "api_key": "5b3ce3597851110001cf62484abe41de1cec4f339d65bd6414b0d01a"},
        
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf624898702b3c1d354d459a47214b9b58de25"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf62487aabff5d81b74853bc1a552fb300513b"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf624838487e91196f49bdb66b9b1224a2941b"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf624804e22b20dd0c412499043268dbd0a2ec"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.209.2:9621", "api_key": "5b3ce3597851110001cf6248d666a3f39b404a7590bcf536841743d0"},

        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248dc0c78d22e95463c8ff20f29979a4cd0"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf62486e017a0e33a14a208d741cff30c9fa55"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248385a1582d5f640379198efebc621c184"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248f51cc86d243c407587f38bd5e27ec95b"},
        # {"http": "http://05RHeL:Ypuj1X@194.28.210.189:9407", "api_key": "5b3ce3597851110001cf6248fb1f4a40c636477dbbe5c463df97c620"},

        # {"http": "http://PAUBax:EK3sMk@31.44.191.78:9116", "api_key": "5b3ce3597851110001cf624880a5d7452e2243a9bc4a4c00954eb162"},
        # {"http": "http://PAUBax:EK3sMk@31.44.191.78:9116", "api_key": "5b3ce3597851110001cf6248f7150794e66a4ce5b9a1d1e189b09ab0"},
        # {"http": "http://PAUBax:EK3sMk@31.44.191.78:9116", "api_key": "5b3ce3597851110001cf624870c8a87208a84e2e92a8fa484b800b05"},
        # {"http": "http://PAUBax:EK3sMk@31.44.191.78:9116", "api_key": "5b3ce3597851110001cf624897046e8da7884224a08a91eb0df23acd"},
    ]
    
    with ThreadPoolExecutor(max_workers=len(proxy_list)) as executor:
        params_files = list(executor.map(create_params_file, proxy_list))

    script_path = "main_part.py"
    input_file = "csv/all_points.csv"
    output_file = "csv/matrix.csv"
    type_arg = "matrix"
    start_index = 1  # начальный индекс

    with ThreadPoolExecutor(max_workers=len(proxy_list)) as executor:
        for params_file in params_files:
            executor.submit(
                execute_script_through_proxy, 
                script_path, input_file, output_file, params_file, type_arg, {"http": ""}, start_index
            )
            start_index += 2  # увеличиваем начальный индекс на 10 для следующего прокси
