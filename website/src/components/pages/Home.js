import React, {useEffect} from 'react';
import '../../App.css';
import { Link } from 'react-router-dom';

function Home() {
    useEffect(() => {
        document.title = "Team Communication Toolkit";
      }, []);

    return (
        <div className='home-container'>
            <div className='background-container'>
                <h1 className='welcome'>
                    Welcome!
                </h1>
            </div>

            <div className="home-body">
                <h1 className='home-headers'>
                    The Team Communication Toolkit
                </h1>
                <p>
                    The Team Communication Toolkit is a research project
                    and Python package that aims to make it easier for social scientists to explore text-based conversational data.
                </p>

                <h1 className='home-subheaders'>
                    Our Goal: Demystify the Science of Conversations.
                </h1>
                <p>
                    Conversations are incredibly rich sources of data.
                    They allow us to coordinate action, resolve differences, and learn new things from each other — and studying conversation
                    can enhance our understanding of many domains, including teamwork, conflict management, and deliberation, among others.
                </p>
                <br />
                <p>
                    However, it can be overwhelming to even begin analyzing a conversation: there are so many potentially relevant attributes,
                    from simple measures of how much is being said (e.g., the number of words, the number of turns) to complex measures of sentiment, temporal patterns,
                    and dynamics between speakers.
                    Studying conversations often means having to select among these different options and implement ways to quantify each attribute — from scratch.
                </p>
                <br />
                <p>
                    We believe that researchers shouldn’t have to “reinvent the wheel” when analyzing conversations.
                    Our goal is to provide scientists with a systematic way of thinking about conversational dimensions, as well as a toolkit to place hundreds of
                    research-backed conversational features right at their fingertips.
                </p>
                <br />
                <p>
                    To learn more about our research, please visit the <Link to="/Research">Research</Link> page.
                </p>

                <h1 className='home-subheaders'>
                    Seven Basic Categories of Conversations
                </h1>
                <p> Our toolkit is rooted in systematic review of the conversational literature, in which we identify seven basic
                    categories of conversational attributes:
                </p>
                <br />
                <div className='bullet-points'>
                    <ol>
                        <li> <strong> Quantity </strong> (or how much you say); </li>
                        <li> <strong> Pace </strong> (or the timing of when you say it); </li>
                        <li> <strong> Content </strong> (or what you say); </li>
                        <li> <strong> Engagement </strong> (or how you react to others); </li>
                        <li> <strong> Equality </strong> (or who is doing the talking); </li>
                        <li> <strong> Emotion </strong> (the valence of what you say); and </li>
                        <li> <strong> Variance </strong> (or the similarities and differences between what people say).</li>
                    </ol>
                </div>
                <br />
                <p> Thinking about conversations along these dimensions can help researchers think about the different attributes that they can consider. </p>

                <h1 className='home-subheaders'>
                    Download our Python Package (Coming Soon in August 2024!)
                </h1>
                <p>
                    To make exploration of conversations more accessible, our framework is accompanied by a Python package, to be released soon.
                    We think of this toolkit as a living representation of our framework; it seeks not only to discuss dimensions of conversations in the abstract,
                    but also to measure and quantify them in real data.
                    This allows researchers to explore how different dimensions that have been proposed by previous research may apply to their own datasets.
                    Our toolkit’s modular design makes it easy to add new dimensions as they are proposed, allowing it to be updated alongside knowledge in the field.
                </p>
                <br />
                <p>
                    Our toolkit can turn text-based conversational data into hundreds of conversational features at three different levels of analysis: (1) features for each utterance;
                    (2) features for each speaker; and (3) features for the conversation as a whole.
                </p>
                <br />
                <p>
                    More information about our toolkit can be found in the <Link to="/HowItWorks">How It Works</Link> page.
                </p>

            </div>

        </div>
    );
}

export default Home;