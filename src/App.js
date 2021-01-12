import React from 'react';
import { BrowserRouter, Route, Switch } from "react-router-dom";
import './App.css'
import Home from './components/Home';
import Result from './components/Result';

class App extends React.Component{
  constructor(props) {
    super(props);
    this.state = {
       img_state : ""
    };
  }
  
  render(){
    console.log("App render");
    return (
      <div className="app">
        <h2> Adult Contents Detector</h2>
        <hr></hr>
        <BrowserRouter>
            <Switch>
                <Route exact path="/">
                  <Home></Home>
                </Route>

                <Route path='/result' component={Result}/>
            </Switch>
          </BrowserRouter>
      </div>
    );
  }
}

export default App;