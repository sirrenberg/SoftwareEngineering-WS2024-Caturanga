import {useEffect, useState} from 'react';
import "../styles/Credits.css";
import smallImage_netlight from '../../public/netlight-logo.png';
import smallImage_FLEE from '../../public/flee.png';
import smallImage_ACLED from '../../public/acled-logo.png';
import FLEE_Credits_text from '../../public/FLEE_Credits.txt';
import ACLED_Credits_text from '../../public/ACLED_Credits.txt';
import NL_Credits_text from '../../public/NL_Credits.txt';

// Flee references:
const FLEE_LITERATURE = [
  {
    title: "Large-Scale Parallelization of Human Migration Simulation",
    authors: "Groen, D., Papadopoulou, N., Anastasiadis, P., Lawenda, M., Szustak, L., Gogolenko, S., Arabnejad, H. and Jahani, A.",
    journal: "IEEE Transactions on Computational Social Systems",
    year: 2023,
    link: "https://ieeexplore.ieee.org/document/10207715"
  },
  {
    title: "Sensitivity-driven simulation development: a case study in forced migration",
    authors: "Suleimenova, D., Arabnejad, H., Edeling, W.N. and Groen, D.",
    journal: "Philosophical Transactions of the Royal Society A",
    volume: 379,
    number: 2197,
    pages: "20200077",
    year: 2021,
    link: "https://bura.brunel.ac.uk/bitstream/2438/22565/1/FullText.pdf"
  },
  {
    title: "A generalized simulation development approach for predicting refugee destinations",
    authors: "Suleimenova, D., Bell, D. and Groen, D.",
    journal: "Scientific reports",
    volume: 7,
    number: 1,
    pages: "13377",
    year: 2017,
    link: "https://www.nature.com/articles/s41598-017-13828-9"
  },
  {
    title: "Simulating refugee movements: Where would you go?",
    authors: "Groen, D.",
    journal: "Procedia Computer Science",
    volume: 80,
    pages: "2251-2255",
    year: 2016,
    link: "https://bura.brunel.ac.uk/bitstream/2438/12519/1/Fulltext.pdf"
  },
  {
    title: "How Policy Decisions Affect Refugee Journeys in South Sudan: A Study Using Automated Ensemble Simulations",
    authors: "Suleimenova, D. and Groen, D.",
    journal: "Journal of Artificial Societies and Social Simulation",
    volume: 23,
    number: 1,
    year: 2020,
    link: "https://bura.brunel.ac.uk/bitstream/2438/19675/4/FullText.pdf"
  }
];

function Credits() {

    // Variables to Store the Credits texts from textfiles in the ../../public - directory:
    const[FLEEcreditsLines, setFLEECreditsLines] = useState<string[]>([]);
    const[ACLEDcreditsLines, setACLEDCreditsLines] = useState<string[]>([]);
    const[NLcreditsLines, setNLCreditsLines] = useState<string[]>([]);

    // Fetch all Credits - texts from the ../../public - directory:
    useEffect(() => {
        const fetchCreditsTexts = async () => {
            try {

                {/*Fetch text in ../../public/FLEE_Credits.txt and convert it to individual lines*/}
                const fleeresponse = await fetch(FLEE_Credits_text);
                const fleetext = await fleeresponse.text();
                const FLEElines = fleetext.split('\n');
                setFLEECreditsLines(FLEElines);

                {/*Fetch text in ../../public/ACLED_Credits.txt and convert it to individual lines*/}
                const acledresponse = await fetch(ACLED_Credits_text);
                const acledtext = await acledresponse.text();
                const ACLEDlines = acledtext.split('\n');
                setACLEDCreditsLines(ACLEDlines);

                {/*Fetch text in ../../public/NL_Credits.txt and convert it to individual lines*/}
                const nlresponse = await fetch(NL_Credits_text);
                const nltext = await nlresponse.text();
                const NLlines = nltext.split('\n');
                setNLCreditsLines(NLlines);
            } catch (error) {
                console.error('Error fetching credits texts:', error);
            }
        };

        fetchCreditsTexts();
    }, []);

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
                            <img className="small-image" src={smallImage_FLEE} alt="Small Image 1"/>
                        </a>
                    </div>
                    {/*Iterate over all lines and map them to card*/}
                    <div className="card-text">
                        {FLEEcreditsLines.map((line, index) => (
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
                            <img className="small-image" src={smallImage_ACLED} alt="Small Image 2"/>
                        </a>
                    </div>
                    {/*Iterate over all lines and map them to card*/}
                    <div className="card-text">
                        {ACLEDcreditsLines.map((line, index) => (
                            <p key={index}>{line}</p>
                        ))}
                    </div>
                </div>

                {/*Netlight Credits */}
                <div className="half-width-card">
                    <div className="card-content">
                        <h1 className="card-heading">Netlight</h1>
                        <a href="https://www.netlight.com/" target="_blank">
                            <img className="small-image" src={smallImage_netlight} alt="Small Image 2"/>
                        </a>
                    </div>
                    {/*Iterate over all lines and map them to card*/}
                    <div className="card-text">
                        {NLcreditsLines.map((line, index) => (
                            <p key={index}>{line}</p>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Credits;