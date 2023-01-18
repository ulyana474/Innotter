import React, {useState} from "react";
import './App.css';
import Homepage from './components/Homepage';
import Signin from './components/Signin';
import Register from "./components/Register";
import Users from "./components/Users";

function App() {
  const [title, setTitle] = useState("Homepage");
  return (
    <div className="App">
      {title === "Signin" && <Signin  setTitle= {setTitle}/>}
      {title === "Homepage" && <Homepage  setTitle= {setTitle}/>}
      {title === "Register" && <Register  setTitle= {setTitle}/>}
      {title === "Users" && <Users  setTitle= {setTitle}/>}
    </div>
  );
}

export default App;
