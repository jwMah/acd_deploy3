import React from 'react';
import { Redirect, withRouter  } from 'react-router-dom';
import Spinner from 'react-bootstrap/Spinner';
import axios from 'axios';
import ProgressBar from './ProgressBar.js';


const api = axios.create({
    baseURL: 'http://localhost:5000'
})

class Detect extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            page_change_flag : 0,           //button -> result
            btn_clicked_flag : 0,           //detectClick && -> flag = 1 
            response_data : "",              //back -> response -> result.js
            response_img_list : [],
            response_status : "",
            response_status_num : 0
        };
    }

    //file 업로드 - 미리보기 함수
    //url upload 시, 처리 필요
    previewImg(e) {
        var reader = new FileReader();
        
        reader.onload = function(e) {
            var img = document.createElement("img");
            img.setAttribute("src", e.target.result);
            img.setAttribute("width", "200");
            img.setAttribute("height", "200");
            document.querySelector("div#preview_div").appendChild(img);
        };
        reader.readAsDataURL(e.target.files[0]);
    }

    detectClick(e) {
        e.preventDefault();
        var photoFile = document.getElementById("input_img");
        var url_input = document.getElementById("img_url").value;
        var flag = 0;
        const detect_click_this = this;
        detect_click_this.setState({
            response_status_num : 10
        })
        if(photoFile.files[0]!==undefined) {
            this.setState({btn_clicked_flag: 1});  // set btn_flag = 1
            flag = this.file_api_call(photoFile);
        }
        else if(url_input !== ''){
            this.setState({btn_clicked_flag: 1});  // set btn_flag = 1
            flag = this.url_api_call(url_input);
        } else {
            // photoFile and url_input both are all empty -> pass
        }

        // Input 입력값을 모두 초기화!
        photoFile.files = null;
        document.getElementById("img_url").value = null;

        
    }

    //file 처리
    file_api_call(photoFile){
        var home_this = this;
        var formData = new FormData();
        formData.append("file", photoFile.files[0]);
        formData.append("image_type", "1");

        api.post('/videoUploading', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(function (response) {
            console.log(response);
            const status_sentence = response.data.video_filename+"is uploaded"
            home_this.setState({
                response_status : status_sentence,
                response_status_num : 40
            })
            return home_this.frame_uploading();
        }).catch(function (error) {
            console.log(error);
        });
    }

    url_api_call(url_input){
        const api = axios.create({
            baseURL: 'http://localhost:5000'
        })
        var home_this = this;
        var formData = new FormData();
        formData.append("image_url", url_input);
        formData.append("image_type", "0");
        
        api.post('/videoUploading', formData)
          .then(function (response) {
            console.log(response);
            const status_sentence = response.data.video_filename+"is uploaded"
            home_this.setState({
                response_status : status_sentence,
                response_status_num : 40
            })
            return home_this.frame_uploading();
            //보류 home_this.make_img_list()
            //보류 return 1;
        }).catch(function (error) {
            console.log(error);
          });
    }

    frame_uploading(){
        const api = axios.create({
            baseURL: 'http://localhost:5000'
        })
        var home_this = this;
        api.post('/frameUploading')
          .then(function (response) {
            console.log(response);
            const status_sentence = home_this.state.response_status + <br></br> +response.data.result.frame_counts + " frames are extracted from " + response.data.result.video_filename;
            home_this.setState({
                response_status : status_sentence,
                response_status_num : 60
            })
            return setTimeout(function() {
                home_this.final_detect();
                return 1;
            }, 5000);
        }).catch(function (error) {
            console.log(error);
          });
    }

    //request detecting
    final_detect(){
        const api = axios.create({
            baseURL: 'http://localhost:5000'
        })
        var home_this = this;
        api.post('/detectFinal')
          .then(function (response) {
            console.log(response);
            const status_sentence = home_this.state.response_status + <br></br> + "detecting...."
            home_this.setState({
                response_status : status_sentence,
                response_data:response.data,
                response_status_num : 90
            })
            return setTimeout(function() {
                home_this.make_img_list();
                return 1;
            }, 5000);
        }).catch(function (error) {
            console.log(error);
        });
    }

    make_img_list(){
        var detect_this = this;

        const api = axios.create({
            baseURL: 'http://localhost:5000'
        })
        
        api.post('/frame')
        .then(function (response) {
            console.log(response.data);
            detect_this.setState({
                page_change_flag:1,
                response_img_list:response.data,
                response_status_num : 100
            })
        }).catch(function (error) {
            console.log(error);
        });
    }

    render(){
        // When loading is complete, go to "Result.js"
        let button;
        if(this.state.page_change_flag===1) {
            return <Redirect to={{
                pathname: '/result',
                state : {
                    response_data : this.state.response_data,
                    response_img_list : this.state.response_img_list
                }
            }}></Redirect>
        }

        // conditional rendering for Loading 
        if(this.state.btn_clicked_flag===0) {
            // not occured click event, set button normally
            button = <input type="submit" value="UPLOAD"></input>;
        } else {
            // when clikc event occur, set button to React-bootstrap Loading Spinner
            button = <Spinner animation="border" role="status"><span className="sr-only">Loading...</span></Spinner>; 
        }
        
        return (
        <div className="body_main">
            <form id="img_input_form" runat="server" action="" method="post" onSubmit={this.detectClick.bind(this)}>
            
            <div id="preview_div"></div>

            <div className="form_div">
                <input type="file" name="input_img" id="input_img" onChange={this.previewImg.bind(this)}></input>
                <br></br>
                <input type="textarea" name = "input_url" id="img_url"></input>
                {button}
            </div>
            <br></br>
            <button name='redirect_btn' onClick={()=> this.props.history.push('/')}>Redirect!</button>
            <br></br>
            <h2>{this.state.response_status}</h2>
            <ProgressBar response_status_num={this.state.response_status_num}></ProgressBar>
            </form>
        </div> 
        );
    }
}

// onChange 세분화, click event 처리 시, 해당 tag의 value도 모두 초기화 할 수 있도록 추가 구현.

export default withRouter(Detect);