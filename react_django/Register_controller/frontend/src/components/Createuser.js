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

export default class Createuser extends Component{
    defaultvotes = 2

    constructor(props){
        super(props);
    }

    render() {
        return (
            <Grid container spacing= {1}>
                <Grid item xs ={12} align='center'>
                    <Typography component="h4" variant="h4">
                        This is creating user page    
                    </Typography>    
                </Grid>
                <Grid item xs ={12} align='center'>
                    <FormControl>
                    <TextField 
                        required={true} 
                        type= "number"
                        defaultValue={this.defaultvotes}
                        inputprops={{
                            min:1,
                            style: {textAlign : 'center'},
                        }}
                        />
                      <FormHelperText>
                        <div align="center">Age required to register user</div>
                      </FormHelperText>   
                    </FormControl> 
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color= 'primary' variant="contained">
                        submit user(Register)
                    </Button>
                </Grid>
                <Grid item xs={12} align="center">
                    <Button color= 'secondary' variant="contained" to="/" component={Link}>
                        Go back to home
                    </Button>
                </Grid>
            </Grid>
        );
    }
        
    
}
