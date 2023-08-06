(self.webpackJsonp=self.webpackJsonp||[]).push([[85],{118:function(e,t,s){"use strict";s.d(t,"a",function(){return i});var a=s(9),o=s(18);const i=Object(a.a)(e=>(class extends e{fire(e,t,s){return s=s||{},Object(o.a)(s.node||this,e,t,s)}}))},175:function(e,t,s){"use strict";var a=s(9);t.a=Object(a.a)(e=>(class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}}))},177:function(e,t,s){"use strict";var a=s(3),o=s(0);class i extends o.a{static get styles(){return o.c`
      :host {
        background: var(
          --ha-card-background,
          var(--paper-card-background-color, white)
        );
        border-radius: var(--ha-card-border-radius, 2px);
        box-shadow: var(
          --ha-card-box-shadow,
          0 2px 2px 0 rgba(0, 0, 0, 0.14),
          0 1px 5px 0 rgba(0, 0, 0, 0.12),
          0 3px 1px -2px rgba(0, 0, 0, 0.2)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
        position: relative;
      }

      .card-header,
      :host ::slotted(.card-header) {
        color: var(--ha-card-header-color, --primary-text-color);
        font-family: var(--ha-card-header-font-family, inherit);
        font-size: var(--ha-card-header-font-size, 24px);
        letter-spacing: -0.012em;
        line-height: 32px;
        padding: 24px 16px 16px;
        display: block;
      }

      :host ::slotted(.card-content:not(:first-child)),
      slot:not(:first-child)::slotted(.card-content) {
        padding-top: 0px;
        margin-top: -8px;
      }

      :host ::slotted(.card-content) {
        padding: 16px;
      }

      :host ::slotted(.card-actions) {
        border-top: 1px solid #e8e8e8;
        padding: 5px 16px;
      }
    `}render(){return o.f`
      ${this.header?o.f`
            <div class="card-header">${this.header}</div>
          `:o.f``}
      <slot></slot>
    `}}Object(a.c)([Object(o.g)()],i.prototype,"header",void 0),customElements.define("ha-card",i)},179:function(e,t,s){"use strict";s.d(t,"a",function(){return i});s(109);const a=customElements.get("iron-icon");let o=!1;class i extends a{listen(e,t,a){super.listen(e,t,a),o||"mdi"!==this._iconsetName||(o=!0,s.e(75).then(s.bind(null,219)))}}customElements.define("ha-icon",i)},198:function(e,t,s){"use strict";var a=s(4),o=s(30);s(95);customElements.define("ha-config-section",class extends o.a{static get template(){return a.a`
      <style include="iron-flex ha-style">
        .content {
          padding: 28px 20px 0;
          max-width: 1040px;
          margin: 0 auto;
        }

        .header {
          @apply --paper-font-display1;
          opacity: var(--dark-primary-opacity);
        }

        .together {
          margin-top: 32px;
        }

        .intro {
          @apply --paper-font-subhead;
          width: 100%;
          max-width: 400px;
          margin-right: 40px;
          opacity: var(--dark-primary-opacity);
        }

        .panel {
          margin-top: -24px;
        }

        .panel ::slotted(*) {
          margin-top: 24px;
          display: block;
        }

        .narrow.content {
          max-width: 640px;
        }
        .narrow .together {
          margin-top: 20px;
        }
        .narrow .header {
          @apply --paper-font-headline;
        }
        .narrow .intro {
          font-size: 14px;
          padding-bottom: 20px;
          margin-right: 0;
          max-width: 500px;
        }
      </style>
      <div class$="[[computeContentClasses(isWide)]]">
        <div class="header"><slot name="header"></slot></div>
        <div class$="[[computeClasses(isWide)]]">
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},201:function(e,t,s){"use strict";var a=s(3),o=s(0),i=(s(235),s(212));const r=customElements.get("mwc-switch");let n=class extends r{firstUpdated(){super.firstUpdated(),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)"),this.classList.toggle("slotted",Boolean(this._slot.assignedNodes().length))}static get styles(){return[i.a,o.c`
        :host {
          display: flex;
          flex-direction: row;
          align-items: center;
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__thumb {
          background-color: var(--paper-toggle-button-unchecked-button-color);
          border-color: var(--paper-toggle-button-unchecked-button-color);
        }
        .mdc-switch:not(.mdc-switch--checked) .mdc-switch__track {
          background-color: var(--paper-toggle-button-unchecked-bar-color);
          border-color: var(--paper-toggle-button-unchecked-bar-color);
        }
        :host(.slotted) .mdc-switch {
          margin-right: 24px;
        }
      `]}};Object(a.c)([Object(o.h)("slot")],n.prototype,"_slot",void 0),n=Object(a.c)([Object(o.d)("ha-switch")],n)},204:function(e,t,s){"use strict";var a=s(199);t.a=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()?(e,t)=>e.toLocaleString(t,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):e=>a.a.format(e,"haDateTime")},221:function(e,t,s){"use strict";s(85),s(188);var a=s(4),o=s(30);customElements.define("ha-progress-button",class extends o.a{static get template(){return a.a`
      <style>
        .container {
          position: relative;
          display: inline-block;
        }

        mwc-button {
          transition: all 1s;
        }

        .success mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--google-green-500);
          transition: none;
        }

        .error mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--google-red-500);
          transition: none;
        }

        .progress {
          @apply --layout;
          @apply --layout-center-center;
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
        }
      </style>
      <div class="container" id="container">
        <mwc-button
          id="button"
          disabled="[[computeDisabled(disabled, progress)]]"
          on-click="buttonTapped"
        >
          <slot></slot>
        </mwc-button>
        <template is="dom-if" if="[[progress]]">
          <div class="progress"><paper-spinner active=""></paper-spinner></div>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},progress:{type:Boolean,value:!1},disabled:{type:Boolean,value:!1}}}tempClass(e){var t=this.$.container.classList;t.add(e),setTimeout(()=>{t.remove(e)},1e3)}ready(){super.ready(),this.addEventListener("click",e=>this.buttonTapped(e))}buttonTapped(e){this.progress&&e.stopPropagation()}actionSuccess(){this.tempClass("success")}actionError(){this.tempClass("error")}computeDisabled(e,t){return e||t}})},249:function(e,t,s){"use strict";s(109);var a=s(179);customElements.define("ha-icon-next",class extends a.a{connectedCallback(){super.connectedCallback(),setTimeout(()=>{this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left"},100)}})},260:function(e,t,s){"use strict";var a=s(9),o=s(99);t.a=Object(a.a)(e=>(class extends e{navigate(...e){Object(o.a)(this,...e)}}))},347:function(e,t,s){"use strict";s.d(t,"a",function(){return o});var a=s(48);const o=(e,t)=>Object(a.a)(e,{message:t.localize("ui.common.successfully_saved")})},375:function(e,t,s){"use strict";var a=s(0),o=(s(221),s(18));customElements.define("ha-call-api-button",class extends a.a{render(){return a.f`
      <ha-progress-button
        .progress="${this.progress}"
        @click="${this._buttonTapped}"
        ?disabled="${this.disabled}"
        ><slot></slot
      ></ha-progress-button>
    `}constructor(){super(),this.method="POST",this.data={},this.disabled=!1,this.progress=!1}static get properties(){return{hass:{},progress:Boolean,path:String,method:String,data:{},disabled:Boolean}}get progressButton(){return this.renderRoot.querySelector("ha-progress-button")}async _buttonTapped(){this.progress=!0;const e={method:this.method,path:this.path,data:this.data};try{const s=await this.hass.callApi(this.method,this.path,this.data);this.progress=!1,this.progressButton.actionSuccess(),e.success=!0,e.response=s}catch(t){this.progress=!1,this.progressButton.actionError(),e.success=!1,e.response=t}Object(o.a)(this,"hass-api-called",e)}})},498:function(e,t,s){"use strict";s.d(t,"a",function(){return a}),s.d(t,"b",function(){return o});const a=e=>e.callWS({type:"cloud/alexa/entities"}),o=e=>e.callWS({type:"cloud/alexa/sync"})},732:function(e,t,s){"use strict";s.r(t);var a=s(3),o=(s(85),s(180),s(4)),i=s(30),r=(s(177),s(375),s(152),s(95),s(198),s(0));s(143),s(188),s(201);const n=e=>e.callWS({type:"webhook/list"});var c=s(292),l=s(18);const d=(e,t)=>{Object(l.a)(e,"show-dialog",{dialogTag:"dialog-manage-cloudhook",dialogImport:()=>Promise.all([s.e(1),s.e(23)]).then(s.bind(null,720)),dialogParams:t})};customElements.define("cloud-webhooks",class extends r.a{constructor(){super(),this._progress=[]}static get properties(){return{hass:{},cloudStatus:{},_cloudHooks:{},_localHooks:{},_progress:{}}}connectedCallback(){super.connectedCallback(),this._fetchData()}render(){return r.f`
      ${this.renderStyle()}
      <ha-card header="Webhooks">
        <div class="card-content">
          Anything that is configured to be triggered by a webhook can be given
          a publicly accessible URL to allow you to send data back to Home
          Assistant from anywhere, without exposing your instance to the
          internet. ${this._renderBody()}

          <div class="footer">
            <a href="https://www.nabucasa.com/config/webhooks" target="_blank">
              Learn more about creating webhook-powered automations.
            </a>
          </div>
        </div>
      </ha-card>
    `}updated(e){super.updated(e),e.has("cloudStatus")&&this.cloudStatus&&(this._cloudHooks=this.cloudStatus.prefs.cloudhooks||{})}_renderBody(){return this.cloudStatus&&this._localHooks&&this._cloudHooks?0===this._localHooks.length?r.f`
        <div class="body-text">
          Looks like you have no webhooks yet. Get started by configuring a
          <a href="/config/integrations">webhook-based integration</a> or by
          creating a <a href="/config/automation/new">webhook automation</a>.
        </div>
      `:this._localHooks.map(e=>r.f`
        <div class="webhook" .entry="${e}">
          <paper-item-body two-line>
            <div>
              ${e.name}
              ${e.domain===e.name.toLowerCase()?"":` (${e.domain})`}
            </div>
            <div secondary>${e.webhook_id}</div>
          </paper-item-body>
          ${this._progress.includes(e.webhook_id)?r.f`
                <div class="progress">
                  <paper-spinner active></paper-spinner>
                </div>
              `:this._cloudHooks[e.webhook_id]?r.f`
                <mwc-button @click="${this._handleManageButton}">
                  Manage
                </mwc-button>
              `:r.f`
                <ha-switch @click="${this._enableWebhook}"></ha-switch>
              `}
        </div>
      `):r.f`
        <div class="body-text">Loading…</div>
      `}_showDialog(e){const t=this._localHooks.find(t=>t.webhook_id===e),s=this._cloudHooks[e];d(this,{webhook:t,cloudhook:s,disableHook:()=>this._disableWebhook(e)})}_handleManageButton(e){const t=e.currentTarget.parentElement.entry;this._showDialog(t.webhook_id)}async _enableWebhook(e){const t=e.currentTarget.parentElement.entry;let s;this._progress=[...this._progress,t.webhook_id];try{s=await Object(c.c)(this.hass,t.webhook_id)}catch(a){return void alert(a.message)}finally{this._progress=this._progress.filter(e=>e!==t.webhook_id)}this._cloudHooks=Object.assign(Object.assign({},this._cloudHooks),{[t.webhook_id]:s}),0===this._progress.length&&this._showDialog(t.webhook_id)}async _disableWebhook(e){this._progress=[...this._progress,e];try{await Object(c.d)(this.hass,e)}catch(i){return void alert(`Failed to disable webhook: ${i.message}`)}finally{this._progress=this._progress.filter(t=>t!==e)}const t=this._cloudHooks,s=e,o=(t[s],Object(a.f)(t,["symbol"==typeof s?s:s+""]));this._cloudHooks=o}async _fetchData(){this._localHooks=this.hass.config.components.includes("webhook")?await n(this.hass):[]}renderStyle(){return r.f`
      <style>
        .body-text {
          padding: 8px 0;
        }
        .webhook {
          display: flex;
          padding: 4px 0;
        }
        .progress {
          margin-right: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .footer {
          padding-top: 16px;
        }
        .body-text a,
        .footer a {
          color: var(--primary-color);
        }
      </style>
    `}});var h=s(498);class u extends r.a{constructor(){super(...arguments),this._syncing=!1}render(){if(!this.cloudStatus)return r.f``;const{alexa_enabled:e,alexa_report_state:t}=this.cloudStatus.prefs;return r.f`
      <ha-card header="Alexa">
        <div class="switch">
          <ha-switch
            .checked=${e}
            @change=${this._enabledToggleChanged}
          ></ha-switch>
        </div>
        <div class="card-content">
          With the Alexa integration for Home Assistant Cloud you'll be able to
          control all your Home Assistant devices via any Alexa-enabled device.
          <ul>
            <li>
              <a
                href="https://skills-store.amazon.com/deeplink/dp/B0772J1QKB?deviceType=app"
                target="_blank"
              >
                Enable the Home Assistant skill for Alexa
              </a>
            </li>
            <li>
              <a
                href="https://www.nabucasa.com/config/amazon_alexa/"
                target="_blank"
              >
                Config documentation
              </a>
            </li>
          </ul>
          <em
            >This integration requires an Alexa-enabled device like the Amazon
            Echo.</em
          >
          ${e?r.f`
                <h3>Enable State Reporting</h3>
                <p>
                  If you enable state reporting, Home Assistant will send
                  <b>all</b> state changes of exposed entities to Amazon. This
                  allows you to always see the latest states in the Alexa app
                  and use the state changes to create routines.
                </p>
                <ha-switch
                  .checked=${t}
                  @change=${this._reportToggleChanged}
                ></ha-switch>
              `:""}
        </div>
        <div class="card-actions">
          <mwc-button @click=${this._handleSync} .disabled=${this._syncing}>
            Sync Entities
          </mwc-button>
          <div class="spacer"></div>
          <a href="/config/cloud/alexa">
            <mwc-button>Manage Entities</mwc-button>
          </a>
        </div>
      </ha-card>
    `}async _handleSync(){this._syncing=!0;try{await Object(h.b)(this.hass)}catch(e){alert(`Failed to sync entities: ${e.body.message}`)}finally{this._syncing=!1}}async _enabledToggleChanged(e){const t=e.target;try{await Object(c.j)(this.hass,{alexa_enabled:t.checked}),Object(l.a)(this,"ha-refresh-cloud-status")}catch(s){t.checked=!t.checked}}async _reportToggleChanged(e){const t=e.target;try{await Object(c.j)(this.hass,{alexa_report_state:t.checked}),Object(l.a)(this,"ha-refresh-cloud-status")}catch(s){alert(`Unable to ${t.checked?"enable":"disable"} report state. ${s.message}`),t.checked=!t.checked}}static get styles(){return r.c`
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 32px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
      h3 {
        margin-bottom: 0;
      }
      h3 + p {
        margin-top: 0.5em;
      }
    `}}Object(a.c)([Object(r.g)()],u.prototype,"hass",void 0),Object(a.c)([Object(r.g)()],u.prototype,"cloudStatus",void 0),Object(a.c)([Object(r.g)()],u.prototype,"_syncing",void 0),customElements.define("cloud-alexa-pref",u);var p=s(347);customElements.define("cloud-google-pref",class extends r.a{static get properties(){return{hass:{},cloudStatus:{}}}render(){if(!this.cloudStatus)return r.f``;const{google_enabled:e,google_secure_devices_pin:t}=this.cloudStatus.prefs;return r.f`
      <ha-card header="Google Assistant">
        <div class="switch">
          <ha-switch
            id="google_enabled"
            .checked="${e}"
            @change="${this._toggleChanged}"
          ></ha-switch>
        </div>
        <div class="card-content">
          With the Google Assistant integration for Home Assistant Cloud you'll
          be able to control all your Home Assistant devices via any Google
          Assistant-enabled device.
          <ul>
            <li>
              <a
                href="https://assistant.google.com/services/a/uid/00000091fd5fb875?hl=en-US"
                target="_blank"
              >
                Activate the Home Assistant skill for Google Assistant
              </a>
            </li>
            <li>
              <a
                href="https://www.nabucasa.com/config/google_assistant/"
                target="_blank"
              >
                Config documentation
              </a>
            </li>
          </ul>
          <em
            >This integration requires a Google Assistant-enabled device like
            the Google Home or Android phone.</em
          >
          ${e?r.f`
                <div class="secure_devices">
                  Please enter a pin to interact with security devices. Security
                  devices are doors, garage doors and locks. You will be asked
                  to say/enter this pin when interacting with such devices via
                  Google Assistant.
                  <paper-input
                    label="Secure Devices Pin"
                    id="google_secure_devices_pin"
                    placeholder="Enter a PIN to use secure devices"
                    .value=${t||""}
                    @change="${this._pinChanged}"
                  ></paper-input>
                </div>
              `:""}
        </div>
        <div class="card-actions">
          <ha-call-api-button
            .hass="${this.hass}"
            .disabled="${!e}"
            path="cloud/google_actions/sync"
          >
            Sync entities to Google
          </ha-call-api-button>
          <div class="spacer"></div>
          <a href="/config/cloud/google-assistant">
            <mwc-button>Manage Entities</mwc-button>
          </a>
        </div>
      </ha-card>
    `}async _toggleChanged(e){const t=e.target;try{await Object(c.j)(this.hass,{[t.id]:t.checked}),Object(l.a)(this,"ha-refresh-cloud-status")}catch(s){t.checked=!t.checked}}async _pinChanged(e){const t=e.target;try{await Object(c.j)(this.hass,{[t.id]:t.value||null}),Object(p.a)(this,this.hass),Object(l.a)(this,"ha-refresh-cloud-status")}catch(s){alert(`Unable to store pin: ${s.message}`),t.value=this.cloudStatus.prefs.google_secure_devices_pin}}static get styles(){return r.c`
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 32px;
      }
      ha-call-api-button {
        color: var(--primary-color);
        font-weight: 500;
      }
      .secure_devices {
        padding-top: 16px;
      }
      paper-input {
        width: 250px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
    `}});let g=class extends r.a{static get properties(){return{hass:{},cloudStatus:{}}}render(){if(!this.cloudStatus)return r.f``;const{remote_connected:e,remote_domain:t,remote_certificate:s}=this.cloudStatus;return s?r.f`
      <ha-card header="Remote Control">
        <div class="switch">
          <ha-switch
            .checked="${e}"
            @change="${this._toggleChanged}"
          ></ha-switch>
        </div>
        <div class="card-content">
          Home Assistant Cloud provides a secure remote connection to your
          instance while away from home. Your instance
          ${e?"is":"will be"} available at
          <a href="https://${t}" target="_blank">
            https://${t}</a
          >.
        </div>
        <div class="card-actions">
          <a href="https://www.nabucasa.com/config/remote/" target="_blank">
            <mwc-button>Learn how it works</mwc-button>
          </a>
          ${s?r.f`
                <div class="spacer"></div>
                <mwc-button @click=${this._openCertInfo}>
                  Certificate Info
                </mwc-button>
              `:""}
        </div>
      </ha-card>
    `:r.f`
        <ha-card header="Remote Control">
          <div class="preparing">
            Remote access is being prepared. We will notify you when it's ready.
          </div>
        </ha-card>
      `}_openCertInfo(){var e,t;e=this,t={certificateInfo:this.cloudStatus.remote_certificate},Object(l.a)(e,"show-dialog",{dialogTag:"dialog-cloud-certificate",dialogImport:()=>Promise.all([s.e(1),s.e(30)]).then(s.bind(null,721)),dialogParams:t})}async _toggleChanged(e){const t=e.target;try{t.checked?await Object(c.b)(this.hass):await Object(c.e)(this.hass),Object(l.a)(this,"ha-refresh-cloud-status")}catch(s){alert(s.message),t.checked=!t.checked}}static get styles(){return r.c`
      .preparing {
        padding: 0 16px 16px;
      }
      a {
        color: var(--primary-color);
      }
      .switch {
        position: absolute;
        right: 24px;
        top: 32px;
      }
      .card-actions {
        display: flex;
      }
      .card-actions a {
        text-decoration: none;
      }
      .spacer {
        flex-grow: 1;
      }
    `}};g=Object(a.c)([Object(r.d)("cloud-remote-pref")],g);var b=s(118),m=s(204),f=s(175);customElements.define("cloud-account",class extends(Object(b.a)(Object(f.a)(i.a))){static get template(){return o.a`
      <style include="iron-flex ha-style">
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        .account-row {
          display: flex;
          padding: 0 16px;
        }
        mwc-button {
          align-self: center;
        }
        .soon {
          font-style: italic;
          margin-top: 24px;
          text-align: center;
        }
        .nowrap {
          white-space: nowrap;
        }
        .wrap {
          white-space: normal;
        }
        .status {
          text-transform: capitalize;
          padding: 16px;
        }
        a {
          color: var(--primary-color);
        }
      </style>
      <hass-subpage header="Home Assistant Cloud">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Home Assistant Cloud</span>
            <div slot="introduction">
              <p>
                Thank you for being part of Home Assistant Cloud. It's because
                of people like you that we are able to make a great home
                automation experience for everyone. Thank you!
              </p>
            </div>

            <ha-card header="Nabu Casa Account">
              <div class="account-row">
                <paper-item-body two-line="">
                  [[cloudStatus.email]]
                  <div secondary class="wrap">
                    [[_formatSubscription(_subscription)]]
                  </div>
                </paper-item-body>
              </div>

              <div class="account-row">
                <paper-item-body> Cloud connection status </paper-item-body>
                <div class="status">[[cloudStatus.cloud]]</div>
              </div>

              <div class="card-actions">
                <a href="https://account.nabucasa.com" target="_blank"
                  ><mwc-button>Manage Account</mwc-button></a
                >
                <mwc-button style="float: right" on-click="handleLogout"
                  >Sign out</mwc-button
                >
              </div>
            </ha-card>
          </ha-config-section>

          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Integrations</span>
            <div slot="introduction">
              <p>
                Integrations for Home Assistant Cloud allow you to connect with
                services in the cloud without having to expose your Home
                Assistant instance publicly on the internet.
              </p>
              <p>
                Check the website for
                <a href="https://www.nabucasa.com" target="_blank"
                  >all available features</a
                >.
              </p>
            </div>

            <cloud-remote-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-remote-pref>

            <cloud-alexa-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-alexa-pref>

            <cloud-google-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-google-pref>

            <cloud-webhooks
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-webhooks>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,cloudStatus:Object,_subscription:{type:Object,value:null}}}ready(){super.ready(),this._fetchSubscriptionInfo()}_computeRemoteConnected(e){return e?"Connected":"Not Connected"}async _fetchSubscriptionInfo(){this._subscription=await Object(c.g)(this.hass),this._subscription.provider&&this.cloudStatus&&"connected"!==this.cloudStatus.cloud&&this.fire("ha-refresh-cloud-status")}handleLogout(){this.hass.callApi("post","cloud/logout").then(()=>this.fire("ha-refresh-cloud-status"))}_formatSubscription(e){if(null===e)return"Fetching subscription…";let t=e.human_description;return e.plan_renewal_date&&(t=t.replace("{periodEnd}",Object(m.a)(new Date(1e3*e.plan_renewal_date),this.hass.language))),t}});s(108),s(93),s(110),s(221);var y=s(260);s(249);customElements.define("cloud-login",class extends(Object(y.a)(Object(b.a)(i.a))){static get template(){return o.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        paper-item {
          cursor: pointer;
        }
        ha-card {
          overflow: hidden;
        }
        ha-card .card-header {
          margin-bottom: -8px;
        }
        h1 {
          @apply --paper-font-headline;
          margin: 0;
        }
        .error {
          color: var(--google-red-500);
        }
        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        [hidden] {
          display: none;
        }
        .flash-msg {
          padding-right: 44px;
        }
        .flash-msg paper-icon-button {
          position: absolute;
          top: 8px;
          right: 8px;
          color: var(--secondary-text-color);
        }
      </style>
      <hass-subpage header="Cloud Login">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Home Assistant Cloud</span>
            <div slot="introduction">
              <p>
                Home Assistant Cloud provides you with a secure remote
                connection to your instance while away from home. It also allows
                you to connect with cloud-only services: Amazon Alexa and Google
                Assistant.
              </p>
              <p>
                This service is run by our partner
                <a href="https://www.nabucasa.com" target="_blank"
                  >Nabu&nbsp;Casa,&nbsp;Inc</a
                >, a company founded by the founders of Home Assistant and
                Hass.io.
              </p>
              <p>
                Home Assistant Cloud is a subscription service with a free one
                month trial. No payment information necessary.
              </p>
              <p>
                <a href="https://www.nabucasa.com" target="_blank"
                  >Learn more about Home Assistant Cloud</a
                >
              </p>
            </div>

            <ha-card hidden$="[[!flashMessage]]">
              <div class="card-content flash-msg">
                [[flashMessage]]
                <paper-icon-button icon="hass:close" on-click="_dismissFlash"
                  >Dismiss</paper-icon-button
                >
                <paper-ripple id="flashRipple" noink=""></paper-ripple>
              </div>
            </ha-card>

            <ha-card header="Sign in">
              <div class="card-content">
                <div class="error" hidden$="[[!_error]]">[[_error]]</div>
                <paper-input
                  label="Email"
                  id="email"
                  type="email"
                  value="{{email}}"
                  on-keydown="_keyDown"
                  error-message="Invalid email"
                ></paper-input>
                <paper-input
                  id="password"
                  label="Password"
                  value="{{_password}}"
                  type="password"
                  on-keydown="_keyDown"
                  error-message="Passwords are at least 8 characters"
                ></paper-input>
              </div>
              <div class="card-actions">
                <ha-progress-button
                  on-click="_handleLogin"
                  progress="[[_requestInProgress]]"
                  >Sign in</ha-progress-button
                >
                <button
                  class="link"
                  hidden="[[_requestInProgress]]"
                  on-click="_handleForgotPassword"
                >
                  forgot password?
                </button>
              </div>
            </ha-card>

            <ha-card>
              <paper-item on-click="_handleRegister">
                <paper-item-body two-line="">
                  Start your free 1 month trial
                  <div secondary="">No payment information necessary</div>
                </paper-item-body>
                <ha-icon-next></ha-icon-next>
              </paper-item>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,email:{type:String,notify:!0},_password:{type:String,value:""},_requestInProgress:{type:Boolean,value:!1},flashMessage:{type:String,notify:!0},_error:String}}static get observers(){return["_inputChanged(email, _password)"]}connectedCallback(){super.connectedCallback(),this.flashMessage&&requestAnimationFrame(()=>requestAnimationFrame(()=>this.$.flashRipple.simulatedRipple()))}_inputChanged(){this.$.email.invalid=!1,this.$.password.invalid=!1,this._error=!1}_keyDown(e){13===e.keyCode&&(this._handleLogin(),e.preventDefault())}_handleLogin(){let e=!1;this.email&&this.email.includes("@")||(this.$.email.invalid=!0,this.$.email.focus(),e=!0),this._password.length<8&&(this.$.password.invalid=!0,e||(e=!0,this.$.password.focus())),e||(this._requestInProgress=!0,this.hass.callApi("post","cloud/login",{email:this.email,password:this._password}).then(()=>{this.fire("ha-refresh-cloud-status"),this.setProperties({email:"",_password:""})},e=>{this._password="";const t=e&&e.body&&e.body.code;if("PasswordChangeRequired"===t)return alert("You need to change your password before logging in."),void this.navigate("/config/cloud/forgot-password");const s={_requestInProgress:!1,_error:e&&e.body&&e.body.message?e.body.message:"Unknown error"};"UserNotConfirmed"===t&&(s._error="You need to confirm your email before logging in."),this.setProperties(s),this.$.email.focus()}))}_handleRegister(){this.flashMessage="",this.navigate("/config/cloud/register")}_handleForgotPassword(){this.flashMessage="",this.navigate("/config/cloud/forgot-password")}_dismissFlash(){setTimeout(()=>{this.flashMessage=""},200)}});var v=s(133),w=s(99);const _=["account","google-assistant","alexa"],k=["login","register","forgot-password"];let x=class extends v.a{constructor(){super(...arguments),this.routerOptions={defaultPage:"login",showLoading:!0,initialLoad:()=>this._cloudStatusLoaded,beforeRender:e=>{if(this.cloudStatus.logged_in){if(!_.includes(e))return"account"}else if(!k.includes(e))return"login"},routes:{login:{tag:"cloud-login"},register:{tag:"cloud-register",load:()=>s.e(22).then(s.bind(null,717))},"forgot-password":{tag:"cloud-forgot-password",load:()=>s.e(20).then(s.bind(null,718))},account:{tag:"cloud-account"},"google-assistant":{tag:"cloud-google-assistant",load:()=>s.e(21).then(s.bind(null,761))},alexa:{tag:"cloud-alexa",load:()=>s.e(19).then(s.bind(null,719))}}},this._flashMessage="",this._loginEmail="",this._cloudStatusLoaded=new Promise(e=>{this._resolveCloudStatusLoaded=e})}firstUpdated(e){super.firstUpdated(e),this.addEventListener("cloud-done",e=>{this._flashMessage=e.detail.flashMessage,Object(w.a)(this,"/config/cloud/login")})}updated(e){if(super.updated(e),e.has("cloudStatus")){const t=e.get("cloudStatus");void 0===t?this._resolveCloudStatusLoaded():t.logged_in!==this.cloudStatus.logged_in&&Object(w.a)(this,this.route.prefix,!0)}}createElement(e){const t=super.createElement(e);return t.addEventListener("email-changed",e=>{this._loginEmail=e.detail.value}),t.addEventListener("flash-message-changed",e=>{this._flashMessage=e.detail.value}),t}updatePageEl(e){this.cloudStatus&&!this.cloudStatus.logged_in&&_.includes(this._currentPage)||("setProperties"in e?e.setProperties({hass:this.hass,email:this._loginEmail,isWide:this.isWide,cloudStatus:this.cloudStatus,flashMessage:this._flashMessage}):(e.hass=this.hass,e.email=this._loginEmail,e.isWide=this.isWide,e.narrow=this.narrow,e.cloudStatus=this.cloudStatus,e.flashMessage=this._flashMessage))}};Object(a.c)([Object(r.g)()],x.prototype,"hass",void 0),Object(a.c)([Object(r.g)()],x.prototype,"isWide",void 0),Object(a.c)([Object(r.g)()],x.prototype,"narrow",void 0),Object(a.c)([Object(r.g)()],x.prototype,"route",void 0),Object(a.c)([Object(r.g)()],x.prototype,"cloudStatus",void 0),Object(a.c)([Object(r.g)()],x.prototype,"_flashMessage",void 0),Object(a.c)([Object(r.g)()],x.prototype,"_loginEmail",void 0),x=Object(a.c)([Object(r.d)("ha-config-cloud")],x)}}]);
//# sourceMappingURL=chunk.721e8a5901dd701db8b9.js.map