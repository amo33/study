import React, { Component} from "react";
import {render} from "react-dom";
import Createuser from "./Createuser";
import { BrowserRouter as Router, Routes, Route, Link, Redirect} from "react-router-dom";
import List from "./list";

export default class App extends Component{

    constructor(props){
        super(props);
        this.handleclickRegister = this.handleclickRegister.bind(this);
    }
    handleclickRegister(){

    }
    render(){
        return (
          <div id = "start">
            
            <h1 style= {{cursor: 'default'}}>This is start page.</h1>
            <Router>
            <h3><a href = '/members' > If you want to register click here</a></h3>
            <h3> <a href = '/list' >If you want to see userinfo click here</a></h3>
            
              <Routes>
                      <Route path='/list' element={<List/>}></Route> 
                      <Route path='/members' element={<Createuser/>}></Route>
                     
              </Routes>     
            </Router>
          </div>
        );
  }
}

const appDiv = document.getElementById('app');
render(<App/>, appDiv); // appdiv를 찾은 공간에 <App/ > render 