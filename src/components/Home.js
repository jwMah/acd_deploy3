import { render } from '@testing-library/react';
import React from 'react';
import { Link , withRouter } from 'react-router-dom';
import './css/home.css'
import Button from '@material-ui/core/Button'
import { shadows } from '@material-ui/system';
import { makeStyles } from '@material-ui/core/styles';

const useStyles = makeStyles((theme) => ({
    root: {
      '& > *': {
        margin: theme.spacing(1),
      },
    },
  }));

class Home extends React.Component{
    constructor(props){
        super(props);
        this.state={
        }
    }

    render(){
        return (
        <div className="home">
            <h1>Adult Contents Detector</h1>
            <p>
            'Adult Contents Detector' is a Web Application that can detect harmful contents that contains exposure.<br></br>
            <br></br>
            The CNN AI model determines the exposure level for video in the form of local files or URLs that you enter. When the discrimination is complete, the results are visually displayed, and the user can change the detection result.<br></br>
            In addition, the application allows you to view all detected frames a quantitative manner.<br></br>
            </p>
            <Button boxShadow={3} id='start_button' variant="contained" component={Link} to={'/detect'}>START</Button>
        </div>
        );
    }
}

export default withRouter(Home);