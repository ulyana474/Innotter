import React, { useState } from "react";
import ReactRoundedImage from "react-rounded-image";
import '../styles/post.css'
import picture from '../logo.svg'
import like from '../images/like.svg'
import liked from '../images/liked.svg'


function Post() {
    const images = {like, liked};
    const [img, setImg] = useState(false);

    const imgChangeHandler = () => {
        if(!img) {
            setImg(true);
        }else{
            setImg(false)
        }
    };
    return(
        <div className="post-block">
            <div className="grid-post-info">
                <ReactRoundedImage 
                image={picture} 
                imageWidth="50"
                imageHeight="50"
                roundedSize="13"
                borderRadius="70"
                />
                <p className="post-username">username</p>
                <p className="post-created-time">12.01.2023 8pm</p>
            </div>
            <p className="post-text">Far quitting dwelling graceful the likewise received building. An fact so to that show am shed sold cold. Unaffected remarkably get yet introduced excellence terminated led. Result either design saw she esteem and. On ashamed no inhabit ferrars it ye besides resolve. Own judgment directly few trifling. Elderly as pursuit at regular do parlors. Rank what has into fond she</p>
            <div className="grid-post-reply-like">
                <form>
                    <input type="text" className="post-reply"></input>
                </form>
                <img src={!img ? like : liked} alt='like' className="post-like" onClick={imgChangeHandler}></img>
            </div>
        </div>
    )
    }

export default Post