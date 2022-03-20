import React, { Component} from "react";
import {Link} from "react-router-dom";

function ShowDetail(props){
    if(props.state != 0 && props.state!= undefined){
        return (
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
                    let add = val.image_path
                    return (
                        <tr key={key}>
                        <td>{val.username}</td>
                        <td>{val.age}</td>
                        <td>{val.user_id}</td>
                        <td><img src= {require(val.image_path).default}/></td>
                        </tr>
        )
        })}
        </tbody>
    </table>

        )
    }
    else{
        return null;
    }
}

export default ShowDetail;