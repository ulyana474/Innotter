import React from "react";
import '../styles/searchline.css'
import '../styles/users.css'
import '../styles/homepage.css'
import my_page from '../images/my_page.svg';
import logo from '../images/logo.svg';
import like from '../images/liked.svg'
import smile from '../images/smile.svg'
import post from '../images/post.svg'

const Users = () => 
<div>
    <div className="grid-users">
        <div className="logo-users">
            <ul className="users-horizontal-list">
                <li>Innotter</li>
                <li>users</li>
            </ul>
            <form>
                <input type="text" className="users-search-line"></input>
            </form>
        </div>
        <div className="homepage-my-page"><img src={my_page}></img></div>
    </div>
    <div className="flex-user-blocks">
        <div className="user-block">
            <p className="users-username">Username</p>
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