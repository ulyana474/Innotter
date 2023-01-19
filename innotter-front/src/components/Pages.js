import React from "react";
import '../styles/searchline.css'
import '../styles/users.css'
import '../styles/homepage.css'
import '../styles/pages.css'
import my_page from '../images/my_page.svg';
import Page from "./Page";

const Pages = () => 
<div>
    <div className="upper-line">line</div>
    <div className="grid-logo">
        <div className="logo-users">
            <ul className="users-horizontal-list">
                <li>Innotter</li>
                <li>pages</li>
            </ul>
            <form>
                <input type="text" className="users-search-line"></input>
            </form>
        </div>
        <div className="my-page"><img src={my_page}></img></div>
    </div>
    <div className="flex-pages">
        <Page />
        <Page />
        <Page />
    </div>
</div>
export default Pages