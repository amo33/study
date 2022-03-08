import React, { Component} from "react";
import {render} from "react-dom";
import InputSample from "./example";

export default class App extends Component{

    render(){
        return <p><InputSample /></p> ;      
    }
}

const appDiv = document.getElementById('app');
render(<App/>, appDiv); // appdiv를 찾은 공간에 <App/ > render 할거야 