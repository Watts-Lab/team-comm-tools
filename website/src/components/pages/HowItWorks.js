import React, {useEffect} from 'react';
import '../../App.css';

function HowItWorks() {
  useEffect(() => {
    document.title = "How It Works | Team Communication Toolkit";
  }, []);

  return (
    <div className='how-it-words-container'>
      <h1 className='how-it-works'>
        How It Works
      </h1>

      <p>
        Our toolkit is implemented completely in Python, with our code open-sourced via GitHub,
        and our documentation managed by ReadTheDocs (using Sphinx).
      </p>
      <br />
      <p>
        The typical user should not need to directly interact with the original source code,
        and should be able to directly download our package via pip. However, we welcome open-sourced
        contributions to the toolkit, particularly bug reports and suggestions for additional features to include.
        We believe these contributions will allow the toolkit to become a living resource for anyone interested
        in understanding and quantifying conversations.
      </p>
      <br />
      <p1> More information coming soon: </p1>
      <p> Our toolkit is currently pre-launch. Details on how to download our package
        will be released after our package officially launches later this summer (August 2024).
      </p>

      <h1 className='how-it-works-headers'> Technical Documentation: ReadTheDocs </h1>
      <p>
        We use ReadTheDocs to host the latest documentation for the toolkit: <a href="https://conversational-featurizer.readthedocs.io/">https://conversational-featurizer.readthedocs.io/</a>
      </p>
      <br />
      <p>
        Please explore the technical documentation to learn more about the following:
      </p>
      <div className='bullet-points'>
        <ul>
          <li>How to import and use the toolkit;</li>
          <li>Technical details for how conversational attributes are implemented;</li>
          <li>Conceptual details for how to understand and interpret the conversational attributes we measure.</li>
        </ul>
      </div>

      <div className='github'>
        <h1 className='how-it-works-headers'> Open-Sourced Code: GitHub </h1>
        <p>
          The implementation details of each feature is public on GitHub, at the following link: <a href="https://github.com/Watts-Lab/team-process-map">Github</a>.
        </p>
        <br />
        <p>
          We encourage anyone interested in developing a feature to either contact <a href="http://xinlanemilyhu.com">Xinlan Emily Hu</a> or to make a pull request.
        </p>
      </div>

    </div>
  );
}

export default HowItWorks;