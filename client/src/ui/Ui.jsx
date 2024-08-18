import './Ui.css';
import Panel from './panel/Panel.jsx'
import Info from './info/Info.jsx';

function Ui() {
    return ( 
        <>
            <div id="Ui">
                <Panel />
                <Info
                    sx={{
                        display: {
                            xs: 'none',
                            md: 'flex'
                        }
                    }}
                />
            </div>
        </>
     );
}

export default Ui;