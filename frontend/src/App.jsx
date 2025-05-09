
  import 'bootstrap/dist/css/bootstrap.min.css';
  import 'bootstrap/dist/js/bootstrap.bundle.min.js';

  import Header from "./Header"
  import "./index.css"
  import "./theme.css"
  import Footer from "./Footer"
  import Navbar from "./Navbar"
  import Form from "./Form"
  import Answer from "./Answer"
  import React, { useState, useEffect } from "react";

  function App() {


    return (
      <> 
      <Header/> 
      <Navbar/>
      <main>
      <Form/>
      
      </main>  
      <Footer/> 
      
      </>
    )
  }

  export default App
