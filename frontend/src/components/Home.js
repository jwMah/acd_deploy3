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
            - the MPAA-based 'R' class is "Restricted". only adults can watch it. It contains adult materials.<br></br>
            - the MPAA-based 'PG' class contains some materials that may not be suitable for children.<br></br>
            - the MPAA-based 'G' class is "G-RATED MOVIE". All ages acknowledged.<br></br>
            <br></br>
            When the discrimination is complete, the results are visually displayed, and the user can change the detection result.<br></br>
            In addition, you can make a direct correction if the result of the discrimination against the frame is ambiguous.<br></br>
            </p>
            <Button boxShadow={3} id='start_button' variant="contained" component={Link} to={'/detect'}>START</Button>
        </div>
        );
    }
}

export default withRouter(Home);