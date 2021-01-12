import React from 'react';
import { Redirect  } from 'react-router-dom';
import axios from 'axios';

class Home extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            page_change_flag : 0,           //button -> result 
            response_data : ""              //back -> response -> result.js
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
       
        if(photoFile.files[0]!==undefined) {
            this.file_api_call(photoFile)
        }
        else{
            this.url_api_call(url_input)
        }
    }

    //file 처리
    file_api_call(photoFile){
        const api = axios.create({
            baseURL: 'http://localhost:5000'
        })
        var home_this = this;
        var formData = new FormData();
        formData.append("file", photoFile.files[0]);

        api.post('/detect', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(function (response) {
            console.log(response);
            home_this.setState({
                page_change_flag:1,
                response_data:response.data
            })
        }).catch(function (error) {
            console.log(error);
        });
    }


    url_api_call(url_input){
        console.log("url_api_call")
        console.log("수정 필요")
        console.log(url_input)
        
        const api = axios.create({
            baseURL: 'http://localhost:5000'
        })
        
        api.post('/detect', {
            image_url : url_input
          })
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });
    }
    render(){
        if(this.state.page_change_flag===1) {
            return <Redirect to={{
                pathname: '/result',
                state : {
                    response_data : this.state.response_data
                }
            }}></Redirect>
        }
        return (
        <div className="body_main">
            <form id="img_input_form" runat="server" action="" method="post" onSubmit={this.detectClick.bind(this)}>
            
            <div id="preview_div"></div>

            <div className="form_div">
                <input type="file" name="input_img" id="input_img" onChange={this.previewImg.bind(this)}></input>
                <br></br>
                <input type="textarea" name = "input_url" id="img_url"></input>
                <input type="submit" value="UPLOAD"></input>
            </div>

            </form>
        </div>
        );
    }
}

export default Home;