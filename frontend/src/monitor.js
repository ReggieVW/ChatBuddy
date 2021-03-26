import React, {Component} from 'react';
import './App.css';

export class Monitor extends Component {
	constructor(props) {
	  super(props);
	  this.state = {
		items: [],
		isLoaded: false,
		test: 'reggie',
		imageStatus: "loading"
	  };
	  
	}

	handleImageLoaded() {
		this.setState({ imageStatus: "loaded" });
	  }
	
	  handleImageErrored() {
		this.setState({ imageStatus: "failed to load" });
	  }
  
	componentDidMount() {
	  fetch('/test')
		.then(res => res.json())
		.then(result => {
			console.log(result)
		  this.setState({
			isLoaded: true,
			items: result,
			test: result.name
		  });
		  this.state.test=result
		  console.log(this.state.test)
		});
	}
  
	render() {
	  const { items } = this.state.items;
	  if (!this.state.isLoaded) {
		return <div>Loading ... </div>;
	  } else {
		return (
			<div>
					<img src={'/video_feed'} className="App-logo" alt="logo" onLoad={this.handleImageLoaded.bind(this)} onError={this.handleImageErrored.bind(this)} />
					{this.state.imageStatus}
   			</div>
		);
	  }
	}
  }
export default Monitor;