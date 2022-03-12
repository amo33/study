import React, { Component} from "react";
import {render} from "react-dom";
import {useState} from "react";
function Showlist(){

    const [text, setText] = useState('');

    const onChange = (e) => {
        setText(e.target.value);
    };

    const onReset = () => {
        setText('');
    };
    const handleClickTosee = () =>{
        $.ajax({
            url : "api/home",
            method : "get",
            datatype : "JSON",
            async : true,
            enctype : 'multipart/form-data',
            contentType : false,
            processData : false,
            success : (file)=>{
                console.log(1000);
                console.log(file);
            },
            error : ()=>{
                alert("error!");
            },
        });
    };
    return (
        <div>
        <input onChange={onChange} value={text}  />
        <button onClick={onReset}>초기화</button>
        <button onClick={handleClickTosee}>리스트 보기</button>
        <div>
            <b>값: {text}</b>
        </div>
        </div>
    );
}

export default Showlist;