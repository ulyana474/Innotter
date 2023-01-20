import React from "react";
import '../styles/searchline.css'
import '../styles/users.css'
import '../styles/homepage.css'
import my_page from '../images/my_page.svg';
import like from '../images/liked.svg'
import smile from '../images/smile.svg'
import post from '../images/post.svg'
import { Link } from 'react-router-dom'

const Users = () => 
<div>
    <div className="upper-line">line</div>
    <div className="grid-logo">
        <div className="logo-users">
            <ul className="users-horizontal-list">
                <li>Innotter</li>
                <li>users</li>
            </ul>
            <form>
                <input type="text" className="users-search-line"></input>
            </form>
        </div>
        <div className="my-page"><img src={my_page}></img></div>
    </div>
    <div className="flex-user-blocks">
        <div className="user-block">
            <Link to="/user-account" className="users-username">Username</Link>
            <div className="statistics">
                <ul className="stat-list">
                    <li>173</li>
                    <li><img src={like} className="list-img"></img></li>
                    <li>20</li>
                    <li><img src={smile} className="list-img"></img></li>
                    <li>15</li>
                    <li><img src={post} className="list-img"></img></li>
                </ul>
            </div>
        </div>
    </div>
</div>
export default Users