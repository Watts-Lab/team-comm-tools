import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';
import { FaBars, FaTimes } from 'react-icons/fa';

function Navbar() {
    const [click, setClick] = useState(false);
    const handleClick = () => setClick(!click);
    const closeMobileMenu = () => setClick(false);

    return (
        <>
            <nav className="navbar">
                <div className="navbar-container">
                    <Link to="/" className="navbar-logo">
                        Team Communication Toolkit
                    </Link>
                    <div className='menu-icon' onClick={handleClick}>
                        {click ? <FaTimes /> : <FaBars />}
                    </div>
                    <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                        <li className='nav-item'>
                            <Link to='/' className='nav-links' onClick={closeMobileMenu}>
                                Home
                            </Link>
                        </li>
                        <li className='nav-item'>
                            <Link to='/Research' className='nav-links' onClick={closeMobileMenu}>
                                Research
                            </Link>
                        </li>
                        <li className='nav-item'>
                            <Link to='/HowItWorks' className='nav-links' onClick={closeMobileMenu}>
                                How It Works
                            </Link>
                        </li>
                        <li className='nav-item'>
                            <Link to='/Team' className='nav-links' onClick={closeMobileMenu}>
                                Team
                            </Link>
                        </li>
                        <li className='nav-item'>
                            <Link to='/Supporters' className='nav-links' onClick={closeMobileMenu}>
                                Our Supporters
                            </Link>
                        </li>
                        <li className='nav-item'>
                            <Link to='/Contact' className='nav-links' onClick={closeMobileMenu}>
                                Contact
                            </Link>
                        </li>
                    </ul>
                </div>
            </nav>
        </>
  )
}

export default Navbar