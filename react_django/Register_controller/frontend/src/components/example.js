import React, { Component, useState } from 'react';
import List from "./list";
import Database from "./database";
import Createuser from "./Createuser";
import { BrowserRouter as Router, Routes, Route, Link, Redirect} from "react-router-dom";
import Userlist from "./list";
import Usercreate from "./Createuser";
import Showlist from './showlist';

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

const handlePushUser = async()=>{
  try{
    setIsloading(true);
    const createlog = await Usercreate(name, age, image);
  }catch (err){
    alert(err)
  }
  setIsloading(false);
}

const axiosUserlist = async () =>{
  try{
    const develop = await Userlist()
    console.log(develop.data)
    setDevelop(develop.data)
  }catch (err){
    alert(err)
  }
}

export default class InputSample extends Component {
    constructor(props){
        super(props);
    }

    render(){
        return (
          <div>
            <Router>
            <h1>This is start page.</h1>
            <a href = '/register'> Register </a>
            <a style={{display: "table-cell"}} href="/register" target="_blank">text</a>

            <h3> <Link to = '/GotoList'>If you want to see userinfo click here</Link></h3>
            
              <Routes>
                      <Route path='/GotoList' element={<List/>}></Route> 
                      <Route path='/showdb' element ={<Database/>}></Route>
                      <Route path='/register' element={<Createuser/>}></Route>
                      <Route path= '/showlist' element ={<Showlist/>}></Route>
              </Routes>     
            </Router>
          </div>
        );
  }
}
