import React, {useEffect} from 'react';
import '../../App.css';

function Research() {
  useEffect(() => {
    document.title = "Research | Team Communication Toolkit";
  }, []);

  return (
    <div className='research-container'>
      <h1 className='research'>
        Research
      </h1>

      <p>
        The Team Communication Toolkit is a research project that has been featured at the International Conference on Computational Social Science (IC2S2) and the Academy of Management (AOM) Annual Meeting.
        It is the winner of the 2024 IACM Technology Innovation Award (by the International Association for Conflict Management).
      </p>

      <h1 className='research-headers'> Background </h1>
      <p>
        Our toolkit seeks to address the “garden of forking paths” problem (Gelman and Loken, 2014), specifically within the domain of team conversations.
        In the study of team conversations, the same construct can be operationalized in many similar but not entirely compatible ways.
        For example, to quantify the concept of the diversity of ideas generated in a conversation, a researcher might compare each utterance to those that came before it (a measure that Gray et al., 2019 call forward flow); compare each utterance to the average utterance in the entire conversation (a measure that Riedl and Woolley, 2017 call information diversity); or compare each speaker’s average utterance with every other speaker’s average utterance (a measure that Lix et al., 2022 call discursive diversity).
        While each of these measures is reasonable in its own right and validated in an empirical context, which one is the “correct” way of quantifying the diversity of ideas?
      </p>
      <br />
      <p>
        This case study highlights a key problem in social science: while many measures are related, researchers are typically able to evaluate only the results of one specific sequence of decisions.
        Consequently, it is difficult to be aware of related constructs or operationalizations, and it can be costly to implement multiple versions of each measure from scratch.
        More importantly, the high cost of exploring beyond one particular set of decisions makes it difficult to test the robustness of research findings.
        Evidence from “many analysts” (e.g., Silberzahn et al., 2018) and “multiverse analysis” (e.g., Steegen et al., 2016) have demonstrated that various reasonable data processing decisions can lead to inconsistent findings.
        Thus, if forward flow predicts one outcome and discursive diversity predicts another, there should exist a method to easily compute both metrics and provide researchers with the fuller picture.
      </p>
      <br />
      <p>
        The objective of the Team Communication Toolkit is to provide such a fuller picture.
        By extracting, structuring, and implementing attributes of conversations from the academic literature, we hope to create a repository that helps researchers rapidly bootstrap analyses, explore a range of options for measuring constructs of interest, and access a “multiverse” of analyses right out of the box.
      </p>
      <br />
      <p> <em>References</em> </p>
      <div className='bullet-points'>
        <ul>
          <li>Gelman, A., & Lokem, E. (2014). The Statistical Crisis in Science Data-Dependent Analysis—A ‘Garden of Forking Paths’—Explains Why Many Statistically Significant Comparisons Don’t Hold Up. American Scientist, 102(6), 460. </li>
          <li>Gray, K., Anderson, S., Chen, E. E., Kelly, J. M., Christian, M. S., Patrick, J., Huang, L., Kenett, Y. N., & Lewis, K. (2019). “Forward Flow”: A New Measure to Quantify Free Thought and Predict Creativity. American Psychologist, 74(5), 539–554.</li>
          <li>Lix, K., Goldberg, A., Srivastava, S. B., & Valentine, M. A. (2022). Aligning Differences: Discursive Diversity and Team Performance. Management Science, 68(11), 8430–8448. <a href='https://doi.org/10.1287/mnsc.2021.4274'> https://doi.org/10.1287/mnsc.2021.4274 </a> </li>
          <li> Riedl, C., & Woolley, A. W. (2017). Teams Vs. Crowds: A Field Test of The Relative Contribution of Incentives, Member Ability, and Emergent Collaboration to Crowd-Based Problem Solving Performance. Academy of Management Discoveries, 3(4), 382-403. </li>
          <li> Silberzahn, R., Uhlmann, E. L., Martin, D. P., Anselmi, P., Aust, F., Awtrey, E., ... & Nosek, B. A. (2018). Many Analysts, One Data Set: Making Transparent How Variations in Analytic Choices Affect Results. Advances in Methods and Practices in Psychological Science, 1(3), 337-356. <a href='https://doi.org/10.1177/2515245917747646'> https://doi.org/10.1177/2515245917747646 </a></li>
          <li> Steegen, S., Tuerlinckx, F., Gelman, A., & Vanpaemel, W. (2016). Increasing Transparency Through a Multiverse Analysis. Perspectives on Psychological Science, 11(5), 702-712.  <a href='https://doi.org/10.1177/1745691616658 '> https://doi.org/10.1177/1745691616658 </a></li>
        </ul>
      </div>

      <h1 className='research-headers'> Applications </h1>
      <p> We have two broad goals for the toolkit: first, to make conversation analysis accessible (by lowering the cost of analyzing them) and second, to allow researchers to conduct sensitivity analysis of findings (by easily comparing results from one method of operationalizing a construct with results from another method). </p>
      <br />
      <p> Examples of research questions that we are currently exploring with the toolkit include: </p>
      <div className='bullet-points'>
        <ul>
          <li> <strong> Analyzing Conflict: </strong> Identifying conversational markers that indicate whether or not a conflict is likely to be resolved productively;</li>
          <li> <strong> Analyzing Negotiations: </strong> Identifying conversational markers that suggest that parties are likely to feel satisfied after a negotiation; </li>
          <li> <strong> Analyzing Longitudinal Friendships</strong> Identifying conversational attributes of conversations among groups of college students whose text message chats remain active over many months, as opposed to fizzling out early. </li>
        </ul>
      </div>
      
      <br />
      <br />
      <p> <strong> We’re interested in working with you / hearing about YOUR ideas for studying conversations! </strong>
      We hope that other researchers will use the Team Conversation Toolkit to study research questions of their own.
      </p>
      
      <h2 className='research-subheaders'> Collaborations </h2>
      <p> If you are interested in a collaboration, please reach out to <a href='https://xinlanemilyhu.com'> Xinlan Emily Hu</a>.</p>


      <h2 className='research-subheaders'> Citation </h2>
      <p> <strong> A full manuscript describing our framework and toolkit is forthcoming. </strong> In the meantime, please use the following citation: </p>
      <br />
      <div className='bullet-points'>
        <ul> Hu, Xinlan Emily. “A Flexible Python-Based Toolkit for Analyzing Team Communication.” in "What are We Talking About? Natural Language Processing in Organizations." Academy of Management Proceedings. Vol. 2024. No. 1. Briarcliff Manor, NY 10510: Academy of Management, 2024. </ul>
      </div>
      
      
    </div>
  );
}

export default Research;