import React, {Component} from 'react';
import { Comment, Header } from 'semantic-ui-react';
import ElizaBot from 'elizabot';
import debounce from 'lodash.debounce';
import './css/main.css';
import './css/util.css';
import './css/semantic.css';

import ChatHistory from './ChatHistory'
import ChatInput from './ChatInput'

export class Monitor extends Component {
	constructor(props) {
	  super(props);
	  this.eliza = new ElizaBot();
	  this.state = {
	  messages: [{
        user: false,
        text: this.fixup(this.eliza.getInitial()),
        date: new Date(),
      }],
		imageStatus: "loading"
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
	 
	logout(){
    	this.props.backhome();
    }
  
	render() {
		return (
		<div class="row">
		<div class="col-sm-4">
        <Header as='h3' block>
          Chat with our Chatbuddy
        </Header>
        <Comment.Group>
          <ChatHistory messages={this.state.messages} />
          <ChatInput inputHandler={this.handleInput} />
        </Comment.Group>
	  </div>
	  <div class="col-sm-6">
			<img src={'/video_feed'} className="video" alt="video" onLoad={this.handleImageLoaded.bind(this)} onError={this.handleImageErrored.bind(this)}/>
			{this.state.imageStatus}
   	  </div>
	 <div class="col-sm-2">
			<button onClick={this.logout.bind(this)} className="login100-form-btn">
				Back!
		</button>
	</div>		
	  </div>
		);
	}
  }
export default Monitor;