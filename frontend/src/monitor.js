import React, {Component} from 'react';
import { Comment, Header } from 'semantic-ui-react';
import ElizaBot from 'elizabot';
import debounce from 'lodash.debounce';
import './css/main.css';
import './css/util.css';
import './css/semantic.css';
import './monitor.css';

import ChatHistory from './ChatHistory'
import ChatInput from './ChatInput'

export class Monitor extends Component {
	constructor(props) {
	  super(props);
	  this.profilepicture = [];
	  this.eliza = new ElizaBot();
	  this.state = {
	  messages: [{
        user: false,
		name: this.props.profilename,
        text: this.fixup(this.eliza.getInitial()),
        date: new Date(),
      }],
		awsApiData : [],
		imageStatus: "loading...",
		profileStatus: "loading..."
	  };
	this.debounced_reply = debounce(this.reply, 1000, { 'maxWait': 5000 });
	}
	
	handleInput = (input) => {
		input = input.trim();
		if (!input)
			return;
		const messages = this.state.messages.slice(0);
		messages.push({
			user: true,
			text: input,
			date: new Date(),
		});
		this.setState({
			messages,
		});
    this.debounced_reply();
	}
	
	reply = () => {
    const unreplied = [];
    const messages = this.state.messages.slice(0);
    let iter = messages.length - 1;
    while (messages[iter].user && iter >= 0) {
      unreplied.unshift(messages[iter].text);
      iter--;
    }
    if (unreplied.length === 0)
      return;
    let response = this.eliza.transform(unreplied.join(' '));
    messages.push({
      user: false,
      text: this.fixup(response),
      date: new Date(),
    });
    this.setState({
      messages,
    });
  }
  
    fixup(text) {
    // Hack fix for weird "?" spacing in elizabot
    return text.replace(/ \?/g, '?');
	}

	handleImageLoaded() {
		this.setState({ imageStatus: "" });
	 }
	
	handleImageErrored() {
		this.setState({ imageStatus: "failed to load" });
	 }
	 
	 handleProfileLoaded() {
		this.setState({ profileStatus: "" });
	 }
	
	handleProfileErrored() {
		this.setState({ profileStatus: "" });
	 }
	 
	logout(){
    	this.props.backhome();
    }
	
	componentDidMount() {
		console.log("componentDidMount")
          fetch('/profilepicture?profilename='+this.props.profilename+'')
			.then(response => response.blob())
			.then(image => {
				this.profilepicture = URL.createObjectURL(image)
				console.log(this.profilepicture)
			})
      }
	
  
	render() {
		return (
		<div class="row">
		<div class="col-sm-2">
            <div class="card">
                <div class="card-body">
                  <div class="d-flex flex-column align-items-center text-center">
                    <img src={this.profilepicture} alt="profileimage"  class="rounded-circle" width="150" onLoad={this.handleProfileLoaded.bind(this)} onError={this.handleProfileErrored.bind(this)}/>
					{this.state.profileStatus}
                    <div class="mt-3">
                      <h4>{this.props.profilename}</h4>
                    </div>
                  </div>
                </div>
			</div>
        </div>
		<div class="col-sm-2">
        <Header as='h3' block>
          Chat with our Chatbuddy
        </Header>
        <Comment.Group>
          <ChatHistory messages={this.state.messages} />
          <ChatInput inputHandler={this.handleInput} />
        </Comment.Group>
	  </div>
	  <div class="col-sm-8 pull-right">
			<img src={'/video_feed'} className="video_emotion_detection" alt="video" onLoad={this.handleImageLoaded.bind(this)} onError={this.handleImageErrored.bind(this)}/>
			{this.state.imageStatus}
   	  </div>
	 <div class="col-sm-2">
	 <button onClick={this.logout.bind(this)} className="login100-form-btn">
				Back Home!
		</button>	
	</div>	
	  </div>
		);
	}
  }
export default Monitor;