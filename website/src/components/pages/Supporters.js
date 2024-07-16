import React, { useEffect } from 'react';
import '../../App.css';

function Supporters() {
  useEffect(() => {
    document.title = "Our Supporters | Team Communication Toolkit";
  }, []);

  return (
    <div className="supporters-container">
      <h1 className="supporters"> Our Supporters </h1>

      <p>
        Our project is supported by the Computational Social Science Lab (CSSLab)
        at the University of Pennsylvania and the Wharton AI & Analytics Initiative (WAIAI).
        We are also proud to have been recognized by the International Association of Conflict Management (IACM)
        with the 2024 Technology Innovation Award.
      </p>
    </div>
  );
}

export default Supporters;