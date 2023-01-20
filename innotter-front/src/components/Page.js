import React from "react";
import '../styles/page.css'
import page_img from '../images/page.svg'
import { Link } from "react-router-dom";

const Page = () => 
    <div className="page-block">
        <div className="flex-page-info">
            <p className="page-name">Nice_page</p>
            <img src={page_img} className="page-img"></img>
        </div>
        <p className="page-text">Believing neglected so so allowance existence departure in. In design active temper be uneasy. Thirty for remove plenty regard you summer though. He preference connection astonished on of ye</p>
        <Link to="/user-page" className="see-page-button">see page</Link>
    </div>

export default Page