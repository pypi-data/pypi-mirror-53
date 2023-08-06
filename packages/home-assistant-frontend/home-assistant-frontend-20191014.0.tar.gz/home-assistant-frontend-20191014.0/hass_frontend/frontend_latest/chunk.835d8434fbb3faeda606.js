(self.webpackJsonp=self.webpackJsonp||[]).push([[18],{176:function(t,e,a){"use strict";a.d(e,"a",function(){return i});var s=a(190);const i=t=>void 0===t.attributes.friendly_name?Object(s.a)(t.entity_id).replace(/_/g," "):t.attributes.friendly_name||""},178:function(t,e,a){"use strict";a.d(e,"a",function(){return n});var s=a(120);const i={alert:"hass:alert",alexa:"hass:amazon-alexa",automation:"hass:playlist-play",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:google-pages",script:"hass:file-document",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",weblink:"hass:open-in-new",zone:"hass:map-marker"},n=(t,e)=>{if(t in i)return i[t];switch(t){case"alarm_control_panel":switch(e){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell"}case"binary_sensor":return e&&"off"===e?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===e?"hass:window-closed":"hass:window-open";case"lock":return e&&"unlocked"===e?"hass:lock-open":"hass:lock";case"media_player":return e&&"off"!==e&&"idle"!==e?"hass:cast-connected":"hass:cast";case"zwave":switch(e){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave"}default:return console.warn("Unable to find icon for domain "+t+" ("+e+")"),s.a}}},181:function(t,e,a){"use strict";a.d(e,"a",function(){return i});var s=a(121);const i=t=>Object(s.a)(t.entity_id)},185:function(t,e,a){"use strict";var s=a(3),i=a(0),n=(a(179),a(181)),o=a(194);class r extends i.a{render(){const t=this.stateObj;return t?i.f`
      <ha-icon
        id="icon"
        data-domain=${Object(n.a)(t)}
        data-state=${t.state}
        .icon=${this.overrideIcon||Object(o.a)(t)}
      ></ha-icon>
    `:i.f``}updated(t){if(!t.has("stateObj")||!this.stateObj)return;const e=this.stateObj,a={color:"",filter:""},s={backgroundImage:""};if(e)if(e.attributes.entity_picture&&!this.overrideIcon||this.overrideImage){let t=this.overrideImage||e.attributes.entity_picture;this.hass&&(t=this.hass.hassUrl(t)),s.backgroundImage=`url(${t})`,a.display="none"}else{if(e.attributes.hs_color){const t=e.attributes.hs_color[0],s=e.attributes.hs_color[1];s>10&&(a.color=`hsl(${t}, 100%, ${100-s/2}%)`)}if(e.attributes.brightness){const t=e.attributes.brightness;if("number"!=typeof t){const a=`Type error: state-badge expected number, but type of ${e.entity_id}.attributes.brightness is ${typeof t} (${t})`;console.warn(a)}a.filter=`brightness(${(t+245)/5}%)`}}Object.assign(this._icon.style,a),Object.assign(this.style,s)}static get styles(){return i.c`
      :host {
        position: relative;
        display: inline-block;
        width: 40px;
        color: var(--paper-item-icon-color, #44739e);
        border-radius: 50%;
        height: 40px;
        text-align: center;
        background-size: cover;
        line-height: 40px;
        vertical-align: middle;
      }

      ha-icon {
        transition: color 0.3s ease-in-out, filter 0.3s ease-in-out;
      }

      /* Color the icon if light or sun is on */
      ha-icon[data-domain="light"][data-state="on"],
      ha-icon[data-domain="switch"][data-state="on"],
      ha-icon[data-domain="binary_sensor"][data-state="on"],
      ha-icon[data-domain="fan"][data-state="on"],
      ha-icon[data-domain="sun"][data-state="above_horizon"] {
        color: var(--paper-item-icon-active-color, #fdd835);
      }

      /* Color the icon if unavailable */
      ha-icon[data-state="unavailable"] {
        color: var(--state-icon-unavailable-color);
      }
    `}}Object(s.c)([Object(i.g)()],r.prototype,"stateObj",void 0),Object(s.c)([Object(i.g)()],r.prototype,"overrideIcon",void 0),Object(s.c)([Object(i.g)()],r.prototype,"overrideImage",void 0),Object(s.c)([Object(i.h)("ha-icon")],r.prototype,"_icon",void 0),customElements.define("state-badge",r)},190:function(t,e,a){"use strict";a.d(e,"a",function(){return s});const s=t=>t.substr(t.indexOf(".")+1)},191:function(t,e,a){"use strict";var s=a(4),i=a(30),n=(a(233),a(185),a(176)),o=a(96);customElements.define("state-info",class extends i.a{static get template(){return s.a`
      ${this.styleTemplate} ${this.stateBadgeTemplate} ${this.infoTemplate}
    `}static get styleTemplate(){return s.a`
      <style>
        :host {
          @apply --paper-font-body1;
          min-width: 120px;
          white-space: nowrap;
        }

        state-badge {
          float: left;
        }

        :host([rtl]) state-badge {
          float: right;
        }

        .info {
          margin-left: 56px;
        }

        :host([rtl]) .info {
          margin-right: 56px;
          margin-left: 0;
          text-align: right;
        }

        .name {
          @apply --paper-font-common-nowrap;
          color: var(--primary-text-color);
          line-height: 40px;
        }

        .name[in-dialog],
        :host([secondary-line]) .name {
          line-height: 20px;
        }

        .time-ago,
        .extra-info,
        .extra-info > * {
          @apply --paper-font-common-nowrap;
          color: var(--secondary-text-color);
        }
      </style>
    `}static get stateBadgeTemplate(){return s.a`
      <state-badge state-obj="[[stateObj]]"></state-badge>
    `}static get infoTemplate(){return s.a`
      <div class="info">
        <div class="name" in-dialog$="[[inDialog]]">
          [[computeStateName(stateObj)]]
        </div>

        <template is="dom-if" if="[[inDialog]]">
          <div class="time-ago">
            <ha-relative-time
              hass="[[hass]]"
              datetime="[[stateObj.last_changed]]"
            ></ha-relative-time>
          </div>
        </template>
        <template is="dom-if" if="[[!inDialog]]">
          <div class="extra-info"><slot> </slot></div>
        </template>
      </div>
    `}static get properties(){return{hass:Object,stateObj:Object,inDialog:{type:Boolean,value:()=>!1},rtl:{type:Boolean,reflectToAttribute:!0,computed:"computeRTL(hass)"}}}computeStateName(t){return Object(n.a)(t)}computeRTL(t){return Object(o.a)(t)}})},194:function(t,e,a){"use strict";var s=a(120);var i=a(121),n=a(178);const o={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",signal_strength:"hass:wifi"};a.d(e,"a",function(){return c});const r={binary_sensor:t=>{const e=t.state&&"off"===t.state;switch(t.attributes.device_class){case"battery":return e?"hass:battery":"hass:battery-outline";case"cold":return e?"hass:thermometer":"hass:snowflake";case"connectivity":return e?"hass:server-network-off":"hass:server-network";case"door":return e?"hass:door-closed":"hass:door-open";case"garage_door":return e?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return e?"hass:shield-check":"hass:alert";case"heat":return e?"hass:thermometer":"hass:fire";case"light":return e?"hass:brightness-5":"hass:brightness-7";case"lock":return e?"hass:lock":"hass:lock-open";case"moisture":return e?"hass:water-off":"hass:water";case"motion":return e?"hass:walk":"hass:run";case"occupancy":return e?"hass:home-outline":"hass:home";case"opening":return e?"hass:square":"hass:square-outline";case"plug":return e?"hass:power-plug-off":"hass:power-plug";case"presence":return e?"hass:home-outline":"hass:home";case"sound":return e?"hass:music-note-off":"hass:music-note";case"vibration":return e?"hass:crop-portrait":"hass:vibrate";case"window":return e?"hass:window-closed":"hass:window-open";default:return e?"hass:radiobox-blank":"hass:checkbox-marked-circle"}},cover:t=>{const e="closed"!==t.state;switch(t.attributes.device_class){case"garage":return e?"hass:garage-open":"hass:garage";case"door":return e?"hass:door-open":"hass:door-closed";case"shutter":return e?"hass:window-shutter-open":"hass:window-shutter";case"blind":return e?"hass:blinds-open":"hass:blinds";case"window":return e?"hass:window-open":"hass:window-closed";default:return Object(n.a)("cover",t.state)}},sensor:t=>{const e=t.attributes.device_class;if(e&&e in o)return o[e];if("battery"===e){const e=Number(t.state);if(isNaN(e))return"hass:battery-unknown";const a=10*Math.round(e/10);return a>=100?"hass:battery":a<=0?"hass:battery-alert":`hass:battery-${a}`}const a=t.attributes.unit_of_measurement;return a===s.j||a===s.k?"hass:thermometer":Object(n.a)("sensor")},input_datetime:t=>t.attributes.has_date?t.attributes.has_time?Object(n.a)("input_datetime"):"hass:calendar":"hass:clock"},c=t=>{if(!t)return s.a;if(t.attributes.icon)return t.attributes.icon;const e=Object(i.a)(t.entity_id);return e in r?r[e](t):Object(n.a)(e,t.state)}},203:function(t,e,a){"use strict";a.d(e,"b",function(){return s}),a.d(e,"a",function(){return i});const s=(t,e)=>t<e?-1:t>e?1:0,i=(t,e)=>s(t.toLowerCase(),e.toLowerCase())},233:function(t,e,a){"use strict";var s=a(1),i=a(30),n=a(245),o=a(175);customElements.define("ha-relative-time",class extends(Object(o.a)(i.a)){static get properties(){return{hass:Object,datetime:{type:String,observer:"datetimeChanged"},datetimeObj:{type:Object,observer:"datetimeObjChanged"},parsedDateTime:Object}}constructor(){super(),this.updateRelative=this.updateRelative.bind(this)}connectedCallback(){super.connectedCallback(),this.updateInterval=setInterval(this.updateRelative,6e4)}disconnectedCallback(){super.disconnectedCallback(),clearInterval(this.updateInterval)}datetimeChanged(t){this.parsedDateTime=t?new Date(t):null,this.updateRelative()}datetimeObjChanged(t){this.parsedDateTime=t,this.updateRelative()}updateRelative(){const t=Object(s.a)(this);this.parsedDateTime?t.innerHTML=Object(n.a)(this.parsedDateTime,this.localize):t.innerHTML=this.localize("ui.components.relative_time.never")}})},245:function(t,e,a){"use strict";a.d(e,"a",function(){return n});const s=[60,60,24,7],i=["second","minute","hour","day"];function n(t,e,a={}){let n=((a.compareTime||new Date).getTime()-t.getTime())/1e3;const o=n>=0?"past":"future";let r;n=Math.abs(n);for(let c=0;c<s.length;c++){if(n<s[c]){n=Math.floor(n),r=e(`ui.components.relative_time.duration.${i[c]}`,"count",n);break}n/=s[c]}return void 0===r&&(r=e("ui.components.relative_time.duration.week","count",n=Math.floor(n))),!1===a.includeTense?r:e(`ui.components.relative_time.${o}`,"time",r)}},457:function(t,e,a){"use strict";a.d(e,"b",function(){return i}),a.d(e,"a",function(){return n});var s=a(121);const i=t=>t.include_domains.length+t.include_entities.length+t.exclude_domains.length+t.exclude_entities.length===0,n=(t,e,a,i)=>{const n=new Set(t),o=new Set(e),r=new Set(a),c=new Set(i),h=n.size>0||o.size>0,l=r.size>0||c.size>0;return h||l?h&&!l?t=>o.has(t)||n.has(Object(s.a)(t)):!h&&l?t=>!c.has(t)&&!r.has(Object(s.a)(t)):n.size?t=>n.has(Object(s.a)(t))?!c.has(t):o.has(t):r.size?t=>r.has(Object(s.a)(t))?o.has(t):!c.has(t):t=>o.has(t):()=>!0}},458:function(t,e,a){"use strict";a.d(e,"a",function(){return n});var s=a(18);const i=()=>Promise.all([a.e(1),a.e(32)]).then(a.bind(null,503)),n=(t,e)=>{Object(s.a)(t,"show-dialog",{dialogTag:"dialog-domain-toggler",dialogImport:i,dialogParams:e})}},720:function(t,e,a){"use strict";a.r(e);var s=a(3),i=a(0),n=(a(108),a(123)),o=(a(152),a(160),a(177),a(201),a(191),a(293)),r=a(457),c=a(203),h=a(18),l=a(458),d=a(500),u=a(176),p=a(121);const b=["Alexa.EndpointHealth"],m=t=>void 0===t.should_expose||t.should_expose;let g=class extends i.a{constructor(){super(...arguments),this._entityConfigs={},this._popstateSyncAttached=!1,this._popstateReloadStatusAttached=!1,this._getEntityFilterFunc=Object(n.a)(t=>Object(r.a)(t.include_domains,t.include_entities,t.exclude_domains,t.exclude_entities))}render(){if(void 0===this._entities)return i.f`
        <hass-loading-screen></hass-loading-screen>
      `;const t=Object(r.b)(this.cloudStatus.alexa_entities),e=this._getEntityFilterFunc(this.cloudStatus.alexa_entities),a=this._isInitialExposed||new Set,s=void 0===this._isInitialExposed;let n=0;const o=[],c=[];return this._entities.forEach(r=>{const h=this.hass.states[r.entity_id],l=this._entityConfigs[r.entity_id]||{},d=t?m(l):e(r.entity_id);d&&(n++,s&&a.add(r.entity_id)),(a.has(r.entity_id)?o:c).push(i.f`
        <ha-card>
          <div class="card-content">
            <state-info
              .hass=${this.hass}
              .stateObj=${h}
              secondary-line
              @click=${this._showMoreInfo}
            >
              ${r.interfaces.filter(t=>!b.includes(t)).map(t=>t.replace("Alexa.","").replace("Controller","")).join(", ")}
            </state-info>
            <ha-switch
              .entityId=${r.entity_id}
              .disabled=${!t}
              .checked=${d}
              @change=${this._exposeChanged}
            >
              ${this.hass.localize("ui.panel.config.cloud.alexa.expose")}
            </ha-switch>
          </div>
        </ha-card>
      `)}),s&&(this._isInitialExposed=a),i.f`
      <hass-subpage header="${this.hass.localize("ui.panel.config.cloud.alexa.title")}">
        <span slot="toolbar-icon">
          ${n}${this.narrow?"":i.f`
            selected
          `}
        </span>
        ${t?i.f`
                <paper-icon-button
                  slot="toolbar-icon"
                  icon="hass:tune"
                  @click=${this._openDomainToggler}
                ></paper-icon-button>
              `:""}
        ${t?"":i.f`
                <div class="banner">
                  ${this.hass.localize("ui.panel.config.cloud.alexa.banner")}
                </div>
              `}
          ${o.length>0?i.f`
                  <h1>
                    ${this.hass.localize("ui.panel.config.cloud.alexa.exposed_entities")}
                  </h1>
                  <div class="content">${o}</div>
                `:""}
          ${c.length>0?i.f`
                  <h1>
                    ${this.hass.localize("ui.panel.config.cloud.alexa.not_exposed_entities")}
                  </h1>
                  <div class="content">${c}</div>
                `:""}
        </div>
      </hass-subpage>
    `}firstUpdated(t){super.firstUpdated(t),this._fetchData()}updated(t){super.updated(t),t.has("cloudStatus")&&(this._entityConfigs=this.cloudStatus.prefs.alexa_entity_configs)}async _fetchData(){const t=await Object(d.a)(this.hass);t.sort((t,e)=>{const a=this.hass.states[t.entity_id],s=this.hass.states[e.entity_id];return Object(c.b)(a?Object(u.a)(a):t.entity_id,s?Object(u.a)(s):e.entity_id)}),this._entities=t}_showMoreInfo(t){const e=t.currentTarget.stateObj.entity_id;Object(h.a)(this,"hass-more-info",{entityId:e})}async _exposeChanged(t){const e=t.currentTarget.entityId,a=t.target.checked;await this._updateExposed(e,a)}async _updateExposed(t,e){e!==m(this._entityConfigs[t]||{})&&(await this._updateConfig(t,{should_expose:e}),this._ensureEntitySync())}async _updateConfig(t,e){const a=await Object(o.h)(this.hass,t,e);this._entityConfigs=Object.assign(Object.assign({},this._entityConfigs),{[t]:a}),this._ensureStatusReload()}_openDomainToggler(){Object(l.a)(this,{domains:this._entities.map(t=>Object(p.a)(t.entity_id)).filter((t,e,a)=>a.indexOf(t)===e),toggleDomain:(t,e)=>{this._entities.forEach(a=>{Object(p.a)(a.entity_id)===t&&this._updateExposed(a.entity_id,e)})}})}_ensureStatusReload(){if(this._popstateReloadStatusAttached)return;this._popstateReloadStatusAttached=!0;const t=this.parentElement;window.addEventListener("popstate",()=>Object(h.a)(t,"ha-refresh-cloud-status"),{once:!0})}_ensureEntitySync(){this._popstateSyncAttached||(this._popstateSyncAttached=!0,window.addEventListener("popstate",()=>{},{once:!0}))}static get styles(){return i.c`
      .banner {
        color: var(--primary-text-color);
        background-color: var(
          --ha-card-background,
          var(--paper-card-background-color, white)
        );
        padding: 16px 8px;
        text-align: center;
      }
      h1 {
        color: var(--primary-text-color);
        font-size: 24px;
        letter-spacing: -0.012em;
        margin-bottom: 0;
        padding: 0 8px;
      }
      .content {
        display: flex;
        flex-wrap: wrap;
        padding: 4px;
      }
      ha-switch {
        clear: both;
      }
      ha-card {
        margin: 4px;
        width: 100%;
        max-width: 300px;
      }
      .card-content {
        padding-bottom: 12px;
      }
      state-info {
        cursor: pointer;
      }
      ha-switch {
        padding: 8px 0;
      }

      @media all and (max-width: 450px) {
        ha-card {
          max-width: 100%;
        }
      }
    `}};Object(s.c)([Object(i.g)()],g.prototype,"hass",void 0),Object(s.c)([Object(i.g)()],g.prototype,"cloudStatus",void 0),Object(s.c)([Object(i.g)({type:Boolean})],g.prototype,"narrow",void 0),Object(s.c)([Object(i.g)()],g.prototype,"_entities",void 0),Object(s.c)([Object(i.g)()],g.prototype,"_entityConfigs",void 0),g=Object(s.c)([Object(i.d)("cloud-alexa")],g)}}]);
//# sourceMappingURL=chunk.835d8434fbb3faeda606.js.map