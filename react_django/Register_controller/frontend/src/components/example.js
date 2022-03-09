import React, { Component, useState } from 'react';
import List from "./list";
import Database from "./database";
import Createuser from "./Createuser";
import { BrowserRouter as Router, Routes, Route, Link, Redirect} from "react-router-dom";
/*
function InputSample() {
  const [text, setText] = useState('');

  const onChange = (e) => {
    setText(e.target.value);
  };

  const onReset = () => {
    setText('');
  };

  return (
    <div>
      <input onChange={onChange} value={text}  />
      <button onClick={onReset}>초기화</button>
      <div>
        <b>값: {text}</b>
      </div>
    </div>
  );
}
*/
export default class InputSample extends Component {
    constructor(props){
        super(props);
    }

    render(){
        return (
          <div>
          <ul>
          <li><Link to="/create">DB</Link></li>
          <li><Link to="/join">list</Link></li>
          <li><Link to="/register">register</Link></li>
        </ul>
        <Router>
           <Routes>
                  <Route path='/join' element={List}></Route> 
                  <Route path='/create' element = {Database}></Route>
                  <Route path='/register' element={Createuser}></Route>
          </Routes>     
        </Router>
        </div>
        );
    }
}

