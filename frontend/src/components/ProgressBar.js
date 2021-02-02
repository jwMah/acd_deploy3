import LinearProgress from '@material-ui/core/LinearProgress';
import { render } from '@testing-library/react';
import React from 'react';

class ProgressBar extends React.Component{
    constructor(props){
        super(props);
        this.state={
            response_status_num : this.props.response_status_num
        }
    }

    render(){
        return (
        <div className='progress_bar'>
            <LinearProgress variant="determinate" value={this.state.response_status_num} />
          </div>
        );
    }
}

export default ProgressBar;