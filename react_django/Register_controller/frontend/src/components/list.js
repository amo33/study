import React, {Component} from "react";
import { render } from "react-dom";
import axios from 'axios';
import  Typography  from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import {Link} from "react-router-dom";
import Button from "@material-ui/core/Button";
import Createuser from "./Createuser";


async function showData(state ,data){
    const Json_data = JSON.parse(data);
    try{
        document.getElementById('showingData').remove();
        }catch(e){
        
        TypeError(e);
        }

    let g = document.createElement('div');
    g.setAttribute("id", "showingData");
    let table = document.createElement('table');
    g.appendChild(table);
    let thead = document.createElement('thead');
    let tbody = document.createElement('tbody');
    table.appendChild(thead);
    table.appendChild(tbody);
    let row_1 = document.createElement('tr');
    let heading_1 = document.createElement('th');
    heading_1.innerHTML = "Username";
    heading_1.style.textAlign = "center";
    let heading_2 = document.createElement('th');
    heading_2.innerHTML = "age";
    heading_2.style.textAlign = "center";
    let heading_3 = document.createElement('th');
    heading_3.innerHTML = "Image Flag";
    heading_3.setAttribute('style','text-align:center');
    row_1.appendChild(heading_1);
    row_1.appendChild(heading_2);
    row_1.appendChild(heading_3);
    thead.appendChild(row_1);
    let Scaled_username = '';
    for(let i=0; i<Json_data.length; i++){
        let row_2 = document.createElement('tr');
        let row_2_data_1 = document.createElement('td');
        let a = document.createElement('a');
        a.href = "/members?name="+Json_data[i].id+"&method="+state
        a.onclick = handleClickUser(Json_data[i].id);
        if(Json_data[i].username.includes('\t')){
            Scaled_username = Json_data[i].username.replace('/','');
        }
        else{
            Scaled_username = Json_data[i].username;
        }
        let innerText = document.createTextNode(Scaled_username);
        a.appendChild(innerText);
        row_2_data_1.appendChild(a);
        let row_2_data_2 = document.createElement('td');
        row_2_data_2.innerHTML = Json_data[i].age;
        let row_2_data_3 = document.createElement('td');
        row_2_data_3.innerHTML = Json_data[i].Image_flag;

        row_2.appendChild(row_2_data_1);
        row_2.appendChild(row_2_data_2);
        row_2.appendChild(row_2_data_3);
        tbody.appendChild(row_2);
    }
    
    function  handleClickUser(id){
   
        console.log(100);
        return(
            
            <Createuser id = {id} sent = {1} />
            
        )
    }
    
    document.getElementById('showdata').appendChild(g);
    document.getElementById('showingData').style.cursor = 'default';
    let div = document.createElement('div');
    let button = document.createElement('button');
    button.innerText = "Go back to list page";
    button.onclick = ()=>{
        // this.setState({status: 'default'})
        document.getElementById('showdata').style = "display:none";
        document.getElementById('default').style = "display:block";
        document.getElementById('redirect').style = "display:none";
    };
    document.getElementById('showingData').appendChild(button);
    
}

export default class List extends Component{
    
    constructor(props){
        super(props); // it's a rule 
        this.handleToseelist = this.handleToseelist.bind(this);
        this.handleToseeDefault = this.handleToseeDefault.bind(this);
        this.handleToseeDB = this.handleToseeDB.bind(this);
        this.state = {status : 'default', data: null};
    };

    handleToseelist(val){
        
        $.ajax({
            url : "api/List?category="+val,
            method : "get",
            datatype : "JSON",
            async : true,
            contentType : false,
            processData : false,
            success :  (text)=>{
                document.getElementById('showdata').style = "display:block";
                document.getElementById('flag').innerHTML="text"; 
                document.getElementById('showdata').style.cursor="pointer"; 
                document.getElementById('default').style = "display:none";
                document.getElementById('redirect').style = "display:block";
                this.setState({status: 'text', data:text});
                
                const Json_data = JSON.parse(text);
                showData(this.state.status, text);
                

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
            url : "api/List?category="+val,
            method : "get",
            datatype : "JSON",
            async : true,
            contentType : false,
            processData : false,
            success : async (db)=>{
                document.getElementById('showdata').style = "display:block";
                document.getElementById('flag').innerHTML="database";
                document.getElementById('flag').style.cursor="default"; 
                document.getElementById('default').style = "display:none";
                document.getElementById('redirect').style = "display:block";
                this.setState({status: 'db', data:db});
                showData(this.state.status,db);
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
                   <Typography component = "h4" variant = "h4" style={{cursor:'default'}}>
                       Choose between db and text 
                   </Typography>
               </Grid>
               <Grid item xs={8} align="center">
                   <Button color= 'primary' variant="contained" value= {'showdb'} onClick={() => this.handleToseeDB('showdb')}>
                       <Link to = '/list?category=showdb'>show me Database</Link>
                   </Button>
               </Grid>
               <Grid item xs={8} align="center">
                   
                   <Button color= 'secondary' variant="contained" value={'showlist'} onClick={() => this.handleToseelist('showlist')}>
                   <Link to = '/list?category=showlist'>show me list </Link>
                   </Button>
                   
               </Grid>
           </Grid>
           
           </div>
           <div id="showdata">
               <div id= "showingData"></div>
               <div id= "redirect">
                <h2 id= 'flag'></h2>
               </div>
               
           </div>

           <div>
               <Button color = 'secondary' value={'showdefault'}>
               <Link to = '/'>Go to start page </Link>
               </Button>
               </div>
         </div>
        );
    }
}