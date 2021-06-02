import React, { Component } from 'react';
import { Comment } from 'semantic-ui-react';
import robotAvatar from './goldfish.svg';
import humanAvatar from './human.svg';

class ChatMessage extends Component {
  render() {
    const message = this.props.message;
    let avatar = robotAvatar;
    let author = 'CHATBUDDY';
    if (message.user) {
      avatar = humanAvatar;
      author = 'Me';
    }

    return (
      <Comment>
       <Comment.Avatar src={avatar} />
        <Comment.Content>
          <Comment.Author as='a'>{author}</Comment.Author>
          <Comment.Metadata>
            <div>Today at {message.date.toLocaleTimeString()}</div>
          </Comment.Metadata>
          <Comment.Text>{message.text}</Comment.Text>
        </Comment.Content>
      </Comment>
    );
  }
}

export default ChatMessage;
