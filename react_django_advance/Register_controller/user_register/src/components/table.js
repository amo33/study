import React, { Component} from "react";
import {Link} from "react-router-dom";
import Button from "@material-ui/core/Button";
function ShowData(props){
    const status = props.method;
    console.log(props.userdata[0].image_path);
    console.log(props.userdata[0].Image_flag);
    if(props.method != 'default'){
        return (
            <div>
                <h4>{props.method}</h4>
            <table>
                <thead>
                    <tr>
                    <th>Name</th>
                    <th>Age</th>
                    {(props.userdata[0].image_path !== ' ' || props.userdata[0].image_path) === undefined && <th>user_id</th>}
                    {(props.userdata[0].image_path === ' ' || props.userdata[0].image_path === undefined )&& <th>Image_Flag</th>}
                    {(props.userdata[0].image_path !== ' ' || props.userdata[0].image_path) === undefined && <th>Image path</th>}
                    </tr>
                </thead>
                <tbody>

                    {props.userdata.map((val, key) => {
                    return (
                        <tr key={key}>
                        {(props.userdata[0].image_path === ' ' || props.userdata[0].image_path === undefined) && <td> <Link to = {'/members/'+ val.id + '/'+ status}>{val.username}</Link></td>}
                        {(props.userdata[0].image_path !== ' '|| props.userdata[0].image_path === undefined) && <td>{val.username}</td>}
                        <td>{val.age}</td>
                        {(props.userdata[0].image_path !== ' '|| props.userdata[0].image_path !== undefined)  && <td>{val.user_id}</td>}
                        {(props.userdata[0].image_path === ' '|| props.userdata[0].image_path === undefined) && <td>{val.Image_flag}</td>}
                        {(props.userdata[0].image_path !== ' ' || props.userdata[0].image_path !== undefined) && <td><img src= {process.env.PUBLIC_URL+val.image_path} alt="No Image Registered"/></td>}
                        
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