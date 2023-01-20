import React from "react";
import '../styles/tags.css'
import my_page from '../images/my_page.svg';
import Tag from "./Tag";


const Tags = () => 
    <>
    <div className="upper-line">line</div>
    <div className="grid-tags">
        <button className="new-tag-button">new tag</button>
        <img src={my_page} className="tags-my-page"></img>
    </div>
    <div className="tags-logo">
        <ul className="tags-horizontal-list">
            <li>Innotter</li>
            <li>tags</li>
        </ul>
    </div>
    <Tag />
    <Tag />
    <Tag />
    </>

export default Tags