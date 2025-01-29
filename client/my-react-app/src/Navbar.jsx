import React from 'react';

function Navbar(){
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light"> 
        <div className="container-fluid"> 
            <ul>
                <li style={{color: 'black' }}><a href="#">Home</a></li>
                <li><a href="#">About</a></li>
                <li><a href="#">Contact</a></li>

            </ul>
        </div>
        
        </nav>
        
    )

}
