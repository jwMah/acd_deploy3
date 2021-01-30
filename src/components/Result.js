import { render } from '@testing-library/react';
import React from 'react';
import ReactPlayer from 'react-player'
import { VictoryPie, VictoryTheme }from 'victory';
import './main.css'

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
        }
      }

    make_PieChart(){
        const _Over = this.state.response_data.result.over;
        const _Under = this.state.response_data.result.under;
        const My_data = [{x:'over', y:_Over}, {x:'under', y:_Under}];

        return <VictoryPie
        standalone={false} 
        width={400} height={400}
        colorScale={["red", "green"]}
        data={My_data}></VictoryPie>;
    }

    make_Video(){
        const { playing } = this.state
        const _Video_URL = this.state.response_data.result.video_URL;
        console.log(_Video_URL);

        return  <ReactPlayer 
        playing={playing}
        ref = {this.ref}
        controls
        url = {_Video_URL}
        className='react-player'
        width="800px"
        height="800px"/>;
    }

    /*
      // For Video Function //
      -> 
      ->
      ->

      */
     handleSeekBtn = e => {
        this.setState({ seeking: true })
        this.setState( {played: parseFloat(e.target.value) })
        this.setState({ playing: !this.state.playing })
        this.player.seekTo(parseFloat(e.target.value))
      }
      
      handleSeekChange = e => {
        this.setState({ played: parseFloat(e.target.value) })
      }
      
      
      ref = player => {
        this.player = player
      }
    
    make_image_list(){
        console.log(this.state.response_img_list)
        return <Image_list response_img_list={this.state.response_img_list}></Image_list>
    }

    render(){
        
        // Example of variable, 해당 구간을 의미하는 변수
        const time = 0.63910701
        
        return (
        <div className="result">
            <h2>Result</h2>
            <div className='player-wrapper' >{this.make_Video()}</div>
            {/*<svg width="200" height="200" viewBox="0 0 200 200" >{this.make_PieChart()}</svg>*/}
            
            <button 
            value={time}
            onClick={this.handleSeekBtn}></button>

            <div>
            <input
            type='range' min={0} max={0.999999} step='any'
            value={this.state.played}
            onChange={this.handleSeekChange} />
            </div>
            
            {this.make_image_list()}
            
        </div>
        );
    }
}

class Image_list extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            response_img_list : this.props.response_img_list
        }
    }
    render(){
        var img_lists = [];
        var data = this.state.response_img_list.img_dict;
        var i=0;
        console.log(typeof data)
        while(i<Object.keys(data).length){
            img_lists.push(<div>
                <img id={data[i]} src={data[i].location} alt='nope'></img>
                </div>)
            i=i+1;
        }
        return(
            <div className="img_list">
                {img_lists}
            </div>
        );
    }
}

export default Result;