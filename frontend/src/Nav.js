import React, {Component} from 'react';
import './App.css';
import Nav from './Nav';
import Monitor from './Monitor';

export class Nav extends Component {

	constructor(props){
		super(props);
	}

	render(){
    	return (<nav >
            <h3>Logo</h3>
    		    <ul>
                    <li>About</li>
                    <li>Monitor</li>
                </ul>
    		</nav>
		)
	}
}
export default Monitor;