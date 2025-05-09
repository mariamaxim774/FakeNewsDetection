function Navbar()
{
    

    return(
    
      <>
      <nav className="navBar">
        <ul className="links">
        <li><a href="">Home</a></li>
        <li><a href="">Despre</a></li>
        <li><a href="">Documentatie</a></li>
        </ul>  
      </nav>

      <div className="dropdown"> 
        <button className="button">☰</button>      
        <div className="content">
          <a href="">Home</a>
          <a href="">Despre</a>
          <a href="">Documentatie</a>
        </div>  
      </div>
      
      </> 
    );
}

export default Navbar