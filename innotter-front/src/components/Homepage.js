import React from "react";
import '../styles/homepage.css'
import Searchline from "./Searchline";
import logo from '../images/logo.svg';
import my_page from '../images/my_page.svg';
import Post from "./Post";


const Homepage = (props) => 
    <body className="body">
        <div className="upper-line">line</div>
        <div className="grid-logo-search">
            <div className="grid-item grid-item-log">
                <div className="innotter-logo">
                    <img src={logo} alt="logo image"></img>
                </div>
                <button onClick={() => props.setTitle("Signin")} className="button-sign-up">sign in</button>
                <button onClick={() => props.setTitle("Register")} className="button-register">register</button>
            </div>
            <div className="grid-item grid-item-search">
                <div className="search-fields">
                    <ul className="horizontal-list">
                        <li onClick={() => props.setTitle("Users")}>users</li>
                        <li>pages</li>
                        <li>tags</li>
                    </ul>
                </div>
                <Searchline />
            </div>
            <div className="homepage-my-page"><img src={my_page}></img></div>
        </div>
        <main className="post-wrapper">
            <Post id="upper-post"/>
            <Post />
            <Post />
        </main>
    </body>

export default Homepage