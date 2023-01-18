import React from "react";
import '../styles/homepage.css'
import '../styles/signin.css'
import '../styles/register.css'

const Register = (props) => 
<div>
    <div className="upper-line">line</div>
    <div className="welcome-message">
        <p className="welcome-text">Welcome to Innotter!</p>
    </div>
    <div className="form-block">
        <form className="flex-input">
            <label for="Username" className="label">username:</label>
            <input type="text" className="signin-line"></input>
        </form>
        <form className="flex-input">
            <label for="Password" className="label">password:</label>
            <input type="text" className="signin-line"></input>
        </form>
        <form className="flex-input">
            <label for="Password" className="label_confirm">confirm password:</label>
            <input type="text" className="signin-line"></input>
        </form>
        <form className="flex-input">
            <label for="Email" className="label_email">email:</label>
            <input type="text" className="signin-line"></input>
        </form>
        <form className="flex-input">
            <label for="First_name" className="label">first name:</label>
            <input type="text" className="signin-line"></input>
        </form>
        <form className="flex-input">
            <label for="Last_name" className="label">last name:</label>
            <input type="text" className="signin-line"></input>
        </form>
        <button className="button-sign-in">sign in</button>
    </div>
</div>
export default Register