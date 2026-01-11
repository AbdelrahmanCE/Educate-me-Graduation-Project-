import React,{useState} from 'react';
import { useNavigate } from 'react-router-dom';

export default function Signup(){
 const [u,setU]=useState('');
 const [e,setE]=useState('');
 const [p,setP]=useState('');
 const nav=useNavigate();
 async function submit(ev){
  ev.preventDefault();
  const r=await fetch('http://127.0.0.1:5000/api/auth/signup',{
   method:'POST',headers:{'Content-Type':'application/json'},
   body:JSON.stringify({username:u,email:e,password:p})
  });
  const d=await r.json();
  if(r.ok){sessionStorage.setItem('token',d.access_token);nav('/dashboard');}
  else alert('Signup failed');
 }
 return(
  <div className='container center'><div className='card'>
   <h2>Sign Up</h2>
   <form onSubmit={submit}>
    <input className='input' placeholder='Username' onChange={ev=>setU(ev.target.value)}/>
    <input className='input' placeholder='Email' onChange={ev=>setE(ev.target.value)}/>
    <input className='input' type='password' placeholder='Password' onChange={ev=>setP(ev.target.value)}/>
    <button className='button'>Create Account</button>
   </form>
   <div className='link' onClick={()=>nav('/')}>Back to login</div>
  </div></div>
 );
}
