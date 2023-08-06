(self.webpackJsonp=self.webpackJsonp||[]).push([[90],{176:function(e,t,s){"use strict";s.d(t,"a",function(){return r});var a=s(190);const r=e=>void 0===e.attributes.friendly_name?Object(a.a)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""},177:function(e,t,s){"use strict";var a=s(3),r=s(0);class i extends r.a{static get styles(){return r.c`
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
    `}render(){return r.f`
      ${this.header?r.f`
            <div class="card-header">${this.header}</div>
          `:r.f``}
      <slot></slot>
    `}}Object(a.c)([Object(r.g)()],i.prototype,"header",void 0),customElements.define("ha-card",i)},178:function(e,t,s){"use strict";s.d(t,"a",function(){return i});var a=s(120);const r={alert:"hass:alert",alexa:"hass:amazon-alexa",automation:"hass:playlist-play",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:google-pages",script:"hass:file-document",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",weblink:"hass:open-in-new",zone:"hass:map-marker"},i=(e,t)=>{if(e in r)return r[e];switch(e){case"alarm_control_panel":switch(t){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell"}case"binary_sensor":return t&&"off"===t?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===t?"hass:window-closed":"hass:window-open";case"lock":return t&&"unlocked"===t?"hass:lock-open":"hass:lock";case"media_player":return t&&"off"!==t&&"idle"!==t?"hass:cast-connected":"hass:cast";case"zwave":switch(t){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave"}default:return console.warn("Unable to find icon for domain "+e+" ("+t+")"),a.a}}},179:function(e,t,s){"use strict";s.d(t,"a",function(){return i});s(109);const a=customElements.get("iron-icon");let r=!1;class i extends a{listen(e,t,a){super.listen(e,t,a),r||"mdi"!==this._iconsetName||(r=!0,s.e(75).then(s.bind(null,219)))}}customElements.define("ha-icon",i)},190:function(e,t,s){"use strict";s.d(t,"a",function(){return a});const a=e=>e.substr(e.indexOf(".")+1)},194:function(e,t,s){"use strict";var a=s(120);var r=s(121),i=s(178);const n={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",signal_strength:"hass:wifi"};s.d(t,"a",function(){return c});const o={binary_sensor:e=>{const t=e.state&&"off"===e.state;switch(e.attributes.device_class){case"battery":return t?"hass:battery":"hass:battery-outline";case"cold":return t?"hass:thermometer":"hass:snowflake";case"connectivity":return t?"hass:server-network-off":"hass:server-network";case"door":return t?"hass:door-closed":"hass:door-open";case"garage_door":return t?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return t?"hass:shield-check":"hass:alert";case"heat":return t?"hass:thermometer":"hass:fire";case"light":return t?"hass:brightness-5":"hass:brightness-7";case"lock":return t?"hass:lock":"hass:lock-open";case"moisture":return t?"hass:water-off":"hass:water";case"motion":return t?"hass:walk":"hass:run";case"occupancy":return t?"hass:home-outline":"hass:home";case"opening":return t?"hass:square":"hass:square-outline";case"plug":return t?"hass:power-plug-off":"hass:power-plug";case"presence":return t?"hass:home-outline":"hass:home";case"sound":return t?"hass:music-note-off":"hass:music-note";case"vibration":return t?"hass:crop-portrait":"hass:vibrate";case"window":return t?"hass:window-closed":"hass:window-open";default:return t?"hass:radiobox-blank":"hass:checkbox-marked-circle"}},cover:e=>{const t="closed"!==e.state;switch(e.attributes.device_class){case"garage":return t?"hass:garage-open":"hass:garage";case"door":return t?"hass:door-open":"hass:door-closed";case"shutter":return t?"hass:window-shutter-open":"hass:window-shutter";case"blind":return t?"hass:blinds-open":"hass:blinds";case"window":return t?"hass:window-open":"hass:window-closed";default:return Object(i.a)("cover",e.state)}},sensor:e=>{const t=e.attributes.device_class;if(t&&t in n)return n[t];if("battery"===t){const t=Number(e.state);if(isNaN(t))return"hass:battery-unknown";const s=10*Math.round(t/10);return s>=100?"hass:battery":s<=0?"hass:battery-alert":`hass:battery-${s}`}const s=e.attributes.unit_of_measurement;return s===a.j||s===a.k?"hass:thermometer":Object(i.a)("sensor")},input_datetime:e=>e.attributes.has_date?e.attributes.has_time?Object(i.a)("input_datetime"):"hass:calendar":"hass:clock"},c=e=>{if(!e)return a.a;if(e.attributes.icon)return e.attributes.icon;const t=Object(r.a)(e.entity_id);return t in o?o[t](e):Object(i.a)(t,e.state)}},197:function(e,t,s){"use strict";s.d(t,"a",function(){return a});const a=(e,t,s=!1)=>{let a;return function(...r){const i=this,n=s&&!a;clearTimeout(a),a=setTimeout(()=>{a=null,s||e.apply(i,r)},t),n&&e.apply(i,r)}}},198:function(e,t,s){"use strict";var a=s(4),r=s(30);s(95);customElements.define("ha-config-section",class extends r.a{static get template(){return a.a`
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
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},201:function(e,t,s){"use strict";var a=s(3),r=s(0),i=(s(235),s(212));const n=customElements.get("mwc-switch");let o=class extends n{firstUpdated(){super.firstUpdated(),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)"),this.classList.toggle("slotted",Boolean(this._slot.assignedNodes().length))}static get styles(){return[i.a,r.c`
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
      `]}};Object(a.c)([Object(r.h)("slot")],o.prototype,"_slot",void 0),o=Object(a.c)([Object(r.d)("ha-switch")],o)},202:function(e,t,s){"use strict";s.d(t,"b",function(){return a}),s.d(t,"a",function(){return r});const a=(e,t)=>e<t?-1:e>t?1:0,r=(e,t)=>a(e.toLowerCase(),t.toLowerCase())},267:function(e,t,s){"use strict";s.d(t,"a",function(){return n}),s.d(t,"d",function(){return o}),s.d(t,"b",function(){return c}),s.d(t,"c",function(){return d});var a=s(13),r=s(176),i=s(197);const n=(e,t)=>{if(t.name)return t.name;const s=e.states[t.entity_id];return s?Object(r.a)(s):null},o=(e,t,s)=>e.callWS(Object.assign({type:"config/entity_registry/update",entity_id:t},s)),c=(e,t)=>e.callWS({type:"config/entity_registry/remove",entity_id:t}),h=e=>e.sendMessagePromise({type:"config/entity_registry/list"}),l=(e,t)=>e.subscribeEvents(Object(i.a)(()=>h(e).then(e=>t.setState(e,!0)),500,!0),"entity_registry_updated"),d=(e,t)=>Object(a.d)("_entityRegistry",h,l,e,t)},449:function(e,t,s){"use strict";s.d(t,"a",function(){return r}),s.d(t,"b",function(){return i});var a=s(18);const r=()=>Promise.all([s.e(0),s.e(1),s.e(115),s.e(34)]).then(s.bind(null,502)),i=(e,t)=>{Object(a.a)(e,"show-dialog",{dialogTag:"dialog-entity-registry-detail",dialogImport:r,dialogParams:t})}},688:function(e,t,s){"use strict";s.r(t);var a=s(3),r=s(0),i=(s(184),s(143),s(180),s(267)),n=(s(152),s(159),s(177),s(179),s(201),s(178)),o=s(194),c=s(121),h=(s(198),s(449)),l=s(202),d=s(73),u=s(123);class p extends r.a{constructor(){super(...arguments),this._showDisabled=!1,this._filteredEntities=Object(u.a)((e,t)=>t?e:e.filter(e=>!Boolean(e.disabled_by)))}disconnectedCallback(){super.disconnectedCallback(),this._unsubEntities&&this._unsubEntities()}render(){return this.hass&&void 0!==this._entities?r.f`
      <hass-subpage
        header="${this.hass.localize("ui.panel.config.entity_registry.caption")}"
      >
        <ha-config-section .isWide=${this.isWide}>
          <span slot="header">
            ${this.hass.localize("ui.panel.config.entity_registry.picker.header")}
          </span>
          <span slot="introduction">
            ${this.hass.localize("ui.panel.config.entity_registry.picker.introduction")}
            <p>
              ${this.hass.localize("ui.panel.config.entity_registry.picker.introduction2")}
            </p>
            <a href="/config/integrations">
              ${this.hass.localize("ui.panel.config.entity_registry.picker.integrations_page")}
            </a>
          </span>
          <ha-card>
            <paper-item>
              <ha-switch
                ?checked=${this._showDisabled}
                @change=${this._showDisabledChanged}
                >${this.hass.localize("ui.panel.config.entity_registry.picker.show_disabled")}</ha-switch
              ></paper-item
            >
            ${this._filteredEntities(this._entities,this._showDisabled).map(e=>{const t=this.hass.states[e.entity_id];return r.f`
                  <paper-icon-item
                    @click=${this._openEditEntry}
                    .entry=${e}
                    class=${Object(d.a)({"disabled-entry":!!e.disabled_by})}
                  >
                    <ha-icon
                      slot="item-icon"
                      .icon=${t?Object(o.a)(t):Object(n.a)(Object(c.a)(e.entity_id))}
                    ></ha-icon>
                    <paper-item-body two-line>
                      <div class="name">
                        ${Object(i.a)(this.hass,e)||`(${this.hass.localize("state.default.unavailable")})`}
                      </div>
                      <div class="secondary entity-id">
                        ${e.entity_id}
                      </div>
                    </paper-item-body>
                    <div class="platform">
                      ${e.platform}
                      ${e.disabled_by?r.f`
                            <br />(disabled)
                          `:""}
                    </div>
                  </paper-icon-item>
                `})}
          </ha-card>
        </ha-config-section>
      </hass-subpage>
    `:r.f`
        <hass-loading-screen></hass-loading-screen>
      `}firstUpdated(e){super.firstUpdated(e),Object(h.a)()}updated(e){super.updated(e),this._unsubEntities||(this._unsubEntities=Object(i.c)(this.hass.connection,e=>{this._entities=e.sort((e,t)=>Object(l.b)(e.entity_id,t.entity_id))}))}_showDisabledChanged(e){this._showDisabled=e.target.checked}_openEditEntry(e){const t=e.currentTarget.entry;Object(h.b)(this,{entry:t})}static get styles(){return r.c`
      a {
        color: var(--primary-color);
      }
      ha-card {
        margin-bottom: 24px;
        direction: ltr;
      }
      paper-icon-item {
        cursor: pointer;
        color: var(--primary-text-color);
      }
      ha-icon {
        margin-left: 8px;
      }
      .platform {
        text-align: right;
        margin: 0 0 0 8px;
      }
      .disabled-entry {
        color: var(--secondary-text-color);
      }
    `}}Object(a.c)([Object(r.g)()],p.prototype,"hass",void 0),Object(a.c)([Object(r.g)()],p.prototype,"isWide",void 0),Object(a.c)([Object(r.g)()],p.prototype,"_entities",void 0),Object(a.c)([Object(r.g)()],p.prototype,"_showDisabled",void 0),customElements.define("ha-config-entity-registry",p)}}]);
//# sourceMappingURL=chunk.4846b0d76a6eb399afc5.js.map