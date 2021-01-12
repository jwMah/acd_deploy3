/*
* Class : Result 화면(detect 결과 화면)
* 
* state :
*  - response_data : axios api 요청 후 받은 response를 받아 저장
*
*
*
*/

import React from 'react';

class Result extends React.Component{
    constructor(props){
        super(props);
        this.state={
            response_data : this.props.location.state.response_data
        }
      }
    render(){
        return (
        <div className="result">
            <h2>Result</h2>
            <h4>{this.state.response_data.result}</h4>
        </div>
        );
    }
}


export default Result;