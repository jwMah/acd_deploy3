import { render } from '@testing-library/react';
import {withRouter } from 'react-router-dom';
import { VictoryStack, VictoryBar, VictoryContainer } from 'victory';
import React from 'react';
import ReactPlayer from 'react-player'
import './css/result.css'
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button'
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import axios from 'axios';

class Result extends React.Component{
    constructor(props){
        super(props);
        this.state={
            response_data : this.props.location.state.response_data,
            response_img_list : this.props.location.state.response_img_list,
            changed_img_list : [],
            // For video Player state
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
        this.setState({duration})
    }
    handleSeekBtn = e => {
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

    //select 선택 value 바뀌는 이벤트 처리 함수 : 바뀐 데이터로 state 업데이트
    handle_select_change = (e, id) => {
        const img_censored = e.target.value;
        const img_id = id;
        document.getElementById(img_id).className=img_censored
        var _changed_img_list = this.state.changed_img_list.concat(
            {id : img_id,  censored : img_censored}
        )
        this.setState({
            changed_img_list : _changed_img_list
        });
    };

    //save button 이벤트 처리 함수 : 바뀐 데이터 실어서 보냄
    click_save = () => {
        console.log('click_save')
        console.log(this.state.changed_img_list)
        
        const api = axios.create({
            baseURL: 'http://localhost:5000'
        })
        var send_changed_censored = this.state.changed_img_list
        api.post('/update', send_changed_censored)
          .then(function (response) {
            console.log(response);
        }).catch(function (error) {
            console.log(error);
        });
        
    }
    
    make_image_list(){
        var img_lists = [];
        var data = this.state.response_img_list.img_dict;
        var i=0;
        while(i<Object.keys(data).length){
            const img_id = data[i].id
            img_lists.push(<div key={data[i].id} className='frame_prt_div'>
                <div id={img_id} className={data[i].ml_censored}>
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
                <Select
                labelId="demo-simple-select-helper-label"
                id="demo-simple-select-helper"
                onChange={ (e) => { this.handle_select_change(e, img_id); } }
                defaultValue={data[i].ml_censored}
                >
                    <MenuItem value='G'>G</MenuItem>
                    <MenuItem value='PG'>PG</MenuItem>
                    <MenuItem value='R'>R</MenuItem>
                </Select>
                </div>)
            i=i+1;
        }
        return(
            <div class="img_list">
                {img_lists}
            </div>
        );
    }

    make_hor_bar_chart() {
        
        let data = this.state.response_img_list.img_dict;
        
        let i=0;
        
        let censored_R = 0;
        let censored_PG = 0;
        let censored_G = 0;

        while(i<Object.keys(data).length){
            if(data[i].ml_censored==='R'){
                censored_R++;
            }
            else if(data[i].ml_censored==='PG'){
                censored_PG++;
            }
            else {
                censored_G++;
            }
            i=i+1;
        }
        return (
            <VictoryStack
            containerComponent={<VictoryContainer responsive={false}/>}
            width={300} height={100}
            colorScale={["tomato", "gold", "green"]}
            >
                <VictoryBar horizontal
                barWidth={({ index }) => index + 10}
                data={[ {x:"R", y: censored_R}]}
                />
                <VictoryBar horizontal
                barWidth={({ index }) => index + 10}
                data={[{x:"PG", y: censored_PG}]}
                />
                <VictoryBar horizontal
                barWidth={({ index }) => index + 10}
                data={[{x:"G", y: censored_G}]}
                />
                </VictoryStack>
        );
    }

    make_Result(){
        let data = this.state.response_img_list.img_dict;
        
        let i=0;
        
        let censored_R = 0;
        let censored_PG = 0;
        let censored_G = 0;
        const length_t = Object.keys(data).length;

        while(i<length_t){
            if(data[i].ml_censored==='R'){
                censored_R++;
            }
            else if(data[i].ml_censored==='PG'){
                censored_PG++;
            }
            else {
                censored_G++;
            }
            i=i+1;
        }

        const Res_R = censored_R / length_t * 100;
        const Res_PG = censored_PG / length_t * 100;
        const Res_G = censored_PG / length_t * 100;

        if(Res_R === 0.0 && Res_PG <= 20.0){
            return(
                <p>이 비디오는 전체이용가 입니다.</p>
            );
        } else if(Res_R <= 20.0) {
            return(
                <p>이 비디오는 15세 이용가 입니다.</p>
                );
        } else {
            return(
                <p>이 비디오는 19세 이용가 입니다.</p>
                );
        }
    }

    render(){
        return (
        <div className="result">
        <button name='redirect_btn' onClick={()=> this.props.history.push('/')}>Redirect!</button>
        <div align="center">{this.make_hor_bar_chart()}</div>
            <Grid container spacing={1} item align="center" justify="center">
                <Grid className='MuiGrid-align-items-xs-center' xs={12} sm={7}><div className='player-wrapper'>{this.make_Video()}</div></Grid>
                <Grid className='MuiGrid-align-items-xs-center' item justify="center" align="center" xs={12} sm={5}>
                {this.make_image_list()}
                <Grid
                container
                justify="center"
                align="center"
                >
                <Button boxShadow={3} id='save_button' variant="contained" onClick={this.click_save}><strong>SAVE</strong></Button>
                </Grid>
                </Grid>
            </Grid>
            <div>{this.make_Result()}</div>
            <div>
            <input
            type='range' min={0} max={0.999999} step='any'
            value={this.state.played}
            onChange={this.handleSeekChange}
            style={{display:'none'}}/>
            </div>
            
        </div>
        );
    }
}


export default withRouter(Result);