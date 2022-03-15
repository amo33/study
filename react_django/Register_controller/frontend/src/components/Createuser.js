import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import  Typography  from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import { Link } from "react-router-dom";
import { useSearchParams } from "react-router-dom";
import { useState } from "react";

function Createuser({userid}){
   
    const [name, setname] = useState('');
    const [age, setage] = useState(0);
    const [image, setimage] = useState(null);
   
    const handleUsernametyped = (e)=>{
       const name = e.target.value; 
       setname(name);
    }
    const handleimageuploaded = (e)=>{
        setimage(e.target.files[0])
    }

    const handleUseragechange=(e)=>{
        let num = e.target.value || 0;
        if(!isFinite(num)) return 
        num = num.toString()

        if (num !== '0' && !num.includes(',')){
            num = num.replace(/^0+/,'')
        }

        setage(num);
    }

    const handleDetailUser=()=>{
        
        if({id} != 0){
            this.UserInfoSent();
            $.ajax({
                url : "api/detail?user_id="+{id},
                method : "get",
                async : true,
                contentType : false,
                processData : false,
                success : (file)=>{
                    let received = file.image;
                    console.log(1);
                    console.log(file);
                    alert(file["username"]);
                    console.log(1);
                },
                error : ()=>{
                    alert("error!");
                },
            });
        }

    }

    const UserInfoSent= () =>{
        document.getElementById('register').style = "display:none";

    }

    const handleregisterButtonPressed=()=>{
        let datum = new FormData();
        console.log(name);
        console.log({age});
        datum.append("username", name);
        datum.append("age", age);
        datum.append("image", image);
        for (var key of datum.entries()) {
            console.log(key[0] + ', ' + key[1]);
        }
    
        $.ajax({
            url : "api/create-user",
            data : datum,
            method : "post",
            async : true,
            enctype : 'multipart/form-data',
            contentType : false,
            processData : false,
            success : (file)=>{
                let received = file[0]
                console.log(1);
                console.log(file);
                alert(file["username"]);
                console.log(1);
            },
            error : ()=>{
                alert("error!");
            },
        });
        
    }

    const UserInfo=()=>{
        //const issent = props.sent;
       
        console.log(1);
        if ({userid}== 1){
            console.log(1);
            return Showdetail();
        }
        return UserRegistration();
    }

    const UserRegistration=()=>{
        return (
            
            <div id = "Register">
                <Grid container spacing= {1}>
                    <Grid item xs ={12} align="center">
                        <Typography component="h4" variant="h4" style={{cursor:'default'}}>
                            This is creating user page    
                        </Typography>    
                    </Grid>
                    <Grid item xs ={12} align="center">
                        <input type = "text" onChange={handleUsernametyped} value= {name} />
                    </Grid>
                    <Grid item xs ={12} align="center">
                                    
                        <input type= "number" onChange= {handleUseragechange} value = {age} />
                            
                            
                    </Grid>
                    <Grid item xs={12} align="center">
                        <input type='file' 
                            accept='image/jpg,impge/png,image/jpeg,image/gif' 
                            name='profile_img' 
                            onChange={handleimageuploaded} > 
                        </input>
                    </Grid>
                    
                    <Grid item xs={12} align="center">
                        <Button color= 'primary' variant="contained" onClick={handleregisterButtonPressed}>
                            Register user 
                        </Button>
                    </Grid>
                    
                    <Grid item xs={12} align="center">
                        <Button color= 'primary' variant="contained" to = "/list" component={Link}>
                            Go to list for choosing source form 
                        </Button>
                    </Grid>
                </Grid>
            </div>
        );
    }

    const Showdetail=()=>{
        return (
            <div id= "detail">
                <h1>Test</h1>
                <h4>{id}</h4>
            </div>
        );
    }

    const temp = {userid};
    console.log(temp);
    if(temp == 0){
        return Showdetail()
    }
    return(
        UserInfo()
    );
        
    
        
    
}
export default Createuser