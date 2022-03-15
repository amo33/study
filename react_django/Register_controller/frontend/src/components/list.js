import React, {useRef, useEffect, useMemo ,useState} from "react";
import {Redirect} from "react-router-dom";
import  Typography  from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import {Link,useNavigate} from "react-router-dom";
import Button from "@material-ui/core/Button";
import {useTable} from "react-table";
import { TableHead } from "@material-ui/core";
import ReactDOM from 'react-dom'; 
const List=({setid})=>{
    
    const [status, setstatus] = useState('default');
    const [data, setdata] = useState([]);
    
    const columndata = 
         [
         {
             accessor: "name",
             Header: "Name",
         },
         {
             accessor:'age',
             Header:"Age",
         },
         {
             accessor:'image_flag',
             Header: 'Image_flag',
         },
        ];     
    const columns = useMemo(() => columndata, []);
    const userdata = useMemo(()=>{data} , []);
    
    useEffect(()=>{
        //showData(columns, userdata);
        
    },[data, status]);

    const handleToseeDefault=()=>{
        setstatus('default');
        document.getElementById('showdata').style = "display:none";
        document.getElementById('default').style = "display:block";
        document.getElementById('redirect').style = "display:none";
        
    }
    const handledataupdate = (updata) =>{
        {(updata) && updata.map(x => setdata(data => [...data, x]))}
        //setdata({...data, updata});
    }

    const onhandlestatus = (state)=>{
        setstatus({...status,state});
        console.log(state);
       
    }
    function ShowData(props){
        return (
            <table>
                <thead>
                    <tr>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Image_Flag</th>
                    </tr>
                </thead>
                <tbody>
                
                    {props.userdata.map((val, key) => {
                    return (
                        <tr key={key}>
                        <td>{val.username}</td>
                        <td>{val.age}</td>
                        <td>{val.Image_flag}</td>
                        </tr>
                
          )
        })}
        </tbody>
      </table>

        )
    }
    /*
    const showData=(columndata,datum)=>{
        const testData = useMemo(()=> datum, []);
        const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
        useTable( {columndata, data : testData});
    
        //let Json_data = JSON.parse(data);
        let Json_data = datum;
        try{
            document.getElementById('showingData').remove();
            }catch(e){
            
            TypeError(e);
            }
        console.log(Json_data[1].id);
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
            let name_click = document.createElement('h3');
          //  a.href = "/members?name="+Json_data[i].id+"&method="+status
            name_click.onclick = async() =>{handleClickUser(Json_data[i].id);}
            console.log(Json_data[i].username);
            if(Json_data[i].username.includes('\t')){
                Scaled_username = Json_data[i].username.replace('/','');
            }
            else{
                Scaled_username = Json_data[i].username;
            }
            name_click.innerHTML = Scaled_username;
            row_2_data_1.appendChild(name_click);
            let row_2_data_2 = document.createElement('td');
            row_2_data_2.innerHTML = Json_data[i].age;
            let row_2_data_3 = document.createElement('td');
            row_2_data_3.innerHTML = Json_data[i].Image_flag;
    
            row_2.appendChild(row_2_data_1);
            row_2.appendChild(row_2_data_2);
            row_2.appendChild(row_2_data_3);
            tbody.appendChild(row_2);
        }
        
        document.getElementById('showdata').appendChild(g);
        document.getElementById('showingData').style.cursor = 'default';
    */
    /*  
        return (
            <table {...getTableProps()}>
                <thead>
                    {headerGroups.map(header=>(
                         <tr {...header.getHeaderGroupProps()}>
                         {header.headers.map((column)=>(
                             <Th {...column.getHeaderProps()}>{column.render('Header')}</Th>
                         ))}
                     </tr>
                    ))}
                </thead>
                <tbody {...getTableBodyProps()}>
                    {rows.map(user=>{
                        prepareRow(user)
                        return(
                        <tr {...row.getRowProps()}>
                        {row.cells.map(cell => {
                          // getCellProps는 각 cell data를 호출해낸다
                           return <Td {...cell.getCellProps()}>{cell.render('Cell')}</Td>
                        })}
                        </tr>
                        );
                    })}
                </tbody>
            </table>
        );
        */
       /*
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
     */ 
    const handleToseedata=(val)=>{
        
        $.ajax({
            url : "api/List?category="+val,
            method : "get",
            datatype : "JSON",
            async : true,
            contentType : false,
            processData : false,
            success : async (datum)=>{
                document.getElementById('showdata').style = "display:block";
                document.getElementById('flag').innerHTML=val;
                document.getElementById('flag').style.cursor="default"; 
                document.getElementById('default').style = "display:none";
                document.getElementById('redirect').style = "display:block";
                handledataupdate(datum);
                console.log(1);
                onhandlestatus(val);

                console.log({data});
                const element = <ShowData userdata = {datum} />;
                ReactDOM.render(
                    element,
                    document.getElementById('showingData')
                  );
                console.log(data);
            },
            error : ()=>{
                alert("error!");
            },
        });
    };

    const handleClickUser=(id)=>{   
       const navigate = useNavigate();

       console.log({status});
       console.log(data);
       setid(id);
       navigate("members?name"+id+"?method="+{status}, {state : {id:id}});
    }
    
   
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
               <div id= "showingData"></div>
               
               
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