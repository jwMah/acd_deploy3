import { render } from '@testing-library/react';
import {withRouter } from 'react-router-dom';
import React from 'react';
import ReactPlayer from 'react-player'
import './css/main.css'

class Result extends React.Component{
    constructor(props){
        super(props);
        this.state={
            response_data : this.props.location.state.response_data,
            response_img_list : this.props.location.state.response_img_list,
            // For video Player Values
            playing: true,
            seeking: true,
            played: 0,
            duration : 0
        }
      }

    make_Video(){
        const { playing } = this.state
        const _Video_URL = this.state.response_data.result.video_URL;
        //console.log(_Video_URL);

        return  <ReactPlayer 
        playing={playing}
        ref = {this.ref}
        controls
        url = {_Video_URL}
        className='react-player'
        width="800px"
        height="800px"
        onDuration={this.handleDutation}/>;
    }

    handleDutation = (duration) =>{
        console.log('onDuration',duration)
        this.setState({duration})
    }
    handleSeekBtn = e => {
        console.log(e.target)
        const img_time = Number(e.target.getAttribute('value'))/1000;
        const img_time_divided = img_time/this.state.duration
        console.log(img_time)

        this.setState({ seeking: true })
        this.setState( {played: parseFloat(img_time_divided) })
        this.setState({ playing: !this.state.playing })
        this.player.seekTo(parseFloat(img_time_divided))
    }
      
    handleSeekChange = e => {
        this.setState({ played: parseFloat(e.target.value) })
    }
      
      
    ref = player => {
        this.player = player
    }

    
    make_image_list(){
        var img_lists = [];
        var data = this.state.response_img_list.img_dict;
        var i=0;
        console.log(data)
        while(i<Object.keys(data).length){
            console.log(data[i].ml_censored)
            img_lists.push(<div key={data[i].id} className='frame_prt_div'>
                <div className='frame_chd_div' id={data[i].ml_censored}>
                <img
                className='frame_img'
                id={data[i].id}
                src={data[i].location}
                alt='nope'
                value={data[i].time_frame}
                censored = {data[i].ml_censored}
                onClick={this.handleSeekBtn}
                ></img>
                </div>
                <select id='selectBox'>
                    <option value="G" selected={data[i].ml_censored==="G"? true:false}>G</option>
                    <option value="PG" selected={data[i].ml_censored==="PG"? true:false}>PG</option>
                    <option value="R" selected={data[i].ml_censored==="R"? true:false}>R</option>
                </select>
                </div>)
            i=i+1;
        }
        return(
            <div className="img_list">
                {img_lists}
            </div>
        );
    }

    render(){
        return (
        <div className="result">
            <h2>Result</h2>
            <div className='player-wrapper' >{this.make_Video()}</div>
            {/*<svg width="200" height="200" viewBox="0 0 200 200" >{this.make_PieChart()}</svg>*/}
            
            <div>
            <input
            type='range' min={0} max={0.999999} step='any'
            value={this.state.played}
            onChange={this.handleSeekChange}
            style={{display:'none'}}/>
            </div>
            
            {this.make_image_list()}
            
        </div>
        );
    }
}


export default withRouter(Result);