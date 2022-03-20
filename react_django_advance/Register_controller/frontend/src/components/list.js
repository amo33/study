import React, {useRef, useEffect, useMemo ,useState} from "react";
import  Typography  from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import {Link,useNavigate} from "react-router-dom";
import Button from "@material-ui/core/Button";

import ShowData from "./table.js";

const List=()=>{
    const [status, setstatus] = useState('default');
    const [data, setdata] = useState([]);
    
    const handledataupdate = (updata) =>{
        setdata([...updata]);
    }

    const onhandlestatus = (state)=>{
        setstatus(state);
    }
    
    const handleToseedata=(val)=>{
        
        $.ajax({
            url : "api/List?category="+val,
            method : "get",
            datatype : "JSON",
            async : true,
            contentType : false,
            processData : false,
            success : (datum)=>{
                document.getElementById('showdata').style = "display:block";
                document.getElementById('flag').innerHTML=val;
                document.getElementById('flag').style.cursor="default"; 
                document.getElementById('default').style = "display:none";
                document.getElementById('redirect').style = "display:block";
                handledataupdate(datum);
                onhandlestatus(val);
            },
            error : ()=>{
                alert("error!");
            },
        });
    };
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
                   <Button color= 'primary' variant="contained" value= {'showdb'} onClick={() => handleToseedata('showdb')}>
                       <Link to = '/list?category=showdb'>show me Database</Link>
                   </Button>
               </Grid>
               <Grid item xs={8} align="center">
                   
                   <Button color= 'secondary' variant="contained" value={'showlist'} onClick={() => handleToseedata('showlist')}>
                   <Link to = '/list?category=showlist'>show me list </Link>
                   </Button>
                   
               </Grid>
           </Grid>
           
           </div>
           <div id="showdata">
                <div id= "redirect">
                    <h2 id= 'flag'></h2>
               </div>
               <div id= "showingData"><ShowData userdata = {data} method = {status} /></div>
           </div>
           <div>
               <Button color = 'secondary' value={'showdefault'}>
               <Link to = '/'>Go to start page </Link>
               </Button>
               </div>
         </div>
        );
    
}

export default List