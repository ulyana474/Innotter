import React, { useState } from "react";
import { Link } from 'react-router-dom'
import '../styles/menu.css'
import cross from '../images/cross.svg'


const Menu = ({active, setActive}) => {
    return (<div className={active ? 'menu active' : 'menu'}>
        <img onClick={() => setActive(false)} src={cross} className="cross-img"></img>
        <ul className={active ? 'menu-content' : 'menu close'}>
            <li><Link to="/users" className="menu-item">users</Link></li>
            <li><Link to="/pages" className="menu-item">pages</Link></li>
            <li><Link to="/tags" className="menu-item">tags</Link></li>
            <li><Link to="/sign" className="menu-item">sign in</Link></li>
            <li><Link to="/register" className="menu-item">register</Link></li>
        </ul>
    </div>
)
}

export default Menu;