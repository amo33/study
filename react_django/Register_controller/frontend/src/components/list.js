import React, {Component} from "react";
import { render } from "react-dom";
import axios from 'axios';
import  Typography  from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import {Link} from "react-router-dom";
import Button from "@material-ui/core/Button";
const API = axios.create();
export default class List extends Component{
    constructor(props){
        super(props); // it's a rule 
        this.handleToseelist = this.handleToseelist.bind(this)
    };
    handleToseelist(val){
        $.ajax({
            url : "api/GotoList?category="+val,
            method : "get",
            datatype : "JSON",
            async : true,
            contentType : false,
            processData : false,
            success :  ( )=>{
                console.log(111)
            },
            error : ()=>{
                alert("error!");
            },
        });
    };
    handleToseeDB(val){
        $.ajax({
            url : "api/GotoList?category="+val,
            method : "get",
            datatype : "JSON",
            async : true,
            contentType : false,
            processData : false,
            success : async (filed)=>{
                console.log(filed);
            },
            error : ()=>{
                alert("error!");
            },
        });
    };
    render(){

        return (
            <Grid container spacing = {2}>
                <Grid item xs = {8} align= 'center'>
                    <Typography component = "h4" variant = "h4">
                        This is list to choose 
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
        );
    }
}