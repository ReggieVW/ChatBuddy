import React, { Component } from 'react';
import { Input, Icon } from 'semantic-ui-react';
import Dictaphone from "./Dictaphone";

class ChatInput extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: '',
	  message: "",
    };
  }

  handleInput(input) {
    this.props.inputHandler(this.state.value);
    this.setState({
      value: '',
    })
  }

  handleChange = (event) => {
    this.setState({
      value: event.target.value,
    });
  }

  handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      this.handleInput();
    }
  }

  handleClick = () => {
    this.handleInput();
  }
  
  callbackFunction = (childData) => {
      this.setState({value: childData})
}

  render() {
    return (
		<div>
	  <Dictaphone parentCallback = {this.callbackFunction}/>
      <Input
        className="chatInput"
        onChange={this.handleChange}
        onKeyDown={this.handleKeyDown}
        action={{ color: 'teal', icon: 'arrow right', onClick: this.handleClick}}
        placeholder='Write to ChatBuddy...'
        value={this.state.value}
      />
	   </div>
    );
  }
}

export default ChatInput;
