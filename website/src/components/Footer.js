import React from 'react';
import './Footer.css';
// import { Button } from './Button';
// import { Link } from 'react-router-dom';

function Footer() {
    return (
        <div className='footer-container'>
            <div className='logo-links'>
                <a href='https://css.seas.upenn.edu/'>
                    <img src={`${process.env.PUBLIC_URL}/csslab_logo.png`} alt='csslabLogo' />
                </a>
                <a href='https://ai-analytics.wharton.upenn.edu/'>
                    <img src={`${process.env.PUBLIC_URL}/wharton_logo_white.png`} alt='whartonLogo' />
                </a>
            </div>
            <br />
            <p style={{color: 'white'}}> &copy; Copyright 2024, Xinlan Emily Hu and the Team Communication Toolkit Research Group</p>
        </div>
    );
}

export default Footer;