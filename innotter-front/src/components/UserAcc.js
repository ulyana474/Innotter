import React from "react";
import '../styles/account.css'
import logo from '../images/logo.svg'
import image from '../images/page.svg'

const UserAcc = () => 
    <>
    <div className="upper-line">line</div>
    <div className="grid-user-account">
        <div className="flex-account">
        <div className="account-sidebar">   
            <img src={logo} className="img-sidebar"></img>
            <p className="account-email">any@gmail.com</p>
            <button className="new-page-button">new page</button>
        </div>
        </div>
        <div className="flex-user-info">
            <div className="account-info">
                <div className="flex-user">
                    <p className="user-role">User:</p>
                    <p className="account-username">Username</p>
                </div>
                <p className="account-description">For norland produce age wishing.<p className="change-title">change title</p></p>
                <img src={image} className='img-user'></img>
                <p className="change-picture">change picture</p>
            </div>
        </div>
    </div>
    </>
export default UserAcc