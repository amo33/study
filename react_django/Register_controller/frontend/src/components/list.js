import React, {Component} from "react";
import { render } from "react-dom";
import axios from 'axios';
import  Typography  from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import {Link} from "react-router-dom";
import Button from "@material-ui/core/Button";

function showData(state ,data){
    console.log(state);
    console.log()
    return (
        <div>
        <div>{{state}}</div>
        <div><pre>{JSON.stringify(data[0], null, 4)}</pre></div>
        </div>
    );
}

export default class List extends Component{
    constructor(props){
        super(props); // it's a rule 
        this.handleToseelist = this.handleToseelist.bind(this);
        this.handleToseeDefault = this.handleToseeDefault.bind(this);
        this.handleToseeDB = this.handleToseeDB.bind(this);
        this.state = {status : 'default'};
    };
    handleToseelist(val){
        $.ajax({
            url : "api/GotoList?category="+val,
            method : "get",
            datatype : "JSON",
            async : true,
            contentType : false,
            processData : false,
            success :  (text)=>{
                document.getElementById('showdata').style = "display:block";
                document.getElementById('flag').innerHTML="text"; 
                document.getElementById('flag').style.cursor="pointer"; 
                document.getElementById('default').style = "display:none";
                document.getElementById('redirect').style = "display:block";
                this.setState({status: 'text'})
                console.log(text);
                document.getElementById('showingData').innerHTML = showData(this.state.status,text);
            },
            error : ()=>{
                alert("error!");
            },
        });
    };
 
    
    handleToseeDefault(){
        this.setState({status: 'default'})
        document.getElementById('showdata').style = "display:none";
        document.getElementById('default').style = "display:block";
        document.getElementById('redirect').style = "display:none";
    }

    handleToseeDB(val){
        $.ajax({
            url : "api/GotoList?category="+val,
            method : "get",
            datatype : "JSON",
            async : true,
            contentType : false,
            processData : false,
            success : async (db)=>{
                document.getElementById('showdata').style = "display:block";
                document.getElementById('flag').innerHTML="database" ;
                document.getElementById('flag').style.cursor="text"; 
                document.getElementById('default').style = "display:none";
                document.getElementById('redirect').style = "display:block";
                console.log(db);
                this.setState({status: 'db'})
                document.getElementById('showingData').innerHTML = showData(this.state.status,db);
            },
            error : ()=>{
                alert("error!");
            },
        });
    };
    
    render(){
        
        return (
          <div>
           <div id= "default">
           <Grid container spacing = {2}>
               <Grid item xs = {8} align= 'center'>
                   <Typography component = "h4" variant = "h4" >
                       Choose between db and text 
                   </Typography>
               </Grid>
               <Grid item xs={8} align="center">
                   <Button color= 'primary' variant="contained" value= {'showdb'} onClick={() => this.handleToseeDB('showdb')}>
                       show me Database
                   </Button>
               </Grid>
               <Grid item xs={8} align="center">
                   <Button color= 'secondary' variant="contained" value={'showlist'} onClick={() => this.handleToseelist('showlist')}>
                       show me list
                   </Button>
               </Grid>
           </Grid>
           
           </div>
           <div id="showdata">
               <h1 id="flag"></h1>
               <div id= "showingData"></div>
               <div id= "redirect">
               <Button color = 'secondary' value={'showdefault'} onClick={()=> this.handleToseeDefault('showdefault')}>
                   show me the default page 
               </Button>
               </div>
               
           </div>
         </div>
        );
    }
}