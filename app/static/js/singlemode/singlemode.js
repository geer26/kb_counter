
import {html, css, LitElement} from 'https://cdn.skypack.dev/pin/lit@v2.0.0-rc.2-TSkkpP2AxiJKOJvPcy1M/mode=imports,min/optimized/lit.js';

class MyElement extends LitElement {

  static properties = {
    version: {},
    clicked: {},
    events: {},
  };

  constructor() {
    super();
    this.version = 'STARTING';
    this.clicked = 0;
    this.events = this.fetch_Userevents();
  }

  fetch_Userevents(){
    show_loader();
    $.get('/API/fetchevents', function(data){
        hide_loader();
        console.log(data['data']);
        return data;
    });
  }

  handleClick(event){
    this.clicked++;
  }

  render() {
    return html`
    <p>Clicked ${this.clicked} times</p>
    <span>
        <button @click=${this.handleClick}>Increase</button>
    </span>
    <h3></h3>

    `;
  }

}

customElements.define('my-element', MyElement);