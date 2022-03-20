import React, { Component} from "react";
import {Link} from "react-router-dom";
import Button from "@material-ui/core/Button";
function ShowData(props){
    const status = props.method;
   
    if(props.method != 'default'){
        return (
            <div>
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
            
            )}
            )}
                </tbody>
             </table>
             <div>
               <Button color = 'secondary' value={'showdefault'}>
               <Link to = '/'>Go to start page </Link>
               </Button>
            </div>
    </div>
        );
    
    }
}

export default ShowData;