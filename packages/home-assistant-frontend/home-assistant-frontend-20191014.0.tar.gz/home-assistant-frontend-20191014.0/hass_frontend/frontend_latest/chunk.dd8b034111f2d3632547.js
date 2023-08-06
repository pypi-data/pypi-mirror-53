/*! For license information please see chunk.dd8b034111f2d3632547.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[154],{188:function(e,r,t){"use strict";t(5),t(68),t(151);var i=t(6),s=t(4),o=t(125);const a=s.a`
  <style include="paper-spinner-styles"></style>

  <div id="spinnerContainer" class-name="[[__computeContainerClasses(active, __coolingDown)]]" on-animationend="__reset" on-webkit-animation-end="__reset">
    <div class="spinner-layer layer-1">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-2">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-3">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>

    <div class="spinner-layer layer-4">
      <div class="circle-clipper left">
        <div class="circle"></div>
      </div>
      <div class="circle-clipper right">
        <div class="circle"></div>
      </div>
    </div>
  </div>
`;a.setAttribute("strip-whitespace",""),Object(i.a)({_template:a,is:"paper-spinner",behaviors:[o.a]})},240:function(e,r,t){"use strict";var i=t(3);let s;var o=t(18),a=t(0);let n=class extends a.b{constructor(){super(...arguments),this.autofocus=!1,this.rtl=!1,this.error=!1,this._value=""}set value(e){this._value=e}get value(){return this.codemirror?this.codemirror.getValue():this._value}get hasComments(){return!!this.shadowRoot.querySelector("span.cm-comment")}connectedCallback(){super.connectedCallback(),this.codemirror&&(this.codemirror.refresh(),!1!==this.autofocus&&this.codemirror.focus())}update(e){super.update(e),this.codemirror&&(e.has("mode")&&this.codemirror.setOption("mode",this.mode),e.has("autofocus")&&this.codemirror.setOption("autofocus",!1!==this.autofocus),e.has("_value")&&this._value!==this.value&&this.codemirror.setValue(this._value),e.has("rtl")&&(this.codemirror.setOption("gutters",this._calcGutters()),this._setScrollBarDirection()),e.has("error")&&this.classList.toggle("error-state",this.error))}firstUpdated(e){super.firstUpdated(e),this._load()}async _load(){const e=await(async()=>(s||(s=Promise.all([t.e(114),t.e(23)]).then(t.bind(null,717))),s))(),r=e.codeMirror,i=this.attachShadow({mode:"open"});i.innerHTML=`\n    <style>\n      ${e.codeMirrorCss}\n      .CodeMirror {\n        height: var(--code-mirror-height, auto);\n        direction: var(--code-mirror-direction, ltr);\n      }\n      .CodeMirror-scroll {\n        max-height: var(--code-mirror-max-height, --code-mirror-height);\n      }\n      .CodeMirror-gutters {\n        border-right: 1px solid var(--paper-input-container-color, var(--secondary-text-color));\n        background-color: var(--paper-dialog-background-color, var(--primary-background-color));\n        transition: 0.2s ease border-right;\n      }\n      :host(.error-state) .CodeMirror-gutters {\n        border-color: var(--error-state-color, red);\n      }\n      .CodeMirror-focused .CodeMirror-gutters {\n        border-right: 2px solid var(--paper-input-container-focus-color, var(--primary-color));\n      }\n      .CodeMirror-linenumber {\n        color: var(--paper-dialog-color, var(--primary-text-color));\n      }\n      .rtl .CodeMirror-vscrollbar {\n        right: auto;\n        left: 0px;\n      }\n      .rtl-gutter {\n        width: 20px;\n      }\n    </style>`,this.codemirror=r(i,{value:this._value,lineNumbers:!0,tabSize:2,mode:this.mode,autofocus:!1!==this.autofocus,viewportMargin:1/0,extraKeys:{Tab:"indentMore","Shift-Tab":"indentLess"},gutters:this._calcGutters()}),this._setScrollBarDirection(),this.codemirror.on("changes",()=>this._onChange())}_onChange(){const e=this.value;e!==this._value&&(this._value=e,Object(o.a)(this,"value-changed",{value:this._value}))}_calcGutters(){return this.rtl?["rtl-gutter","CodeMirror-linenumbers"]:[]}_setScrollBarDirection(){this.codemirror&&this.codemirror.getWrapperElement().classList.toggle("rtl",this.rtl)}};Object(i.c)([Object(a.g)()],n.prototype,"mode",void 0),Object(i.c)([Object(a.g)()],n.prototype,"autofocus",void 0),Object(i.c)([Object(a.g)()],n.prototype,"rtl",void 0),Object(i.c)([Object(a.g)()],n.prototype,"error",void 0),Object(i.c)([Object(a.g)()],n.prototype,"_value",void 0),n=Object(i.c)([Object(a.d)("ha-code-editor")],n)},691:function(e,r,t){"use strict";t.r(r);t(188);var i=t(12),s=t(22),o=t(4),a=t(30);t(240),t(95);customElements.define("developer-tools-template",class extends a.a{static get template(){return o.a`
      <style include="ha-style iron-flex iron-positioning"></style>
      <style>
        :host {
          -ms-user-select: initial;
          -webkit-user-select: initial;
          -moz-user-select: initial;
        }

        .content {
          padding: 16px;
          direction: ltr;
        }

        .edit-pane {
          margin-right: 16px;
        }

        .edit-pane a {
          color: var(--dark-primary-color);
        }

        .horizontal .edit-pane {
          max-width: 50%;
        }

        .render-pane {
          position: relative;
          max-width: 50%;
        }

        .render-spinner {
          position: absolute;
          top: 8px;
          right: 8px;
        }

        .rendered {
          @apply --paper-font-code1;
          clear: both;
          white-space: pre-wrap;
        }

        .rendered.error {
          color: red;
        }
      </style>

      <div class$="[[computeFormClasses(narrow)]]">
        <div class="edit-pane">
          <p>
            Templates are rendered using the Jinja2 template engine with some
            Home Assistant specific extensions.
          </p>
          <ul>
            <li>
              <a
                href="http://jinja.pocoo.org/docs/dev/templates/"
                target="_blank"
                >Jinja2 template documentation</a
              >
            </li>
            <li>
              <a
                href="https://home-assistant.io/docs/configuration/templating/"
                target="_blank"
                >Home Assistant template extensions</a
              >
            </li>
          </ul>
          <p>Template editor</p>
          <ha-code-editor
            mode="jinja2"
            value="[[template]]"
            error="[[error]]"
            autofocus
            on-value-changed="templateChanged"
          ></ha-code-editor>
        </div>

        <div class="render-pane">
          <paper-spinner
            class="render-spinner"
            active="[[rendering]]"
          ></paper-spinner>
          <pre class$="[[computeRenderedClasses(error)]]">[[processed]]</pre>
        </div>
      </div>
    `}static get properties(){return{hass:{type:Object},error:{type:Boolean,value:!1},rendering:{type:Boolean,value:!1},template:{type:String,value:'Imitate available variables:\n{% set my_test_json = {\n  "temperature": 25,\n  "unit": "°C"\n} %}\n\nThe temperature is {{ my_test_json.temperature }} {{ my_test_json.unit }}.\n\n{% if is_state("device_tracker.paulus", "home") and\n      is_state("device_tracker.anne_therese", "home") -%}\n  You are both home, you silly\n{%- else -%}\n  Anne Therese is at {{ states("device_tracker.anne_therese") }}\n  Paulus is at {{ states("device_tracker.paulus") }}\n{%- endif %}\n\nFor loop example:\n{% for state in states.sensor -%}\n  {%- if loop.first %}The {% elif loop.last %} and the {% else %}, the {% endif -%}\n  {{ state.name | lower }} is {{state.state_with_unit}}\n{%- endfor %}.'},processed:{type:String,value:""}}}ready(){super.ready(),this.renderTemplate()}computeFormClasses(e){return e?"content fit":"content fit layout horizontal"}computeRenderedClasses(e){return e?"error rendered":"rendered"}templateChanged(e){this.template=e.detail.value,this.error&&(this.error=!1),this._debouncer=s.a.debounce(this._debouncer,i.d.after(500),()=>{this.renderTemplate()})}renderTemplate(){this.rendering=!0,this.hass.callApi("POST","template",{template:this.template}).then(function(e){this.processed=e,this.rendering=!1}.bind(this),function(e){this.processed=e&&e.body&&e.body.message||"Unknown error rendering template",this.error=!0,this.rendering=!1}.bind(this))}})}}]);
//# sourceMappingURL=chunk.dd8b034111f2d3632547.js.map