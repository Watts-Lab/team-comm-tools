import React from 'react';
import '../../App.css';

const current = [
  {
    name: 'Shruti Agarwal',
    image: './team-process-map/shruti.png'
  },
  {
    name: 'Gina Chen',
    image: './team-process-map/gina.jfif'
  },
  {
    name: 'Priya DCosta',
    image: './team-process-map/priya.png'
  },
  {
    name: 'Evan Rowbotham',
    image: './team-process-map/evan.png'
  },
  {
    name: 'Yuxuan Zhang',
    image: './team-process-map/yuxuan.jpg'
  },
  {
    name: 'Amy Zheng',
    image: './team-process-map/amy.png'
  },
  {
    name: 'Helena Zhou',
    image: './team-process-map/helena.png'
  }
]

const alumni = [
  {
    name: 'Yuluan Cao',
    image: './team-process-map/yuluan.jpg'
  },
  {
    name: 'Nikhil Kumar',
    image: './team-process-map/nikhil.png'
  },
  {
    name: 'Yashveer Singh Sohi',
    image: './team-process-map/yashveer.png'
  },
  {
    name: 'Eric Zhong',
    image: './team-process-map/eric.jfif'
  }
]

function Team() {
  return (
    <div className='team-container'>
      <h1 className='team'>
        Meet Our Team
      </h1>

      <div className="emily">
        <div className='emily-member'>
          <img src='./team-process-map/xinlan-emily-hu.jpg' alt={'Xinlan Emily Hu'} className="emily-image" />
          <h2> Xinlan Emily Hu </h2>
          <h4> Project Lead </h4>
          <h3> PhD Student at the University of Pennsylvania</h3>
        </div>
      </div>

      <h1 class="team-headers"> Current Members </h1>
      <div className="current">
        {current.map((member, index) => {
          let title = 'Undergraduate Student, UPenn';
          if (member.name === 'Evan Rowbotham') {
            title = 'Undergraduate Student, FSU';
          } 
          else if (member.name === 'Gina Chen') {
            title = 'Data Scientist';
          } 
          else if (member.name === 'Yuxuan Zhang') {
            title = 'Data Scientist';
          }
          else if (member.name === 'Priya DCosta') {
            title = 'Graduate Student, UPenn';
          }

          return (<div key={index} className='current-member'>
            <img src={member.image} alt={member.name} className="current-image" />
            <h2>{member.name}</h2>
            <h3> {title} </h3>
          </div>
          );
        })}
      </div>

      <h1 class="team-headers"> Alumni </h1>
      <div className="alumni">
        {alumni.map((member, index) => {
          let title = 'Undergraduate Student, UPenn';
          if (member.name === 'Yuluan Cao') {
            title = 'Graduate Student, UPenn';
          } 
          else if (member.name === 'Yashveer Singh Sohi') {
            title = 'Data Scientist';
          } 
          else if (member.name === 'Eric Zhong') {
            title = 'Undergraduate Student, Cornell';
          }

          return (<div key={index} className='alumni-member'>
            <img src={member.image} alt={member.name} className="alumni-image" />
            <h2>{member.name}</h2>
            <h3> {title} </h3>
          </div>
          );
        })}
      </div>
    </div>
  );
}

export default Team;