import './Ui.css';

import Panel from './panel/Panel.jsx'
import Info from './info/Info.jsx';

function Ui() {
    return ( 
        <>
            <div id="Ui">
                <Panel />
                <Info/>
            </div>
        </>
     );
}

export default Ui;