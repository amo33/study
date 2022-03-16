import React, { Component} from "react";
import {Link} from "react-router-dom";
function ShowData(props){
    const status = props.method;
    console.log(props.userdata);
    if(props.method != 'default'){
        return (
            <table>
                <thead>
                    <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Image_Flag</th>
                    </tr>
                </thead>
                <tbody>

                    {props.userdata.map((val, key) => {
                    return (
                        <tr key={key}>
                        <td> <Link to = {'/members/'+ val.id + '/'+ status}>{val.username}</Link></td>
                        <td>{val.age}</td>
                        <td>{val.Image_flag}</td>
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

export default ShowData;