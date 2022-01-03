
//const axios = require('axios');

import {html, css, LitElement} from 'https://cdn.skypack.dev/pin/lit@v2.0.0-rc.2-TSkkpP2AxiJKOJvPcy1M/mode=imports,min/optimized/lit.js';

class MyElement extends LitElement {

  static properties = {
    version: {},
    clicked: {},
    data: {},
  };

  constructor() {
    super();
    this.version = 'STARTING';
    this.clicked = 0;
    this.data = this.fetch_Userevents();
  }

  fetch_Userevents(){
    show_loader();

    $.get('/API/fetchevents', function(data){
        hide_loader();
        console.log(data);
        return data;
    });

    /*
    $.ajax({
            url: '/API/fetchevents',
            type: 'GET',
            //dataType: "json",
            //data: (d),
            //contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                console.log(result);
                return result;
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                //showerror(jqXhr['responseJSON']['message'], $('#addcomperror'))
                console.log( jqXhr['responseJSON']['message'] );
            }
    });
    */

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