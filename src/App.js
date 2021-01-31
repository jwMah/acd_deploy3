import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css'; // For React-BootStrap default CSS ( 없으면 해당 strap 객체 렌더링 불가능 )
import { BrowserRouter, Route, Switch, withRouter } from "react-router-dom";
import pirate_white from './images/pirate_white.png';
import './App.css'
import Home from './components/Home'
import Detect from './components/Detect';
import Result from './components/Result';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar'
import IconButton from '@material-ui/core/IconButton'
import ArrowBackIosOutlinedIcon from '@material-ui/icons/ArrowBackIosOutlined';

class App extends React.Component{
  
  constructor(props) {
    super(props);
    this.state = {
       img_state : ""
    };
  }
  render(){
    return (
      <div className="app">
        <AppBar position="static" style={{ background: '#2E3B55', padding:'10px', alignItems:'center'}}>
        <Toolbar>
          {/*<IconButton edge="start" color="inherit" aria-label="menu">
            <ArrowBackIosOutlinedIcon onClick={() => this.props.history.goBack()}/>
          </IconButton>*/}
          <img height="50" alt="pirate_white.png" src={pirate_white}></img>
        </Toolbar>
        </AppBar>
        
        <div id="main_body">
        <BrowserRouter>
            <Switch>
                <Route exact path="/">
                  <Home></Home>
                </Route>
                <Route path='/detect' component={Detect}/>
                <Route path='/result' component={Result}/>
            </Switch>
          </BrowserRouter>
          </div>
      </div>
    );
  }
}

export default App;