import React, { Component} from "react";
import {render} from "react-dom";
import InputSample from "./example";

export default class App extends Component{

    render(){
        return <InputSample />;      // ㅇㅕ기에 p 태그를 넣으면 오류가 생기는데 아무래도 p 태그 안에 불러오는게 h1태그로 감싸져있어서 오류가 발생 
    }
}

const appDiv = document.getElementById('app');
render(<App/>, appDiv); // appdiv를 찾은 공간에 <App/ > render 할거야 