import React, { Component} from "react";
import { useState } from "react";
import axios from "axios";
/*
const Getimage = () =>{
    axios.get('http://127.0.0.1:3000/api/detail?user_id='+props.state+'&method='+props.methods)
    .then((Response) =>{
        handleimgpath(Response.data)
    })
    .catch((Error)=>{
        console.log(Error);
    })
}
const handleimgpath = (val) =>{
    setimgpath([...val])
}
*/
function ShowDetail(props){
    // const [img_path, setimgpath] = useState(''); 

    if(props.state != 0 && props.state!= undefined){
        return (
            <div>
                <h4>{props.method}</h4>
            <table>
                <thead>
                    <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>User_id</th>
                    <th>Image</th>
                    </tr>
                </thead>
                <tbody>

                    {props.data.map((val, key) => {
                    return (
                        <tr key={key}>
                        <td>{val.username}</td>
                        <td>{val.age}</td>
                        <td>{val.user_id}</td>
                        <td><img src= {process.env.PUBLIC_URL+val.image_path}/></td>
                        </tr>
        )
        })}
        </tbody>
    </table>
    </div>
        )
    }
}

export default ShowDetail;