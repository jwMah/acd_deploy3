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
import { VictoryPie, VictoryTheme }from 'victory';

class Result extends React.Component{
    constructor(props){
        super(props);
        this.state={
            response_data : this.props.location.state.response_data
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

    render(){
        console.log(this.state.response_data.result); 
        console.log(this.state.response_data.result.over);
        console.log(this.state.response_data.result.under);
        return (
        <div className="result">
            <h2>Result</h2>
            <svg width="400" height="400" viewBox="0 0 400 400" >{this.make_PieChart()}</svg>
        </div>
        );
    }
}


export default Result;