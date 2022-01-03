
//const axios = require('axios');

import {html, css, LitElement} from 'https://cdn.skypack.dev/pin/lit@v2.0.0-rc.2-TSkkpP2AxiJKOJvPcy1M/mode=imports,min/optimized/lit.js';

class MyElement extends LitElement {

  static properties = {
    version: {},
    clicked: {},
  };

  constructor() {
    super();
    this.version = 'STARTING';
    this.clicked = 0;
  }

  handleClick(event){
    this.clicked++;
  }

  render() {
    return html`
    <p>Welcome to the Lit tutorial!</p>
    <p>This is the ${this.version} code.</p>
    <p>Clicked ${this.clicked} times</p>
    <span>
        <button @click=${this.handleClick}>Increase</button>
    </span>


    `;
  }

}

customElements.define('my-element', MyElement);