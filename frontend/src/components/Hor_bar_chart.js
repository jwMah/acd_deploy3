import { render } from '@testing-library/react';
import React from 'react';
import { VictoryStack, VictoryBar, VictoryContainer } from 'victory';


class Hor_bar_chart extends React.Component{
    constructor(props){
        super(props);
        this.state={
            Res_G : this.props.Res_G,
            Res_PG : this.props.Res_PG,
            Res_R : this.props.Res_R
        }
    }

    render(){
        return (
        <VictoryStack
            containerComponent={<VictoryContainer responsive={false}/>}
            width={300} height={100}
            colorScale={["green", "gold", "tomato"]}
            >
            <VictoryBar horizontal
                barWidth={({ index }) => index + 10}
                data={[{x:"G", y: this.state.Res_G}]}
            />
            <VictoryBar horizontal
                barWidth={({ index }) => index + 10}
                data={[{x:"PG", y: this.state.Res_PG}]}
            />
            <VictoryBar horizontal
                barWidth={({ index }) => index + 10}
                data={[ {x:"R", y: this.state.Res_R}]}
            />
        </VictoryStack>
        );
    }
}

export default Hor_bar_chart;