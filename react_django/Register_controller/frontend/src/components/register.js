import React, { Component} from "react";
import {render} from "react-dom";
import {useState} from "react";
function register(){

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

export default register;