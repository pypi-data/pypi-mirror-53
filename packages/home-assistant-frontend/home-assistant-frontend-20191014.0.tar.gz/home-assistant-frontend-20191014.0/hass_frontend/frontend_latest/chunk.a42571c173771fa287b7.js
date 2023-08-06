(self.webpackJsonp=self.webpackJsonp||[]).push([[91],{118:function(e,t,a){"use strict";a.d(t,"a",function(){return o});var i=a(9),s=a(18);const o=Object(i.a)(e=>(class extends e{fire(e,t,a){return a=a||{},Object(s.a)(a.node||this,e,t,a)}}))},175:function(e,t,a){"use strict";var i=a(9);t.a=Object(i.a)(e=>(class extends e{static get properties(){return{hass:Object,localize:{type:Function,computed:"__computeLocalize(hass.localize)"}}}__computeLocalize(e){return e}}))},176:function(e,t,a){"use strict";a.d(t,"a",function(){return s});var i=a(190);const s=e=>void 0===e.attributes.friendly_name?Object(i.a)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||""},177:function(e,t,a){"use strict";var i=a(3),s=a(0);class o extends s.a{static get styles(){return s.c`
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
    `}render(){return s.f`
      ${this.header?s.f`
            <div class="card-header">${this.header}</div>
          `:s.f``}
      <slot></slot>
    `}}Object(i.c)([Object(s.g)()],o.prototype,"header",void 0),customElements.define("ha-card",o)},178:function(e,t,a){"use strict";a.d(t,"a",function(){return o});var i=a(120);const s={alert:"hass:alert",alexa:"hass:amazon-alexa",automation:"hass:playlist-play",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",device_tracker:"hass:account",fan:"hass:fan",google_assistant:"hass:google-assistant",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",persistent_notification:"hass:bell",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:google-pages",script:"hass:file-document",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weather:"hass:weather-cloudy",weblink:"hass:open-in-new",zone:"hass:map-marker"},o=(e,t)=>{if(e in s)return s[e];switch(e){case"alarm_control_panel":switch(t){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell"}case"binary_sensor":return t&&"off"===t?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===t?"hass:window-closed":"hass:window-open";case"lock":return t&&"unlocked"===t?"hass:lock-open":"hass:lock";case"media_player":return t&&"off"!==t&&"idle"!==t?"hass:cast-connected":"hass:cast";case"zwave":switch(t){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave"}default:return console.warn("Unable to find icon for domain "+e+" ("+t+")"),i.a}}},179:function(e,t,a){"use strict";a.d(t,"a",function(){return o});a(109);const i=customElements.get("iron-icon");let s=!1;class o extends i{listen(e,t,i){super.listen(e,t,i),s||"mdi"!==this._iconsetName||(s=!0,a.e(75).then(a.bind(null,214)))}}customElements.define("ha-icon",o)},181:function(e,t,a){"use strict";a.d(t,"a",function(){return s});var i=a(121);const s=e=>Object(i.a)(e.entity_id)},185:function(e,t,a){"use strict";var i=a(3),s=a(0),o=(a(179),a(181)),n=a(194);class r extends s.a{render(){const e=this.stateObj;return e?s.f`
      <ha-icon
        id="icon"
        data-domain=${Object(o.a)(e)}
        data-state=${e.state}
        .icon=${this.overrideIcon||Object(n.a)(e)}
      ></ha-icon>
    `:s.f``}updated(e){if(!e.has("stateObj")||!this.stateObj)return;const t=this.stateObj,a={color:"",filter:""},i={backgroundImage:""};if(t)if(t.attributes.entity_picture&&!this.overrideIcon||this.overrideImage){let e=this.overrideImage||t.attributes.entity_picture;this.hass&&(e=this.hass.hassUrl(e)),i.backgroundImage=`url(${e})`,a.display="none"}else{if(t.attributes.hs_color){const e=t.attributes.hs_color[0],i=t.attributes.hs_color[1];i>10&&(a.color=`hsl(${e}, 100%, ${100-i/2}%)`)}if(t.attributes.brightness){const e=t.attributes.brightness;if("number"!=typeof e){const a=`Type error: state-badge expected number, but type of ${t.entity_id}.attributes.brightness is ${typeof e} (${e})`;console.warn(a)}a.filter=`brightness(${(e+245)/5}%)`}}Object.assign(this._icon.style,a),Object.assign(this.style,i)}static get styles(){return s.c`
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
    `}}Object(i.c)([Object(s.g)()],r.prototype,"stateObj",void 0),Object(i.c)([Object(s.g)()],r.prototype,"overrideIcon",void 0),Object(i.c)([Object(s.g)()],r.prototype,"overrideImage",void 0),Object(i.c)([Object(s.h)("ha-icon")],r.prototype,"_icon",void 0),customElements.define("state-badge",r)},190:function(e,t,a){"use strict";a.d(t,"a",function(){return i});const i=e=>e.substr(e.indexOf(".")+1)},194:function(e,t,a){"use strict";var i=a(120);var s=a(121),o=a(178);const n={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge",power:"hass:flash",signal_strength:"hass:wifi"};a.d(t,"a",function(){return c});const r={binary_sensor:e=>{const t=e.state&&"off"===e.state;switch(e.attributes.device_class){case"battery":return t?"hass:battery":"hass:battery-outline";case"cold":return t?"hass:thermometer":"hass:snowflake";case"connectivity":return t?"hass:server-network-off":"hass:server-network";case"door":return t?"hass:door-closed":"hass:door-open";case"garage_door":return t?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return t?"hass:shield-check":"hass:alert";case"heat":return t?"hass:thermometer":"hass:fire";case"light":return t?"hass:brightness-5":"hass:brightness-7";case"lock":return t?"hass:lock":"hass:lock-open";case"moisture":return t?"hass:water-off":"hass:water";case"motion":return t?"hass:walk":"hass:run";case"occupancy":return t?"hass:home-outline":"hass:home";case"opening":return t?"hass:square":"hass:square-outline";case"plug":return t?"hass:power-plug-off":"hass:power-plug";case"presence":return t?"hass:home-outline":"hass:home";case"sound":return t?"hass:music-note-off":"hass:music-note";case"vibration":return t?"hass:crop-portrait":"hass:vibrate";case"window":return t?"hass:window-closed":"hass:window-open";default:return t?"hass:radiobox-blank":"hass:checkbox-marked-circle"}},cover:e=>{const t="closed"!==e.state;switch(e.attributes.device_class){case"garage":return t?"hass:garage-open":"hass:garage";case"door":return t?"hass:door-open":"hass:door-closed";case"shutter":return t?"hass:window-shutter-open":"hass:window-shutter";case"blind":return t?"hass:blinds-open":"hass:blinds";case"window":return t?"hass:window-open":"hass:window-closed";default:return Object(o.a)("cover",e.state)}},sensor:e=>{const t=e.attributes.device_class;if(t&&t in n)return n[t];if("battery"===t){const t=Number(e.state);if(isNaN(t))return"hass:battery-unknown";const a=10*Math.round(t/10);return a>=100?"hass:battery":a<=0?"hass:battery-alert":`hass:battery-${a}`}const a=e.attributes.unit_of_measurement;return a===i.j||a===i.k?"hass:thermometer":Object(o.a)("sensor")},input_datetime:e=>e.attributes.has_date?e.attributes.has_time?Object(o.a)("input_datetime"):"hass:calendar":"hass:clock"},c=e=>{if(!e)return i.a;if(e.attributes.icon)return e.attributes.icon;const t=Object(s.a)(e.entity_id);return t in r?r[t](e):Object(o.a)(t,e.state)}},196:function(e,t,a){"use strict";a.d(t,"a",function(){return i});const i=(e,t,a=!1)=>{let i;return function(...s){const o=this,n=a&&!i;clearTimeout(i),i=setTimeout(()=>{i=null,a||e.apply(o,s)},t),n&&e.apply(o,s)}}},198:function(e,t,a){"use strict";var i=a(4),s=a(30);a(95);customElements.define("ha-config-section",class extends s.a{static get template(){return i.a`
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
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},203:function(e,t,a){"use strict";a.d(t,"b",function(){return i}),a.d(t,"a",function(){return s});const i=(e,t)=>e<t?-1:e>t?1:0,s=(e,t)=>i(e.toLowerCase(),t.toLowerCase())},225:function(e,t,a){"use strict";a.d(t,"b",function(){return o}),a.d(t,"a",function(){return c});var i=a(13),s=a(196);const o=(e,t,a)=>e.callWS(Object.assign({type:"config/device_registry/update",device_id:t},a)),n=e=>e.sendMessagePromise({type:"config/device_registry/list"}),r=(e,t)=>e.subscribeEvents(Object(s.a)(()=>n(e).then(e=>t.setState(e,!0)),500,!0),"device_registry_updated"),c=(e,t)=>Object(i.d)("_dr",n,r,e,t)},235:function(e,t,a){"use strict";a.d(t,"a",function(){return n}),a.d(t,"d",function(){return r}),a.d(t,"b",function(){return c}),a.d(t,"c",function(){return h});var i=a(13),s=a(203),o=a(196);const n=(e,t)=>e.callWS(Object.assign({type:"config/area_registry/create"},t)),r=(e,t,a)=>e.callWS(Object.assign({type:"config/area_registry/update",area_id:t},a)),c=(e,t)=>e.callWS({type:"config/area_registry/delete",area_id:t}),d=e=>e.sendMessagePromise({type:"config/area_registry/list"}).then(e=>e.sort((e,t)=>Object(s.b)(e.name,t.name))),l=(e,t)=>e.subscribeEvents(Object(o.a)(()=>d(e).then(e=>t.setState(e,!0)),500,!0),"area_registry_updated"),h=(e,t)=>Object(i.d)("_areaRegistry",d,l,e,t)},237:function(e,t,a){"use strict";var i=a(3),s=a(14),o=a(74);a(249);const n=customElements.get("mwc-fab");let r=class extends n{render(){const e={"mdc-fab--mini":this.mini,"mdc-fab--exited":this.exited,"mdc-fab--extended":this.extended},t=""!==this.label&&this.extended;return s.g`
      <button
        .ripple="${Object(o.a)()}"
        class="mdc-fab ${Object(s.d)(e)}"
        ?disabled="${this.disabled}"
        aria-label="${this.label||this.icon}"
      >
        ${t&&this.showIconAtEnd?this.label:""}
        ${this.icon?s.g`
              <ha-icon .icon=${this.icon}></ha-icon>
            `:""}
        ${t&&!this.showIconAtEnd?this.label:""}
      </button>
    `}};r=Object(i.c)([Object(s.f)("ha-fab")],r)},258:function(e,t,a){"use strict";a.d(t,"a",function(){return n}),a.d(t,"d",function(){return r}),a.d(t,"b",function(){return c}),a.d(t,"c",function(){return h});var i=a(13),s=a(176),o=a(196);const n=(e,t)=>{if(t.name)return t.name;const a=e.states[t.entity_id];return a?Object(s.a)(a):null},r=(e,t,a)=>e.callWS(Object.assign({type:"config/entity_registry/update",entity_id:t},a)),c=(e,t)=>e.callWS({type:"config/entity_registry/remove",entity_id:t}),d=e=>e.sendMessagePromise({type:"config/entity_registry/list"}),l=(e,t)=>e.subscribeEvents(Object(o.a)(()=>d(e).then(e=>t.setState(e,!0)),500,!0),"entity_registry_updated"),h=(e,t)=>Object(i.d)("_entityRegistry",d,l,e,t)},261:function(e,t,a){"use strict";a(109);var i=a(179);customElements.define("ha-icon-next",class extends i.a{connectedCallback(){super.connectedCallback(),setTimeout(()=>{this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left"},100)}})},289:function(e,t,a){"use strict";var i=a(3),s=a(11),o=a(0),n=a(18);a(109),a(93),a(108),a(85);let r=class extends o.a{render(){return s.g`
      <div class="search-container">
        <paper-input
          autofocus
          label="Search"
          .value=${this.filter}
          @value-changed=${this._filterInputChanged}
        >
          <iron-icon
            icon="hass:magnify"
            slot="prefix"
            class="prefix"
          ></iron-icon>
          ${this.filter&&s.g`
              <paper-icon-button
                slot="suffix"
                class="suffix"
                @click=${this._clearSearch}
                icon="hass:close"
                alt="Clear"
                title="Clear"
              ></paper-icon-button>
            `}
        </paper-input>
      </div>
    `}async _filterChanged(e){Object(n.a)(this,"value-changed",{value:String(e)})}async _filterInputChanged(e){this._filterChanged(e.target.value)}async _clearSearch(){this._filterChanged("")}static get styles(){return o.c`
      paper-input {
        flex: 1 1 auto;
        margin: 0 16px;
      }
      .search-container {
        display: inline-flex;
        width: 100%;
        align-items: center;
      }
      .prefix {
        margin: 8px;
      }
    `}};Object(i.c)([Object(o.g)()],r.prototype,"filter",void 0),r=Object(i.c)([Object(o.d)("search-input")],r)},298:function(e,t,a){"use strict";a.d(t,"a",function(){return i}),a.d(t,"b",function(){return s});const i=e=>{requestAnimationFrame(()=>setTimeout(e,0))},s=()=>new Promise(e=>{i(e)})},316:function(e,t,a){"use strict";a.d(t,"b",function(){return i}),a.d(t,"a",function(){return s}),a.d(t,"c",function(){return o}),a.d(t,"d",function(){return n});const i=e=>e.callApi("GET","config/config_entries/entry"),s=(e,t)=>e.callApi("DELETE",`config/config_entries/entry/${t}`),o=(e,t)=>e.callWS({type:"config_entries/system_options/list",entry_id:t}),n=(e,t,a)=>e.callWS(Object.assign({type:"config_entries/system_options/update",entry_id:t},a))},317:function(e,t,a){var i=a(154),s=["filterSortData","filterData","sortData"];e.exports=function(){var e=new Worker(a.p+"507fef43a02a5f1dc496.worker.js",{name:"[hash].worker.js"});return i(e,s),e}},319:function(e,t,a){"use strict";var i=a(3),s=a(325),o=a(284),n=a(765),r=a(14),c=a(317),d=a.n(c),l=(a(179),a(289),a(0)),h=(a(408),a(378));const p=customElements.get("mwc-checkbox");let b=class extends p{firstUpdated(){super.firstUpdated(),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}static get styles(){return[h.a,l.c`
        .mdc-checkbox__native-control:enabled:not(:checked):not(:indeterminate)
          ~ .mdc-checkbox__background {
          border-color: rgba(var(--rgb-primary-text-color), 0.54);
        }
      `]}};b=Object(i.c)([Object(l.d)("ha-checkbox")],b);var u=a(18),g=a(298),f=a(196);let m=class extends r.a{constructor(){super(...arguments),this.columns={},this.data=[],this.selectable=!1,this.id="id",this.mdcFoundationClass=n.a,this._filterable=!1,this._headerChecked=!1,this._headerIndeterminate=!1,this._checkedRows=[],this._filter="",this._sortDirection=null,this._filteredData=[],this._sortColumns={},this.curRequest=0,this._debounceSearch=Object(f.a)(e=>{this._filter=e.detail.value},200,!1)}firstUpdated(){super.firstUpdated(),this._worker=d()()}updated(e){if(super.updated(e),e.has("columns")){this._filterable=Object.values(this.columns).some(e=>e.filterable);for(const t in this.columns)if(this.columns[t].direction){this._sortDirection=this.columns[t].direction,this._sortColumn=t;break}const e=Object(o.a)(this.columns);Object.values(e).forEach(e=>{delete e.title,delete e.type,delete e.template}),this._sortColumns=e}(e.has("data")||e.has("columns")||e.has("_filter")||e.has("_sortColumn")||e.has("_sortDirection"))&&this._filterData()}render(){return r.g`
      ${this._filterable?r.g`
            <search-input
              @value-changed=${this._handleSearchChange}
            ></search-input>
          `:""}
      <div class="mdc-data-table">
        <table class="mdc-data-table__table">
          <thead>
            <tr class="mdc-data-table__header-row">
              ${this.selectable?r.g`
                    <th
                      class="mdc-data-table__header-cell mdc-data-table__header-cell--checkbox"
                      role="columnheader"
                      scope="col"
                    >
                      <ha-checkbox
                        id="header-checkbox"
                        class="mdc-data-table__row-checkbox"
                        @change=${this._handleHeaderRowCheckboxChange}
                        .indeterminate=${this._headerIndeterminate}
                        .checked=${this._headerChecked}
                      >
                      </ha-checkbox>
                    </th>
                  `:""}
              ${Object.entries(this.columns).map(e=>{const[t,a]=e,i=t===this._sortColumn,s={"mdc-data-table__header-cell--numeric":Boolean(a.type&&"numeric"===a.type),"mdc-data-table__header-cell--icon":Boolean(a.type&&"icon"===a.type),sortable:Boolean(a.sortable),"not-sorted":Boolean(a.sortable&&!i)};return r.g`
                  <th
                    class="mdc-data-table__header-cell ${Object(r.d)(s)}"
                    role="columnheader"
                    scope="col"
                    @click=${this._handleHeaderClick}
                    data-column-id="${t}"
                  >
                    ${a.sortable?r.g`
                          <ha-icon
                            .icon=${i&&"desc"===this._sortDirection?"hass:arrow-down":"hass:arrow-up"}
                          ></ha-icon>
                        `:""}
                    <span>${a.title}</span>
                  </th>
                `})}
            </tr>
          </thead>
          <tbody class="mdc-data-table__content">
            ${Object(s.a)(this._filteredData,e=>e[this.id],e=>r.g`
                <tr
                  data-row-id="${e[this.id]}"
                  @click=${this._handleRowClick}
                  class="mdc-data-table__row"
                >
                  ${this.selectable?r.g`
                        <td
                          class="mdc-data-table__cell mdc-data-table__cell--checkbox"
                        >
                          <ha-checkbox
                            class="mdc-data-table__row-checkbox"
                            @change=${this._handleRowCheckboxChange}
                            .checked=${this._checkedRows.includes(e[this.id])}
                          >
                          </ha-checkbox>
                        </td>
                      `:""}
                  ${Object.entries(this.columns).map(t=>{const[a,i]=t;return r.g`
                      <td
                        class="mdc-data-table__cell ${Object(r.d)({"mdc-data-table__cell--numeric":Boolean(i.type&&"numeric"===i.type),"mdc-data-table__cell--icon":Boolean(i.type&&"icon"===i.type)})}"
                      >
                        ${i.template?i.template(e[a],e):e[a]}
                      </td>
                    `})}
                </tr>
              `)}
          </tbody>
        </table>
      </div>
    `}createAdapter(){return{addClassAtRowIndex:(e,t)=>{this.rowElements[e].classList.add(t)},getRowCount:()=>this.data.length,getRowElements:()=>this.rowElements,getRowIdAtIndex:e=>this._getRowIdAtIndex(e),getRowIndexByChildElement:e=>Array.prototype.indexOf.call(this.rowElements,e.closest("tr")),getSelectedRowCount:()=>this._checkedRows.length,isCheckboxAtRowIndexChecked:e=>this._checkedRows.includes(this._getRowIdAtIndex(e)),isHeaderRowCheckboxChecked:()=>this._headerChecked,isRowsSelectable:()=>!0,notifyRowSelectionChanged:()=>void 0,notifySelectedAll:()=>void 0,notifyUnselectedAll:()=>void 0,registerHeaderRowCheckbox:()=>void 0,registerRowCheckboxes:()=>void 0,removeClassAtRowIndex:(e,t)=>{this.rowElements[e].classList.remove(t)},setAttributeAtRowIndex:(e,t,a)=>{this.rowElements[e].setAttribute(t,a)},setHeaderRowCheckboxChecked:e=>{this._headerChecked=e},setHeaderRowCheckboxIndeterminate:e=>{this._headerIndeterminate=e},setRowCheckboxCheckedAtIndex:(e,t)=>{this._setRowChecked(this._getRowIdAtIndex(e),t)}}}async _filterData(){const e=(new Date).getTime();this.curRequest++;const t=this.curRequest,a=this._worker.filterSortData(this.data,this._sortColumns,this._filter,this._sortDirection,this._sortColumn),[i]=await Promise.all([a,g.b]),s=(new Date).getTime()-e;s<100&&await new Promise(e=>setTimeout(e,100-s)),this.curRequest===t&&(this._filteredData=i)}_getRowIdAtIndex(e){return this.rowElements[e].getAttribute("data-row-id")}_handleHeaderClick(e){const t=e.target.closest("th").getAttribute("data-column-id");this.columns[t].sortable&&(this._sortDirection&&this._sortColumn===t?"asc"===this._sortDirection?this._sortDirection="desc":this._sortDirection=null:this._sortDirection="asc",this._sortColumn=null===this._sortDirection?void 0:t,Object(u.a)(this,"sorting-changed",{column:t,direction:this._sortDirection}))}_handleHeaderRowCheckboxChange(){this._headerChecked=this._headerCheckbox.checked,this._headerIndeterminate=this._headerCheckbox.indeterminate,this.mdcFoundation.handleHeaderRowCheckboxChange()}_handleRowCheckboxChange(e){const t=e.target,a=t.closest("tr").getAttribute("data-row-id");this._setRowChecked(a,t.checked),this.mdcFoundation.handleRowCheckboxChange(e)}_handleRowClick(e){const t=e.target.closest("tr").getAttribute("data-row-id");Object(u.a)(this,"row-click",{id:t},{bubbles:!1})}_setRowChecked(e,t){if(t&&!this._checkedRows.includes(e))this._checkedRows=[...this._checkedRows,e];else if(!t){const t=this._checkedRows.indexOf(e);-1!==t&&this._checkedRows.splice(t,1)}Object(u.a)(this,"selection-changed",{id:e,selected:t})}_handleSearchChange(e){this._debounceSearch(e)}static get styles(){return r.e`
      /* default mdc styles, colors changed, without checkbox styles */

      .mdc-data-table__content {
        font-family: Roboto, sans-serif;
        -moz-osx-font-smoothing: grayscale;
        -webkit-font-smoothing: antialiased;
        font-size: 0.875rem;
        line-height: 1.25rem;
        font-weight: 400;
        letter-spacing: 0.0178571429em;
        text-decoration: inherit;
        text-transform: inherit;
      }

      .mdc-data-table {
        background-color: var(--card-background-color);
        border-radius: 4px;
        border-width: 1px;
        border-style: solid;
        border-color: rgba(var(--rgb-primary-text-color), 0.12);
        display: inline-flex;
        flex-direction: column;
        box-sizing: border-box;
        overflow-x: auto;
      }

      .mdc-data-table__row--selected {
        background-color: rgba(var(--rgb-primary-color), 0.04);
      }

      .mdc-data-table__row {
        border-top-color: rgba(var(--rgb-primary-text-color), 0.12);
      }

      .mdc-data-table__row {
        border-top-width: 1px;
        border-top-style: solid;
      }

      .mdc-data-table__row:not(.mdc-data-table__row--selected):hover {
        background-color: rgba(var(--rgb-primary-text-color), 0.04);
      }

      .mdc-data-table__header-cell {
        color: var(--primary-text-color);
      }

      .mdc-data-table__cell {
        color: var(--primary-text-color);
      }

      .mdc-data-table__header-row {
        height: 56px;
      }

      .mdc-data-table__row {
        height: 52px;
      }

      .mdc-data-table__cell,
      .mdc-data-table__header-cell {
        padding-right: 16px;
        padding-left: 16px;
      }

      .mdc-data-table__header-cell--checkbox,
      .mdc-data-table__cell--checkbox {
        /* @noflip */
        padding-left: 16px;
        /* @noflip */
        padding-right: 0;
      }
      [dir="rtl"] .mdc-data-table__header-cell--checkbox,
      .mdc-data-table__header-cell--checkbox[dir="rtl"],
      [dir="rtl"] .mdc-data-table__cell--checkbox,
      .mdc-data-table__cell--checkbox[dir="rtl"] {
        /* @noflip */
        padding-left: 0;
        /* @noflip */
        padding-right: 16px;
      }

      .mdc-data-table__table {
        width: 100%;
        border: 0;
        white-space: nowrap;
        border-collapse: collapse;
      }

      .mdc-data-table__cell {
        font-family: Roboto, sans-serif;
        -moz-osx-font-smoothing: grayscale;
        -webkit-font-smoothing: antialiased;
        font-size: 0.875rem;
        line-height: 1.25rem;
        font-weight: 400;
        letter-spacing: 0.0178571429em;
        text-decoration: inherit;
        text-transform: inherit;
      }

      .mdc-data-table__cell--numeric {
        text-align: right;
      }
      [dir="rtl"] .mdc-data-table__cell--numeric,
      .mdc-data-table__cell--numeric[dir="rtl"] {
        /* @noflip */
        text-align: left;
      }

      .mdc-data-table__cell--icon {
        color: var(--secondary-text-color);
        text-align: center;
      }

      .mdc-data-table__header-cell {
        font-family: Roboto, sans-serif;
        -moz-osx-font-smoothing: grayscale;
        -webkit-font-smoothing: antialiased;
        font-size: 0.875rem;
        line-height: 1.375rem;
        font-weight: 500;
        letter-spacing: 0.0071428571em;
        text-decoration: inherit;
        text-transform: inherit;
        text-align: left;
      }
      [dir="rtl"] .mdc-data-table__header-cell,
      .mdc-data-table__header-cell[dir="rtl"] {
        /* @noflip */
        text-align: right;
      }

      .mdc-data-table__header-cell--numeric {
        text-align: right;
      }
      [dir="rtl"] .mdc-data-table__header-cell--numeric,
      .mdc-data-table__header-cell--numeric[dir="rtl"] {
        /* @noflip */
        text-align: left;
      }

      .mdc-data-table__header-cell--icon {
        text-align: center;
      }

      /* custom from here */

      .mdc-data-table {
        display: block;
      }
      .mdc-data-table__header-cell {
        overflow: hidden;
      }
      .mdc-data-table__header-cell.sortable {
        cursor: pointer;
      }
      .mdc-data-table__header-cell.not-sorted:not(.mdc-data-table__header-cell--numeric):not(.mdc-data-table__header-cell--icon)
        span {
        position: relative;
        left: -24px;
      }
      .mdc-data-table__header-cell.not-sorted > * {
        transition: left 0.2s ease 0s;
      }
      .mdc-data-table__header-cell.not-sorted ha-icon {
        left: -36px;
      }
      .mdc-data-table__header-cell.not-sorted:not(.mdc-data-table__header-cell--numeric):not(.mdc-data-table__header-cell--icon):hover
        span {
        left: 0px;
      }
      .mdc-data-table__header-cell:hover.not-sorted ha-icon {
        left: 0px;
      }
    `}};Object(i.c)([Object(r.i)({type:Object})],m.prototype,"columns",void 0),Object(i.c)([Object(r.i)({type:Array})],m.prototype,"data",void 0),Object(i.c)([Object(r.i)({type:Boolean})],m.prototype,"selectable",void 0),Object(i.c)([Object(r.i)({type:String})],m.prototype,"id",void 0),Object(i.c)([Object(r.j)(".mdc-data-table")],m.prototype,"mdcRoot",void 0),Object(i.c)([Object(r.k)(".mdc-data-table__row")],m.prototype,"rowElements",void 0),Object(i.c)([Object(r.j)("#header-checkbox")],m.prototype,"_headerCheckbox",void 0),Object(i.c)([Object(r.i)({type:Boolean})],m.prototype,"_filterable",void 0),Object(i.c)([Object(r.i)({type:Boolean})],m.prototype,"_headerChecked",void 0),Object(i.c)([Object(r.i)({type:Boolean})],m.prototype,"_headerIndeterminate",void 0),Object(i.c)([Object(r.i)({type:Array})],m.prototype,"_checkedRows",void 0),Object(i.c)([Object(r.i)({type:String})],m.prototype,"_filter",void 0),Object(i.c)([Object(r.i)({type:String})],m.prototype,"_sortColumn",void 0),Object(i.c)([Object(r.i)({type:String})],m.prototype,"_sortDirection",void 0),Object(i.c)([Object(r.i)({type:Array})],m.prototype,"_filteredData",void 0),m=Object(i.c)([Object(r.f)("ha-data-table")],m)},327:function(e,t,a){"use strict";a.d(t,"a",function(){return o}),a.d(t,"c",function(){return n}),a.d(t,"f",function(){return r}),a.d(t,"b",function(){return c}),a.d(t,"d",function(){return d}),a.d(t,"e",function(){return p}),a.d(t,"h",function(){return b}),a.d(t,"g",function(){return u});var i=a(196),s=a(13);const o=(e,t)=>e.callApi("POST","config/config_entries/flow",{handler:t}),n=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`),r=(e,t,a)=>e.callApi("POST",`config/config_entries/flow/${t}`,a),c=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),d=e=>e.callApi("GET","config/config_entries/flow_handlers"),l=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),h=(e,t)=>e.subscribeEvents(Object(i.a)(()=>l(e).then(e=>t.setState(e,!0)),500,!0),"config_entry_discovered"),p=e=>Object(s.h)(e,"_configFlowProgress",l,h),b=(e,t)=>p(e.connection).subscribe(t),u=(e,t)=>{const a=t.context.title_placeholders||{},i=Object.keys(a);if(0===i.length)return e(`component.${t.handler}.config.title`);const s=[];return i.forEach(e=>{s.push(e),s.push(a[e])}),e(`component.${t.handler}.config.flow_title`,...s)}},402:function(e,t,a){"use strict";a.d(t,"a",function(){return s}),a.d(t,"b",function(){return o});var i=a(18);const s=()=>Promise.all([a.e(1),a.e(4),a.e(6),a.e(11),a.e(31)]).then(a.bind(null,505)),o=(e,t,a)=>{Object(i.a)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:s,dialogParams:Object.assign(Object.assign({},t),{flowConfig:a})})}},405:function(e,t,a){"use strict";var i=a(4),s=a(30),o=(a(179),a(194));customElements.define("ha-state-icon",class extends s.a{static get template(){return i.a`
      <ha-icon icon="[[computeIcon(stateObj)]]"></ha-icon>
    `}static get properties(){return{stateObj:{type:Object}}}computeIcon(e){return Object(o.a)(e)}})},447:function(e,t,a){"use strict";a.d(t,"a",function(){return c}),a.d(t,"b",function(){return d});var i=a(327),s=a(0),o=a(58),n=a(402),r=a(203);const c=n.a,d=(e,t)=>Object(n.b)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:e=>Object(i.d)(e).then(t=>t.sort((t,a)=>Object(r.a)(e.localize(`component.${t}.config.title`),e.localize(`component.${a}.config.title`)))),createFlow:i.a,fetchFlow:i.c,handleFlowStep:i.f,deleteFlow:i.b,renderAbortDescription(e,t){const a=Object(o.b)(e.localize,`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return a?s.f`
            <ha-markdown allowsvg .content=${a}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`),renderShowFormStepDescription(e,t){const a=Object(o.b)(e.localize,`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return a?s.f`
            <ha-markdown allowsvg .content=${a}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,a)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${a.name}`),renderShowFormStepFieldError:(e,t,a)=>e.localize(`component.${t.handler}.config.error.${a}`),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`),renderExternalStepDescription(e,t){const a=Object(o.b)(e.localize,`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return s.f`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${a?s.f`
              <ha-markdown allowsvg .content=${a}></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const a=Object(o.b)(e.localize,`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return s.f`
        ${a?s.f`
              <ha-markdown allowsvg .content=${a}></ha-markdown>
            `:""}
        <p>Created config for ${t.title}.</p>
      `}})},452:function(e,t,a){"use strict";var i=a(3),s=(a(319),a(405),a(123)),o=a(0),n=a(99),r=a(176);let c=class extends o.a{constructor(){super(...arguments),this.narrow=!1,this._devices=Object(s.a)((e,t,a,i,s,o)=>{let n=e;const r={};for(const h of e)r[h.id]=h;const c={};for(const h of a)h.device_id&&(h.device_id in c||(c[h.device_id]=[]),c[h.device_id].push(h));const d={};for(const h of t)d[h.entry_id]=h;const l={};for(const h of i)l[h.area_id]=h;return s&&(n=n.filter(e=>e.config_entries.find(e=>e in d&&d[e].domain===s))),n=n.map(e=>Object.assign(Object.assign({},e),{name:e.name_by_user||e.name||this._fallbackDeviceName(e.id,c)||"No name",model:e.model||"<unknown>",manufacturer:e.manufacturer||"<unknown>",area:e.area_id?l[e.area_id].name:"No area",integration:e.config_entries.length?e.config_entries.filter(e=>e in d).map(e=>o(`component.${d[e].domain}.config.title`)||d[e].domain).join(", "):"No integration",battery_entity:this._batteryEntity(e.id,c)}))}),this._columns=Object(s.a)(e=>e?{name:{title:"Device",sortable:!0,filterKey:"name",filterable:!0,direction:"asc",template:(e,t)=>{const a=t.battery_entity?this.hass.states[t.battery_entity]:void 0;return o.f`
                  ${e}<br />
                  ${t.area} | ${t.integration}<br />
                  ${a?o.f`
                        ${a.state}%
                        <ha-state-icon
                          .hass=${this.hass}
                          .stateObj=${a}
                        ></ha-state-icon>
                      `:""}
                `}}}:{name:{title:"Device",sortable:!0,filterable:!0,direction:"asc"},manufacturer:{title:"Manufacturer",sortable:!0,filterable:!0},model:{title:"Model",sortable:!0,filterable:!0},area:{title:"Area",sortable:!0,filterable:!0},integration:{title:"Integration",sortable:!0,filterable:!0},battery_entity:{title:"Battery",sortable:!0,type:"numeric",template:e=>{const t=e?this.hass.states[e]:void 0;return t?o.f`
                      ${t.state}%
                      <ha-state-icon
                        .hass=${this.hass}
                        .stateObj=${t}
                      ></ha-state-icon>
                    `:o.f`
                      -
                    `}}})}render(){return o.f`
      <ha-data-table
        .columns=${this._columns(this.narrow)}
        .data=${this._devices(this.devices,this.entries,this.entities,this.areas,this.domain,this.hass.localize)}
        @row-click=${this._handleRowClicked}
      ></ha-data-table>
    `}_batteryEntity(e,t){const a=(t[e]||[]).find(e=>this.hass.states[e.entity_id]&&"battery"===this.hass.states[e.entity_id].attributes.device_class);return a?a.entity_id:void 0}_fallbackDeviceName(e,t){for(const a of t[e]||[]){const e=this.hass.states[a.entity_id];if(e)return Object(r.a)(e)}}_handleRowClicked(e){const t=e.detail.id;Object(n.a)(this,`/config/devices/device/${t}`)}};Object(i.c)([Object(o.g)()],c.prototype,"hass",void 0),Object(i.c)([Object(o.g)()],c.prototype,"narrow",void 0),Object(i.c)([Object(o.g)()],c.prototype,"devices",void 0),Object(i.c)([Object(o.g)()],c.prototype,"entries",void 0),Object(i.c)([Object(o.g)()],c.prototype,"entities",void 0),Object(i.c)([Object(o.g)()],c.prototype,"areas",void 0),Object(i.c)([Object(o.g)()],c.prototype,"domain",void 0),c=Object(i.c)([Object(o.d)("ha-devices-data-table")],c)},738:function(e,t,a){"use strict";a.r(t);var i=a(3),s=(a(244),a(0)),o=(a(182),a(276),a(85),a(109),a(143),a(180),a(177),a(261),a(237),a(405),a(152),a(95),a(179),a(96)),n=(a(198),a(176)),r=a(447),c=a(327),d=a(18);let l=class extends s.a{connectedCallback(){super.connectedCallback(),Object(r.a)()}render(){return s.f`
      <hass-subpage
        header=${this.hass.localize("ui.panel.config.integrations.caption")}
      >
        ${this.configEntriesInProgress.length?s.f`
              <ha-config-section>
                <span slot="header"
                  >${this.hass.localize("ui.panel.config.integrations.discovered")}</span
                >
                <ha-card>
                  ${this.configEntriesInProgress.map(e=>s.f`
                      <div class="config-entry-row">
                        <paper-item-body>
                          ${Object(c.g)(this.hass.localize,e)}
                        </paper-item-body>
                        <mwc-button
                          @click=${this._continueFlow}
                          data-id="${e.flow_id}"
                          >${this.hass.localize("ui.panel.config.integrations.configure")}</mwc-button
                        >
                      </div>
                    `)}
                </ha-card>
              </ha-config-section>
            `:""}

        <ha-config-section class="configured">
          <span slot="header"
            >${this.hass.localize("ui.panel.config.integrations.configured")}</span
          >
          <ha-card>
            ${this.entityRegistryEntries.length?this.configEntries.map((e,t)=>s.f`
                    <a
                      href="/config/integrations/config_entry/${e.entry_id}"
                    >
                      <paper-item data-index=${t}>
                        <paper-item-body two-line>
                          <div>
                            ${this.hass.localize(`component.${e.domain}.config.title`)}:
                            ${e.title}
                          </div>
                          <div secondary>
                            ${this._getEntities(e).map(e=>s.f`
                                <span>
                                  <ha-state-icon
                                    .stateObj=${e}
                                  ></ha-state-icon>
                                  <paper-tooltip position="bottom"
                                    >${Object(n.a)(e)}</paper-tooltip
                                  >
                                </span>
                              `)}
                          </div>
                        </paper-item-body>
                        <ha-icon-next></ha-icon-next>
                      </paper-item>
                    </a>
                  `):s.f`
                  <div class="config-entry-row">
                    <paper-item-body two-line>
                      <div>
                        ${this.hass.localize("ui.panel.config.integrations.none")}
                      </div>
                    </paper-item-body>
                  </div>
                `}
          </ha-card>
        </ha-config-section>

        <ha-fab
          icon="hass:plus"
          title=${this.hass.localize("ui.panel.config.integrations.new")}
          @click=${this._createFlow}
          ?rtl=${Object(o.a)(this.hass)}
        ></ha-fab>
      </hass-subpage>
    `}_createFlow(){Object(r.b)(this,{dialogClosedCallback:()=>Object(d.a)(this,"hass-reload-entries")})}_continueFlow(e){Object(r.b)(this,{continueFlowId:e.target.getAttribute("data-id")||void 0,dialogClosedCallback:()=>Object(d.a)(this,"hass-reload-entries")})}_getEntities(e){if(!this.entityRegistryEntries)return[];const t=[];return this.entityRegistryEntries.forEach(a=>{a.config_entry_id===e.entry_id&&a.entity_id in this.hass.states&&t.push(this.hass.states[a.entity_id])}),t}static get styles(){return s.c`
      ha-card {
        overflow: hidden;
      }
      mwc-button {
        top: 3px;
        margin-right: -0.57em;
      }
      .config-entry-row {
        display: flex;
        padding: 0 16px;
      }
      ha-icon {
        cursor: pointer;
        margin: 8px;
      }
      .configured a {
        color: var(--primary-text-color);
        text-decoration: none;
      }
      ha-fab {
        position: fixed;
        bottom: 16px;
        right: 16px;
        z-index: 1;
      }

      ha-fab[rtl] {
        right: auto;
        left: 16px;
      }
    `}};Object(i.c)([Object(s.g)()],l.prototype,"hass",void 0),Object(i.c)([Object(s.g)()],l.prototype,"configEntries",void 0),Object(i.c)([Object(s.g)()],l.prototype,"entityRegistryEntries",void 0),Object(i.c)([Object(s.g)()],l.prototype,"configEntriesInProgress",void 0),l=Object(i.c)([Object(s.d)("ha-config-entries-dashboard")],l);var h=a(123),p=(a(161),a(452),a(184),a(4)),b=a(30),u=a(118),g=a(175),f=(a(185),a(258));customElements.define("ha-ce-entities-card",class extends(Object(g.a)(Object(u.a)(b.a))){static get template(){return p.a`
      <style>
        ha-card {
          margin-top: 8px;
          padding-bottom: 8px;
        }
        paper-icon-item {
          cursor: pointer;
          padding-top: 4px;
          padding-bottom: 4px;
        }
      </style>
      <ha-card header="[[heading]]">
        <template is="dom-repeat" items="[[entities]]" as="entity">
          <paper-icon-item on-click="_openMoreInfo">
            <state-badge
              state-obj="[[_computeStateObj(entity, hass)]]"
              slot="item-icon"
            ></state-badge>
            <paper-item-body>
              <div class="name">[[_computeEntityName(entity, hass)]]</div>
              <div class="secondary entity-id">[[entity.entity_id]]</div>
            </paper-item-body>
          </paper-icon-item>
        </template>
      </ha-card>
    `}static get properties(){return{heading:String,entities:Array,hass:Object}}_computeStateObj(e,t){return t.states[e.entity_id]}_computeEntityName(e,t){return Object(f.a)(t,e)||`(${this.localize("ui.panel.config.integrations.config_entry.entity_unavailable")})`}_openMoreInfo(e){this.fire("hass-more-info",{entityId:e.model.entity.entity_id})}});const m=(e,t)=>e.callApi("POST","config/config_entries/options/flow",{handler:t}),_=(e,t)=>e.callApi("GET",`config/config_entries/options/flow/${t}`),y=(e,t,a)=>e.callApi("POST",`config/config_entries/options/flow/${t}`,a),w=(e,t)=>e.callApi("DELETE",`config/config_entries/options/flow/${t}`);var v=a(58),O=a(402);O.a;const j=(e,t)=>Object(O.b)(e,{startFlowHandler:t.entry_id},{loadDevicesAndAreas:!1,createFlow:m,fetchFlow:_,handleFlowStep:y,deleteFlow:w,renderAbortDescription(e,a){const i=Object(v.b)(e.localize,`component.${t.domain}.options.abort.${a.reason}`,a.description_placeholders);return i?s.f`
              <ha-markdown allowsvg .content=${i}></ha-markdown>
            `:""},renderShowFormStepHeader:(e,t)=>e.localize("ui.dialogs.options_flow.form.header"),renderShowFormStepDescription:(e,t)=>"",renderShowFormStepFieldLabel:(e,a,i)=>e.localize(`component.${t.domain}.options.step.${a.step_id}.data.${i.name}`),renderShowFormStepFieldError:(e,a,i)=>e.localize(`component.${t.domain}.options.error.${i}`),renderExternalStepHeader:(e,t)=>"",renderExternalStepDescription:(e,t)=>"",renderCreateEntryDescription:(e,t)=>s.f`
          <p>${e.localize("ui.dialogs.options_flow.success.description")}</p>
        `});var x=a(99),k=a(316);const $=()=>Promise.all([a.e(1),a.e(115),a.e(26)]).then(a.bind(null,724)),E=(e,t)=>{Object(d.a)(e,"show-dialog",{dialogTag:"dialog-config-entry-system-options",dialogImport:$,dialogParams:t})};class C extends s.a{constructor(){super(...arguments),this._computeConfigEntryDevices=Object(h.a)((e,t)=>t?t.filter(t=>t.config_entries.includes(e.entry_id)):[]),this._computeNoDeviceEntities=Object(h.a)((e,t)=>t?t.filter(t=>!t.device_id&&t.config_entry_id===e.entry_id):[])}get _configEntry(){return this.configEntries?this.configEntries.find(e=>e.entry_id===this.configEntryId):void 0}render(){const e=this._configEntry;if(!e)return s.f`
        <hass-error-screen error="Integration not found."></hass-error-screen>
      `;const t=this._computeConfigEntryDevices(e,this.deviceRegistryEntries),a=this._computeNoDeviceEntities(e,this.entityRegistryEntries);return s.f`
      <hass-subpage .header=${e.title}>
        ${e.supports_options?s.f`
              <paper-icon-button
                slot="toolbar-icon"
                icon="hass:settings"
                @click=${this._showSettings}
              ></paper-icon-button>
            `:""}
        <paper-icon-button
          slot="toolbar-icon"
          icon="hass:message-settings-variant"
          @click=${this._showSystemOptions}
        ></paper-icon-button>
        <paper-icon-button
          slot="toolbar-icon"
          icon="hass:delete"
          @click=${this._removeEntry}
        ></paper-icon-button>

        <div class="content">
          ${0===t.length&&0===a.length?s.f`
                <p>
                  ${this.hass.localize("ui.panel.config.integrations.config_entry.no_devices")}
                </p>
              `:s.f`
                <ha-devices-data-table
                  .hass=${this.hass}
                  .narrow=${this.narrow}
                  .devices=${t}
                  .entries=${this.configEntries}
                  .entities=${this.entityRegistryEntries}
                  .areas=${this.areas}
                ></ha-devices-data-table>
              `}
          ${a.length>0?s.f`
                <ha-ce-entities-card
                  .heading=${this.hass.localize("ui.panel.config.integrations.config_entry.no_device")}
                  .entities=${a}
                  .hass=${this.hass}
                  .narrow=${this.narrow}
                ></ha-ce-entities-card>
              `:""}
        </div>
      </hass-subpage>
    `}_showSettings(){j(this,this._configEntry)}_showSystemOptions(){E(this,{entry:this._configEntry})}_removeEntry(){confirm(this.hass.localize("ui.panel.config.integrations.config_entry.delete_confirm"))&&Object(k.a)(this.hass,this.configEntryId).then(e=>{Object(d.a)(this,"hass-reload-entries"),e.require_restart&&alert(this.hass.localize("ui.panel.config.integrations.config_entry.restart_confirm")),Object(x.a)(this,"/config/integrations/dashboard",!0)})}static get styles(){return s.c`
      .content {
        padding: 4px;
      }
      p {
        text-align: center;
      }
      ha-devices-data-table {
        width: 100%;
      }
    `}}Object(i.c)([Object(s.g)()],C.prototype,"hass",void 0),Object(i.c)([Object(s.g)()],C.prototype,"narrow",void 0),Object(i.c)([Object(s.g)()],C.prototype,"configEntryId",void 0),Object(i.c)([Object(s.g)()],C.prototype,"configEntries",void 0),Object(i.c)([Object(s.g)()],C.prototype,"entityRegistryEntries",void 0),Object(i.c)([Object(s.g)()],C.prototype,"deviceRegistryEntries",void 0),Object(i.c)([Object(s.g)()],C.prototype,"areas",void 0),customElements.define("ha-config-entry-page",C);var R=a(203),S=a(235),I=a(133),z=a(225);let D=class extends I.a{constructor(){super(...arguments),this.routerOptions={defaultPage:"dashboard",routes:{dashboard:{tag:"ha-config-entries-dashboard"},config_entry:{tag:"ha-config-entry-page"}}},this._configEntries=[],this._configEntriesInProgress=[],this._entityRegistryEntries=[],this._deviceRegistryEntries=[],this._areas=[]}connectedCallback(){super.connectedCallback(),this.hass&&this._loadData()}disconnectedCallback(){if(super.disconnectedCallback(),this._unsubs){for(;this._unsubs.length;)this._unsubs.pop()();this._unsubs=void 0}}firstUpdated(e){super.firstUpdated(e),this.addEventListener("hass-reload-entries",()=>{this._loadData(),Object(c.e)(this.hass.connection).refresh()})}updated(e){super.updated(e),!this._unsubs&&e.has("hass")&&this._loadData()}updatePageEl(e){e.hass=this.hass,e.entityRegistryEntries=this._entityRegistryEntries,e.configEntries=this._configEntries,"dashboard"!==this._currentPage?(e.configEntryId=this.routeTail.path.substr(1),e.deviceRegistryEntries=this._deviceRegistryEntries,e.areas=this._areas,e.narrow=this.narrow):e.configEntriesInProgress=this._configEntriesInProgress}_loadData(){Object(k.b)(this.hass).then(e=>{this._configEntries=e.sort((e,t)=>Object(R.b)(e.title,t.title))}),this._unsubs||(this._unsubs=[Object(S.c)(this.hass.connection,e=>{this._areas=e}),Object(f.c)(this.hass.connection,e=>{this._entityRegistryEntries=e}),Object(z.a)(this.hass.connection,e=>{this._deviceRegistryEntries=e}),Object(c.h)(this.hass,e=>{this._configEntriesInProgress=e})])}};Object(i.c)([Object(s.g)()],D.prototype,"hass",void 0),Object(i.c)([Object(s.g)()],D.prototype,"narrow",void 0),Object(i.c)([Object(s.g)()],D.prototype,"_configEntries",void 0),Object(i.c)([Object(s.g)()],D.prototype,"_configEntriesInProgress",void 0),Object(i.c)([Object(s.g)()],D.prototype,"_entityRegistryEntries",void 0),Object(i.c)([Object(s.g)()],D.prototype,"_deviceRegistryEntries",void 0),Object(i.c)([Object(s.g)()],D.prototype,"_areas",void 0),D=Object(i.c)([Object(s.d)("ha-config-integrations")],D)}}]);
//# sourceMappingURL=chunk.a42571c173771fa287b7.js.map