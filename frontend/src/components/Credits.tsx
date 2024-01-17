import "../styles/Credits.css";
import { ACLED_CREDITS, ACLED_LOGO, FLEE_CREDITS, FLEE_LITERATURE, FLEE_LOGO, NETLIGHT_CREDITS, NETLIGHT_LOGO } from '../helper/constants/CreditsConstants';

function Credits() {
    // Return Collection of Cards, displaying Credits and Logos:
    return (
        <div className="credits-background">

            {/* First Row of Credits Fields*/}
            <div className="row">

                {/*FLEE Credits */}
                <div className="full-width-card">
                    <div className="card-content">
                        <h1 className="card-heading">FLEE</h1>
                        <a href="https://flee.readthedocs.io/en/master/" target="_blank">
                            <img className="small-image" src={FLEE_LOGO} alt="Small Image 1"/>
                        </a>
                    </div>
                    {/*Iterate over all lines and map them to card*/}
                    <div className="card-text">
                        {FLEE_CREDITS.split('\n').map((line, index) => (
                            <p key={index}>{line}</p>
                        ))}
                    </div>
                    {/* Add FLEE literature as small cards by mapping over FLEE_LITERATURE*/}
                    <div className="row" style={{marginTop: '20px'}}>
                        {FLEE_LITERATURE.map((paper, index) => (
                            <div key={index} className="sub-card" style={{marginRight: '20px'}}>
                                <a key={index} target="_blank" href={paper.link}>
                                    <div className="card-content">
                                        <h1 className="reference-heading">{paper.title}</h1>
                                    </div>
                                    <div className="card-text">
                                        <p style={{marginTop: '10px'}}>{paper.authors}</p>
                                        <p style={{marginTop: '10px'}}>{paper.journal}</p>
                                        <p>{paper.volume && `Volume: ${paper.volume}`}</p>
                                        <p>{`Year: ${paper.year}`}</p>
                                    </div>
                                </a>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Second Row of Credits Fields*/}
            <div className="row">

                {/*ACLED Credits */}
                <div className="half-width-card">
                    <div className="card-content">
                        <h1 className="card-heading">ACLED</h1>
                        <a href="https://acleddata.com/" target="_blank">
                            <img className="small-image" src={ACLED_LOGO} alt="Small Image 2"/>
                        </a>
                    </div>
                    {/*Iterate over all lines and map them to card*/}
                    <div className="card-text">
                        {ACLED_CREDITS.split('\n').map((line, index) => (
                            <p key={index}>{line}</p>
                        ))}
                    </div>
                </div>

                {/*Netlight Credits */}
                <div className="half-width-card">
                    <div className="card-content">
                        <h1 className="card-heading">Netlight</h1>
                        <a href="https://www.netlight.com/" target="_blank">
                            <img className="small-image" src={NETLIGHT_LOGO} alt="Small Image 2"/>
                        </a>
                    </div>
                    {/*Iterate over all lines and map them to card*/}
                    <div className="card-text">
                        {NETLIGHT_CREDITS.split('\n').map((line, index) => (
                            <p key={index}>{line}</p>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Credits;