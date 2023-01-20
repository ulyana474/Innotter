import React from "react";
import '../styles/userPage.css'
import my_page from '../images/my_page.svg';
import logo from '../images/logo.svg';
import image from '../images/page.svg'

const UserPage = () => 
    <>
    <div className="upper-line">line</div>
    <div className="grid-user-page">
        <img src={logo} className="logo-user-page"></img>
        <div className="user-page-block">
            <div className="page-uuid">1256132t23</div>
            <div className="flex-row-page-info">
                <div className="flex-column-user-info">
                    <p className="user-page-username">Username</p>
                    <p className="user-page-pagename">Page name</p>
                </div>
                <img src={image} className="user-image"></img>
            </div>
        </div>
        <img src={my_page} className="user-my-page"></img>
        <div className="link-text">
            <div className="flex-column-link-descr">
            <div className="link-posts-followers">
                                <p className="see-followers">see followers</p>
                                <p className="see-posts">see posts</p>
                </div>
                <p className="page-descr">Believing neglected so so allowance existence departure in. In design active temper be uneasy. Thirty for remove plenty regard you summer though. He preference connection astonished on of ye</p>
            <hr/>     
            <div className="page-tags">
                <ul className="tags-list">
                    <li>#likesforlikes</li>
                    <li>#likesforlikes</li>
                    <li>#likesforlikes</li>
                    <li>#likesforlikes</li>
                </ul>
            </div>         
            </div>
            </div>
    </div>
    </>
export default UserPage