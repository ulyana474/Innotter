import React from "react";
import '../styles/homepage.css'
import { Link } from 'react-router-dom'
import Searchline from "./Searchline";
import logo from '../images/logo.svg';
import my_page from '../images/my_page.svg';
import Post from "./Post";


const Homepage = () => 
    <body className="body">
        <div className="upper-line">line</div>
        <div className="grid-logo-search">
            <div className="grid-item grid-item-log">
                <div className="innotter-logo">
                    <img src={logo} alt="logo image"></img>
                </div>
                <Link to="/sign" className="button-sign-up">Sign in</Link>
                <Link to="/register" className="button-register">Register</Link>
            </div>
            <div className="grid-item grid-item-search">
                <div className="search-fields">
                    <ul className="horizontal-list">
                        <li><Link to="/users" className="link-list">users</Link></li>
                        <li><Link to="/pages" className="link-list">pages</Link></li>
                        <li><Link to="/tags" className="link-list">tags</Link></li>
                    </ul>
                </div>
                <Searchline />
            </div>
            <div className="my-page"><img src={my_page}></img></div>
        </div>
        <main className="post-wrapper">
            <Post id="upper-post"/>
            <Post />
            <Post />
        </main>
    </body>

export default Homepage