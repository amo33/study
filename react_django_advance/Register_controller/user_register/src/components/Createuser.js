import React, { useEffect } from "react";
import Button from "@material-ui/core/Button";
import  Typography  from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import { Link } from "react-router-dom";
import { useParams} from "react-router-dom";
import { useState } from "react";
import axios from "axios";
import ShowDetail from "./detail";

function Createuser(){
   
    const [name, setname] = useState('');
    const [age, setage] = useState(0);
    const [image, setimage] = useState(null);
    const [Incomedata, setIncomedata] = useState([])
    const {userid} = useParams();
    const {method} = useParams();
    const handleUsernametyped = (e)=>{ // name updated
        let regExp = /[ \{\}\[\]\/?.,;:|\)*~`!^\-_+┼<>@\#$%&\ '\"\\(\=]/gi;
        let name = e.target.value; 
        name = name.replace(regExp, "")
        if(name.length==0){
            alert('No name entered!');
            return UserRegistration();
        }
        else{
            setname(name);
        }
        
    }
    const handleimageuploaded = (e)=>{ // image updated
        setimage(e.target.files[0])
    }
    const IncomeFromBack = (val)=>{  // if detail user is required.. 
        setIncomedata([...val])
    }
    // 나이 마이너스 
    const handleUseragechange=(e)=>{ //age change
        let num = e.target.value || 0;
        if (num <0){
            num = 0;
        }
        if(!isFinite(num)) return 
        num = num.toString()

        if (num !== '0' && !num.includes(',')){
            num = num.replace(/^0+/,'')
        }

        setage(num);
    }

    useEffect(()=>{ // if userid changed . get data
        axios.get('http://127.0.0.1:3000/api/detail?user_id='+userid+'&method='+method)
                .then((Response)=>
                {   
                    IncomeFromBack(Response.data);
                })
                .catch((Error)=>{console.log(Error)})
                       
    },[userid]);

    const handleregisterButtonPressed=()=>{ // 사용자 등록
        let datum = new FormData();
        datum.append("username", name);
        datum.append("age", age);
        datum.append("image", image);

        axios.post("api/create-user", datum, {headers: { "Content-Type": "multipart/form-data"}})
        .then((response) => {alert(response.data['username'] + ' register success')})
        .catch((Error)=>{alert(Error)});
    }
    // 이름만 공백 . 
    const UserRegistration=()=>{ // 사용자 등록시 페이지

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

   return (
       userid !== undefined ? <div><ShowDetail userdata = {Incomedata} state = {userid} method= {method}/></div> : UserRegistration()
   );
}
export default Createuser