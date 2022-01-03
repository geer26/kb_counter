import {html, css, LitElement} from 'https://cdn.skypack.dev/pin/lit@v2.0.0-rc.2-TSkkpP2AxiJKOJvPcy1M/mode=imports,min/optimized/lit.js';
//import {customElement, property, state} from 'https://cdn.skypack.dev/pin/lit@v2.0.0-rc.2-TSkkpP2AxiJKOJvPcy1M/mode=imports,min/optimized//decorators.js';

//import {LitElement, html, css} from '../lit.min.js';
//import {customElement, property, state} from '../lit/decorators.js';

//import {LitElement, html} from 'lit';

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