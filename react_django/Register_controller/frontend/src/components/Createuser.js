import React, { Component } from "react";
import Button from "@material-ui/core/Button";
import  Typography  from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import { Link } from "react-router-dom";
import { useSearchParams } from "react-router-dom";

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
        this.handleDetailUser = this.handleDetailUser.bind(this);
        this.UserInfoSent = this.UserInfoSent.bind(this);
        this.UserInfo = this.UserInfo.bind(this);
        this.UserRegistration = this.UserRegistration.bind(this);
        this.Showdetail = this.Showdetail.bind(this)
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

    handleDetailUser(props){
        console.log(this.state.sent);
        if(this.state.sent != ' '){
            this.UserInfoSent();
            $.ajax({
                url : "api/detail?user_id="+this.state.sent,
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

    UserInfoSent(){
        document.getElementById('register').style = "display:none";

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

    UserInfo(){
        //const issent = props.sent;
        const issent = this.props.sent;
        console.log(this.props.id);
        console.log(issent);
        console.log(1);
        if (issent == 1){
            console.log(1);
            return this.Showdetail();
        }
        return this.UserRegistration();
    }

    UserRegistration (){
        return (
            
            <div id = "Register">
                <Grid container spacing= {1}>
                    <Grid item xs ={12} align="center">
                        <Typography component="h4" variant="h4" style={{cursor:'default'}}>
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
                        <Button color= 'primary' variant="contained" onClick={this.handleregisterButtonPressed}>
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

    Showdetail(){
        return (
            <div id= "detail">
                <h1>Test</h1>
                <h4>{this.props.id}</h4>
            </div>
        );
    }

    render() {
        const temp = 1;
        if(this.props.sent == 1){
            this.Showdetail()
        }
        return(
            this.UserInfo()
        );
        
    }
        
    
}
