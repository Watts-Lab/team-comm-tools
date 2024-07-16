import React, { useEffect } from 'react';
import '../../App.css';

function Contact() {
    useEffect(() => {
        document.title = "Contact | Team Communication Toolkit";
    }, []);

    return (
        <div className='contact-container'>
            <h1 className='contact'>
                Contact Us
            </h1>

            <p>
                For questions or comments about the Team Communication Toolkit, please reach out to <a href="http://xinlanemilyhu.com">Xinlan Emily Hu</a>.
            </p>

        </div>
    );
}

export default Contact;