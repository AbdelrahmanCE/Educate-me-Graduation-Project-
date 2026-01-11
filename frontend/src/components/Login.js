import React,{useState} from 'react';
import { useNavigate } from 'react-router-dom';

export default function Login(){
 const [u,setU]=useState('');
 const [p,setP]=useState('');
 const nav=useNavigate();
 async function submit(e){
  e.preventDefault();
  const r=await fetch('http://127.0.0.1:5000/api/auth/login',{
   method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({username:u,password:p})
  });
  const d=await r.json();
  if(r.ok){sessionStorage.setItem('token',d.access_token);nav('/dashboard');}
  else alert('Login failed');
 }
 return(
  <div className='container center'><div className='card'>
   <h2>Login</h2>
   <form onSubmit={submit}>
    <input className='input' placeholder='Username' onChange={e=>setU(e.target.value)}/>
    <input className='input' type='password' placeholder='Password' onChange={e=>setP(e.target.value)}/>
    <button className='button'>Login</button>
   </form>
   <div className='link' onClick={()=>nav('/signup')}>Create account</div>
  </div></div>
 );
}
