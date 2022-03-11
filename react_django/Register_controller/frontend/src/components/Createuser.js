import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import  Typography  from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import render from "react-dom";
import TextField  from "@material-ui/core/TextField";
import  FormHelperText  from "@material-ui/core/FormHelperText";
import  FormControl  from "@material-ui/core/FormControl";
import { Link } from "react-router-dom";
import  Radio  from "@material-ui/core/Radio";
import  FormControlLabel  from "@material-ui/core/FormControlLabel";
import  RadioGroup  from "@material-ui/core/RadioGroup";
import { useState } from "react";

// 현재까지 4번 register 누름 , FormData를 ajax로 보낼 시 content type 과 process data가 false여야한다. 
//export const Usercreate = ((name, age, image) =>
//    API.post("/register",{
//        username: name,
//        age : age,
//       image : image 
//    }));
export default class Createuser extends Component{


    constructor(props){
        super(props);
        this.state = {
            name : "",
            age : 0,
            image : null,
        };

        this.handleregisterButtonPressed = this.handleregisterButtonPressed.bind(this);
        this.handleimageuploaded = this.handleimageuploaded.bind(this);
        this.handleUseragechange = this.handleUseragechange.bind(this);
        this.handleUsernametyped = this.handleUsernametyped.bind(this);
    }
    handleUsernametyped(e){
        this.setState({
            name : e.target.value,
        })
    }
    handleimageuploaded(e){

        this.setState({
            image : this.target.files[0],
        });
    }

    handleUseragechange(e){
        let num = e.target.value || 0;
        if(!isFinite(num)) return 
        num = num.toString()

        if (num !== '0' && !num.includes(',')){
            num = num.replace(/^0+/,'')
        }

        this.setState({
            age : e.target.value,
        })
    }
    handleregisterButtonPressed(){
        let datum = new FormData();
        datum.append("username", this.state.name);
        datum.append("age", this.state.age);
        datum.append("image", this.state.image);
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
    render() {
        return (
            <Grid container spacing= {1}>
                <Grid item xs ={12} align="center">
                    <Typography component="h4" variant="h4">
                        This is creating user page    
                    </Typography>    
                </Grid>
                <Grid item xs ={12} align="center">
                    <input type = "text" onChange={this.handleUsernametyped} value= {this.state.name} />
                </Grid>
                <Grid item xs ={12} align="center">
                                
                    <input type= "number" onChange= {this.handleUseragechange} value = {this.state.age} />
                          
                        
                </Grid>
                <Grid item xs={12} align="center">
                    <input type='file' 
                        accept='image/jpg,impge/png,image/jpeg,image/gif' 
                        name='profile_img' 
                        onChange={this.handleimageuploaded} > 
                    </input>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color= 'primary' variant="contained" to = "/GotoList" component={Link}>
                        Go to list for choosing source form 
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color= 'primary' variant="contained" onClick={this.handleregisterButtonPressed}>
                        Register user 
                    </Button>
                </Grid>
            </Grid>
        );
    }
        
    
}
