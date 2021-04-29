import React, { Component } from "react";
import { Segment, Comment, Header } from "semantic-ui-react";
import ElizaBot from "elizabot";
import debounce from "lodash.debounce";
import "./css/main.css";
import "./css/util.css";
import "./css/semantic.css";
import "./monitor.css";
import Sketch from "react-p5";
import ImageGallery from "react-image-gallery";
import "./css/carousel.css";
import { Carousel } from "react-responsive-carousel";
import ChatHistory from "./ChatHistory";
import ChatInput from "./ChatInput";

let video;
const axios = require("axios");
const retry = require("retry");

const operation = retry.operation({
  retries: 5,
  factor: 3,
  minTimeout: 1 * 1000,
  maxTimeout: 60 * 1000,
  randomize: true,
});

Massachusetts;

export class Monitor extends Component {
  constructor(props) {
    super(props);
    this.outside = [];
    this.eliza = new ElizaBot();
    this.state = {
      images: [],
      messages: [
        {
          user: false,
          name: this.props.profilename,
          text: this.fixup(this.eliza.getInitial()),
          date: new Date(),
        },
      ],
    };
    this.images = [];
    this.debounced_reply = debounce(this.reply, 2000, { maxWait: 10000 });
  }

  handleInput = (input) => {
    input = input.trim();
    if (!input) return;
    const messages = this.state.messages.slice(0);
    messages.push({
      user: true,
      text: input,
      date: new Date(),
    });

    video.loadPixels();
    const image64 = video.canvas.toDataURL();
    const profilename = this.props.profilename[0];
    const data = { image64, profilename };
    const options = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    };

    operation.attempt(async (currentAttempt) => {
      console.log("sending request: ", currentAttempt, " attempt");
      try {
        axios
          .post("http://localhost:5000/add_emotion_image", {
            image64: image64,
            profilename: profilename,
          })
          .then((response) => response)
          .then((json) => {
            setTimeout(() => {
              fetch(
                "/get_emotion_image?profilename=" +
                  this.props.profilename +
                  "&currenttime=" +
                  Date().toLocaleString()
              )
                .then((response) => response.blob())
                .then((image) => {
                  this.outside = URL.createObjectURL(image);
                  this.state.images.push({
                    data: this.outside,
                  });
                });
            });
          }, 3000);
      } catch (e) {
        if (operation.retry(e)) {
          return;
        }
      }
    });

    this.setState({
      messages,
      images: this.images,
    });

    this.debounced_reply();
  };

  reply = () => {
    const unreplied = [];
    const messages = this.state.messages.slice(0);
    let iter = messages.length - 1;
    while (messages[iter].user && iter >= 0) {
      unreplied.unshift(messages[iter].text);
      iter--;
    }
    if (unreplied.length === 0) return;
    let response = this.eliza.transform(unreplied.join(" "));
    messages.push({
      user: false,
      text: this.fixup(response),
      date: new Date(),
    });
    this.setState({
      messages,
    });
  };

  setup(p5 = "", canvasParentRef = "") {
    p5.noCanvas();
    video = p5.createCapture(p5.VIDEO);
    const v = document.querySelector("video");
    let st =
      "position: absolute; top: 40px; left:5px; display: block; height: 250px; width: 250px; border-radius: 50%;";
    v.setAttribute("style", st);
  }

  stop() {
    const tracks = document.querySelector("video").srcObject.getTracks();
    tracks.forEach(function (track) {
      track.stop();
    });
  }

  fixup(text) {
    // Hack fix for weird "?" spacing in elizabot
    return text.replace(/ \?/g, "?");
  }

  logout() {
    this.stop();
    this.props.backhome();
  }

  render() {
    return (
      <div class="row">
        <div class="col-sm-2">
          <div class="card">
            <div class="card-body">
              <div class="d-flex flex-column align-items-center text-center">
                <div class="mt-6">
                  <h4>Welcome {this.props.profilename}</h4>
                  <Sketch setup={this.setup} draw={this.draw} />
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-sm-1"></div>
        <div class="col-sm-5">
          <Segment>
            <Segment>
              <Header as="h3" block>
                Chat with our Chatbuddy
              </Header>
            </Segment>
            <Segment style={{ overflow: "auto", maxHeight: 600 }}>
              <Comment.Group>
                <ChatHistory messages={this.state.messages} />
                <ChatInput inputHandler={this.handleInput} />
              </Comment.Group>
            </Segment>
          </Segment>
        </div>
        <div class="col-sm-1"></div>
        <div
          class="col-sm-3 pt-4 d-flex justify-content-center"
          id="right-panel"
        >
          <Carousel>
            {this.state.images.map((subItems) => {
              return (
                <>
                  <img src={subItems.data} alt="image" />
                  <p className="legend">{Date().toLocaleString()}</p>{" "}
                </>
              );
            })}
          </Carousel>
        </div>
        <div class="col-sm-2 text-center" id="bottom-panel">
          <button
            onClick={this.logout.bind(this)}
            className="login100-form-btn pt-100 fixed-bottom"
          >
            Back Home
          </button>
        </div>
      </div>
    );
  }
}
export default Monitor;
