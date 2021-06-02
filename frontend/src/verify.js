import React, {Component} from 'react';
import './css/main.css';
import './css/util.css';
import './verify.css';
import Sketch from "react-p5";
import {Monitor} from './monitor.js';
const axios = require('axios');

let video;

export class Verify extends Component {

	constructor(props){
		super(props);
		this.state = {
			verify : false,
			idenity: ' '
		};
	}

	setup(p5='', canvasParentRef='') {
        p5.noCanvas();
        video = p5.createCapture(p5.VIDEO);  
        const v = document.querySelector("video");
        let st = "position: absolute; margin-left: auto; margin-right: auto; left: 0; right: 0; text-align: center;"
        v.setAttribute("style", st);		
    }

    stop(){
		if(document.querySelector("video").srcObject != null){
			const tracks = document.querySelector("video").srcObject.getTracks();
		  	tracks.forEach(function(track) {
    				track.stop();
  			});
		}
    }

    logout(){
    	this.stop();
    	this.props.backhome();
    }

    signin(){
    	const button = document.getElementById('submit');
        button.addEventListener('click', async event => {
          video.loadPixels();
          console.log(video.canvas);
          const image64 = video.canvas.toDataURL();
          const data = { image64 };
          const options = {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          };
          const response = await axios.post('http://localhost:5000/verify', {'image64':image64});
          console.log(response.data.identity);
          if(response.data.identity){
          	this.stop();
			this.state.identity = []
	        this.setState({
	        	verify:true,
	        	idenity: this.state.identity.push(response.data.identity)
	        })
          } else {
          	this.stop();
          	alert("Not a registered user!")
          	this.props.backhome();
          }
        });
    }

	render(){

		let verify = (<div>
					<div className="limiter">
						<div className="container-login100">
							<div className="wrap-login100 p-l-110 p-r-110 p-t-62 p-b-33">
									
									<span className="login100-form-title p-b-53">
										Sign In
									</span>
									<br/><br/>
									<br/><br/>
									<br/><br/>
									<br/><br/>
									<br/><br/>
									<br/><br/>
									<br/><br/>
									<br/><br/>
									<br/><br/>
									<br/><br/>

									<Sketch setup={this.setup} draw={this.draw}/>
									
									 
									<div className="container-login100-form-btn m-t-17">
										<button id="submit" onMouseDown={this.signin.bind(this)} className="login100-form-btn">
											Sign In
										</button>
									</div>
									<div className="container-login100-form-btn m-t-17">
										<button onClick={this.logout.bind(this)} className="login100-form-btn">
											Back!
										</button>
									</div>
								
							</div>
						</div>
					</div>
				</div>
		)


    	return (<div >
    		{this.state.verify? <Monitor backhome={this.props.backhome} profilename={this.state.identity}/>: verify }
    		</div>
		)
	}
}
export default Verify;