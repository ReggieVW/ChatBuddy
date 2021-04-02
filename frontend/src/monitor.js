import React, {Component} from 'react';
import './App.css';

export class Monitor extends Component {
	constructor(props) {
	  super(props);
	  this.state = {
		items: [],
		imageStatus: "loading"
	  };
	}

	handleImageLoaded() {
		this.setState({ imageStatus: "loaded" });
	  }
	
	  handleImageErrored() {
		this.setState({ imageStatus: "failed to load" });
	  }
  
	render() {
		return (
			<div>
					<img src={'/video_feed'} className="App-logo" alt="logo" onLoad={this.handleImageLoaded.bind(this)} onError={this.handleImageErrored.bind(this)} />
					{this.state.imageStatus}
   			</div>
		);
	}
  }
export default Monitor;