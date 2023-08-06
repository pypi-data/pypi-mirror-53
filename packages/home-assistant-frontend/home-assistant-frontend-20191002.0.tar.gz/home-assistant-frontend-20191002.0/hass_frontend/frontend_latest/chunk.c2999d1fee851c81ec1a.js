/*! For license information please see chunk.c2999d1fee851c81ec1a.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[62],{180:function(e,t,i){"use strict";i(5),i(45),i(42),i(54);var a=i(6),n=i(4);Object(a.a)({_template:n.a`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},184:function(e,t,i){"use strict";i(5),i(45),i(54),i(144);var a=i(6),n=i(4),o=i(119);Object(a.a)({_template:n.a`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[o.a]})},189:function(e,t,i){"use strict";var a=i(3),n=(i(108),i(93),i(184),i(180),i(207),i(123)),o=(i(185),i(176)),s=i(0),c=i(18);const l=(e,t,i)=>{e.firstElementChild||(e.innerHTML='\n      <style>\n        paper-icon-item {\n          margin: -10px;\n          padding: 0;\n        }\n      </style>\n      <paper-icon-item>\n        <state-badge state-obj="[[item]]" slot="item-icon"></state-badge>\n        <paper-item-body two-line="">\n          <div class=\'name\'>[[_computeStateName(item)]]</div>\n          <div secondary>[[item.entity_id]]</div>\n        </paper-item-body>\n      </paper-icon-item>\n    '),e.querySelector("state-badge").stateObj=i.item,e.querySelector(".name").textContent=Object(o.a)(i.item),e.querySelector("[secondary]").textContent=i.item.entity_id};class r extends s.a{constructor(){super(...arguments),this._getStates=Object(n.a)((e,t,i)=>{let a=[];if(!e)return[];let n=Object.keys(e.states);return t&&(n=n.filter(e=>e.substr(0,e.indexOf("."))===t)),a=n.sort().map(t=>e.states[t]),i&&(a=a.filter(e=>e.entity_id===this.value||i(e))),a})}updated(e){super.updated(e),e.has("hass")&&!this._opened&&(this._hass=this.hass)}render(){const e=this._getStates(this._hass,this.domainFilter,this.entityFilter);return s.f`
      <vaadin-combo-box-light
        item-value-path="entity_id"
        item-label-path="entity_id"
        .items=${e}
        .value=${this._value}
        .allowCustomValue=${this.allowCustomEntity}
        .renderer=${l}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._valueChanged}
      >
        <paper-input
          .autofocus=${this.autofocus}
          .label=${void 0===this.label&&this._hass?this._hass.localize("ui.components.entity.entity-picker.entity"):this.label}
          .value=${this._value}
          .disabled=${this.disabled}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          spellcheck="false"
        >
          ${this.value?s.f`
                <paper-icon-button
                  aria-label="Clear"
                  slot="suffix"
                  class="clear-button"
                  icon="hass:close"
                  no-ripple
                >
                  Clear
                </paper-icon-button>
              `:""}
          ${e.length>0?s.f`
                <paper-icon-button
                  aria-label="Show entities"
                  slot="suffix"
                  class="toggle-button"
                  .icon=${this._opened?"hass:menu-up":"hass:menu-down"}
                >
                  Toggle
                </paper-icon-button>
              `:""}
        </paper-input>
      </vaadin-combo-box-light>
    `}get _value(){return this.value||""}_openedChanged(e){this._opened=e.detail.value}_valueChanged(e){e.detail.value!==this._value&&(this.value=e.detail.value,setTimeout(()=>{Object(c.a)(this,"value-changed",{value:this.value}),Object(c.a)(this,"change")},0))}static get styles(){return s.c`
      paper-input > paper-icon-button {
        width: 24px;
        height: 24px;
        padding: 2px;
        color: var(--secondary-text-color);
      }
      [hidden] {
        display: none;
      }
    `}}Object(a.c)([Object(s.g)({type:Boolean})],r.prototype,"autofocus",void 0),Object(a.c)([Object(s.g)({type:Boolean})],r.prototype,"disabled",void 0),Object(a.c)([Object(s.g)({type:Boolean,attribute:"allow-custom-entity"})],r.prototype,"allowCustomEntity",void 0),Object(a.c)([Object(s.g)()],r.prototype,"hass",void 0),Object(a.c)([Object(s.g)()],r.prototype,"label",void 0),Object(a.c)([Object(s.g)()],r.prototype,"value",void 0),Object(a.c)([Object(s.g)({attribute:"domain-filter"})],r.prototype,"domainFilter",void 0),Object(a.c)([Object(s.g)()],r.prototype,"entityFilter",void 0),Object(a.c)([Object(s.g)({type:Boolean})],r.prototype,"_opened",void 0),Object(a.c)([Object(s.g)()],r.prototype,"_hass",void 0),customElements.define("ha-entity-picker",r)},192:function(e,t,i){"use strict";var a=i(203);i.d(t,"a",function(){return n});const n=Object(a.a)({types:{"entity-id":function(e){return"string"!=typeof e?"entity id should be a string":!!e.includes(".")||"entity id should be in the format 'domain.entity'"},icon:function(e){return"string"!=typeof e?"icon should be a string":!!e.includes(":")||"icon should be in the format 'mdi:icon'"}}})},200:function(e,t,i){"use strict";i.d(t,"a",function(){return a});const a=i(0).f`
  <style>
    ha-switch {
      padding: 16px 0;
    }
    .side-by-side {
      display: flex;
    }
    .side-by-side > * {
      flex: 1;
      padding-right: 4px;
    }
    .suffix {
      margin: 0 8px;
    }
  </style>
`},231:function(e,t,i){"use strict";var a=i(3),n=i(0),o=(i(108),i(18));i(189);let s=class extends n.a{render(){return this.entities?n.f`
      <h3>
        ${this.label||this.hass.localize("ui.panel.lovelace.editor.card.generic.entities")+" ("+this.hass.localize("ui.panel.lovelace.editor.card.config.required")+")"}
      </h3>
      <div class="entities">
        ${this.entities.map((e,t)=>n.f`
            <div class="entity">
              <ha-entity-picker
                .hass="${this.hass}"
                .value="${e.entity}"
                .index="${t}"
                @change="${this._valueChanged}"
                allow-custom-entity
              ></ha-entity-picker>
              <paper-icon-button
                title="Move entity down"
                icon="hass:arrow-down"
                .index="${t}"
                @click="${this._entityDown}"
                ?disabled="${t===this.entities.length-1}"
              ></paper-icon-button>
              <paper-icon-button
                title="Move entity up"
                icon="hass:arrow-up"
                .index="${t}"
                @click="${this._entityUp}"
                ?disabled="${0===t}"
              ></paper-icon-button>
            </div>
          `)}
        <ha-entity-picker
          .hass="${this.hass}"
          @change="${this._addEntity}"
        ></ha-entity-picker>
      </div>
    `:n.f``}_addEntity(e){const t=e.target;if(""===t.value)return;const i=this.entities.concat({entity:t.value});t.value="",Object(o.a)(this,"entities-changed",{entities:i})}_entityUp(e){const t=e.target,i=this.entities.concat();[i[t.index-1],i[t.index]]=[i[t.index],i[t.index-1]],Object(o.a)(this,"entities-changed",{entities:i})}_entityDown(e){const t=e.target,i=this.entities.concat();[i[t.index+1],i[t.index]]=[i[t.index],i[t.index+1]],Object(o.a)(this,"entities-changed",{entities:i})}_valueChanged(e){const t=e.target,i=this.entities.concat();""===t.value?i.splice(t.index,1):i[t.index]=Object.assign(Object.assign({},i[t.index]),{entity:t.value}),Object(o.a)(this,"entities-changed",{entities:i})}static get styles(){return n.c`
      .entities {
        padding-left: 20px;
      }
      .entity {
        display: flex;
        align-items: flex-end;
      }
      .entity ha-entity-picker {
        flex-grow: 1;
      }
    `}};Object(a.c)([Object(n.g)()],s.prototype,"hass",void 0),Object(a.c)([Object(n.g)()],s.prototype,"entities",void 0),Object(a.c)([Object(n.g)()],s.prototype,"label",void 0),s=Object(a.c)([Object(n.d)("hui-entity-editor")],s)},257:function(e,t,i){"use strict";i.d(t,"a",function(){return n}),i.d(t,"b",function(){return o});var a=i(192);const n=Object(a.a)({action:"string",navigation_path:"string?",url_path:"string?",service:"string?",service_data:"object?"}),o=a.a.union([{entity:"entity-id",name:"string?",icon:"icon?"},"entity-id"])},258:function(e,t,i){"use strict";var a=i(4),n=i(30),o=(i(108),i(93),i(143),i(207),i(118));customElements.define("ha-combo-box",class extends(Object(o.a)(n.a)){static get template(){return a.a`
      <style>
        paper-input > paper-icon-button {
          width: 24px;
          height: 24px;
          padding: 2px;
          color: var(--secondary-text-color);
        }
        [hidden] {
          display: none;
        }
      </style>
      <vaadin-combo-box-light
        items="[[_items]]"
        item-value-path="[[itemValuePath]]"
        item-label-path="[[itemLabelPath]]"
        value="{{value}}"
        opened="{{opened}}"
        allow-custom-value="[[allowCustomValue]]"
        on-change="_fireChanged"
      >
        <paper-input
          autofocus="[[autofocus]]"
          label="[[label]]"
          class="input"
          value="[[value]]"
        >
          <paper-icon-button
            slot="suffix"
            class="clear-button"
            icon="hass:close"
            hidden$="[[!value]]"
            >Clear</paper-icon-button
          >
          <paper-icon-button
            slot="suffix"
            class="toggle-button"
            icon="[[_computeToggleIcon(opened)]]"
            hidden$="[[!items.length]]"
            >Toggle</paper-icon-button
          >
        </paper-input>
        <template>
          <style>
            paper-item {
              margin: -5px -10px;
              padding: 0;
            }
          </style>
          <paper-item>[[_computeItemLabel(item, itemLabelPath)]]</paper-item>
        </template>
      </vaadin-combo-box-light>
    `}static get properties(){return{allowCustomValue:Boolean,items:{type:Object,observer:"_itemsChanged"},_items:Object,itemLabelPath:String,itemValuePath:String,autofocus:Boolean,label:String,opened:{type:Boolean,value:!1,observer:"_openedChanged"},value:{type:String,notify:!0}}}_openedChanged(e){e||(this._items=this.items)}_itemsChanged(e){this.opened||(this._items=e)}_computeToggleIcon(e){return e?"hass:menu-up":"hass:menu-down"}_computeItemLabel(e,t){return t?e[t]:e}_fireChanged(e){e.stopPropagation(),this.fire("change")}});var s=i(175);customElements.define("ha-service-picker",class extends(Object(s.a)(n.a)){static get template(){return a.a`
      <ha-combo-box
        label="[[localize('ui.components.service-picker.service')]]"
        items="[[_services]]"
        value="{{value}}"
        allow-custom-value=""
      ></ha-combo-box>
    `}static get properties(){return{hass:{type:Object,observer:"_hassChanged"},_services:Array,value:{type:String,notify:!0}}}_hassChanged(e,t){if(!e)return void(this._services=[]);if(t&&e.services===t.services)return;const i=[];Object.keys(e.services).sort().forEach(t=>{const a=Object.keys(e.services[t]).sort();for(let e=0;e<a.length;e++)i.push(`${t}.${a[e]}`)}),this._services=i}})},271:function(e,t,i){"use strict";function a(e){return e.map(e=>"string"==typeof e?{entity:e}:e)}i.d(t,"a",function(){return a})},316:function(e,t,i){"use strict";var a=i(3),n=i(0),o=(i(216),i(146),i(143),i(145),i(258),i(18));let s=class extends n.a{get _action(){return this.config.action||""}get _navigation_path(){return this.config.navigation_path||""}get _url_path(){return this.config.url_path||""}get _service(){return this.config.service||""}render(){return this.hass&&this.actions?n.f`
      <paper-dropdown-menu
        .label="${this.label}"
        .configValue="${"action"}"
        @value-changed="${this._valueChanged}"
      >
        <paper-listbox
          slot="dropdown-content"
          .selected="${this.actions.indexOf(this._action)}"
        >
          ${this.actions.map(e=>n.f`
              <paper-item>${e}</paper-item>
            `)}
        </paper-listbox>
      </paper-dropdown-menu>
      ${"navigate"===this._action?n.f`
            <paper-input
              label="Navigation Path"
              .value="${this._navigation_path}"
              .configValue="${"navigation_path"}"
              @value-changed="${this._valueChanged}"
            ></paper-input>
          `:""}
      ${"url"===this._action?n.f`
            <paper-input
              label="Url Path"
              .value="${this._url_path}"
              .configValue="${"url_path"}"
              @value-changed="${this._valueChanged}"
            ></paper-input>
          `:""}
      ${this.config&&"call-service"===this.config.action?n.f`
            <ha-service-picker
              .hass="${this.hass}"
              .value="${this._service}"
              .configValue="${"service"}"
              @value-changed="${this._valueChanged}"
            ></ha-service-picker>
            <h3>Toggle Editor to input Service Data</h3>
          `:""}
    `:n.f``}_valueChanged(e){if(!this.hass)return;const t=e.target;this[`_${t.configValue}`]!==t.value&&("action"===t.configValue&&(this.config={action:"none"}),t.configValue&&(this.config=Object.assign(Object.assign({},this.config),{[t.configValue]:t.value}),Object(o.a)(this,"action-changed")))}};Object(a.c)([Object(n.g)()],s.prototype,"config",void 0),Object(a.c)([Object(n.g)()],s.prototype,"label",void 0),Object(a.c)([Object(n.g)()],s.prototype,"actions",void 0),Object(a.c)([Object(n.g)()],s.prototype,"hass",void 0),s=Object(a.c)([Object(n.d)("hui-action-editor")],s)},705:function(e,t,i){"use strict";i.r(t),i.d(t,"HuiPictureGlanceCardEditor",function(){return h});var a=i(3),n=i(0),o=(i(93),i(146),i(143),i(145),i(316),i(231),i(189),i(192)),s=i(257),c=i(18),l=i(200),r=i(271);const p=Object(o.a)({type:"string",title:"string?",entity:"string?",image:"string?",camera_image:"string?",camera_view:"string?",aspect_ratio:"string?",tap_action:o.a.optional(s.a),hold_action:o.a.optional(s.a),entities:[s.b]});let h=class extends n.a{setConfig(e){e=p(e),this._config=e,this._configEntities=Object(r.a)(e.entities)}get _entity(){return this._config.entity||""}get _title(){return this._config.title||""}get _image(){return this._config.image||this._camera_image?"":"https://www.home-assistant.io/images/merchandise/shirt-frontpage.png"}get _camera_image(){return this._config.camera_image||""}get _camera_view(){return this._config.camera_view||this._camera_image?"auto":""}get _state_image(){return this._config.state_image||{}}get _aspect_ratio(){return this._config.aspect_ratio||""}get _tap_action(){return this._config.tap_action||{action:"more-info"}}get _hold_action(){return this._config.hold_action||{action:"more-info"}}get _show_name(){return this._config.show_name||!1}get _show_state(){return this._config.show_state||!1}render(){if(!this.hass)return n.f``;const e=["more-info","toggle","navigate","call-service","none"],t=["auto","live"];return n.f`
      ${l.a}
      <div class="card-config">
        <paper-input
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.title")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .value="${this._title}"
          .configValue="${"title"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <paper-input
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.image")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .value="${this._image}"
          .configValue="${"image"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <ha-entity-picker
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.camera_image")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass="${this.hass}"
          .value="${this._camera_image}"
          .configValue=${"camera_image"}
          @change="${this._valueChanged}"
          allow-custom-entity
          domain-filter="camera"
        ></ha-entity-picker>
        <div class="side-by-side">
          <paper-dropdown-menu
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.camera_view")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .configValue="${"camera_view"}"
            @value-changed="${this._valueChanged}"
          >
            <paper-listbox
              slot="dropdown-content"
              .selected="${t.indexOf(this._camera_view)}"
            >
              ${t.map(e=>n.f`
                  <paper-item>${e}</paper-item>
                `)}
            </paper-listbox>
          </paper-dropdown-menu>
          <paper-input
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.aspect_ratio")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            type="number"
            .value="${Number(this._aspect_ratio.replace("%",""))}"
            .configValue="${"aspect_ratio"}"
            @value-changed="${this._valueChanged}"
          ></paper-input>
        </div>
        <ha-entity-picker
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.entity")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .hass="${this.hass}"
          .value="${this._entity}"
          .configValue=${"entity"}
          @change="${this._valueChanged}"
          allow-custom-entity
        ></ha-entity-picker>
        <div class="side-by-side">
          <hui-action-editor
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.tap_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .hass="${this.hass}"
            .config="${this._tap_action}"
            .actions="${e}"
            .configValue="${"tap_action"}"
            @action-changed="${this._valueChanged}"
          ></hui-action-editor>
          <hui-action-editor
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.hold_action")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .hass="${this.hass}"
            .config="${this._hold_action}"
            .actions="${e}"
            .configValue="${"hold_action"}"
            @action-changed="${this._valueChanged}"
          ></hui-action-editor>
        </div>
        <hui-entity-editor
          .hass="${this.hass}"
          .entities="${this._configEntities}"
          @entities-changed="${this._valueChanged}"
        ></hui-entity-editor>
      </div>
    `}_valueChanged(e){if(!this._config||!this.hass)return;const t=e.target;let i=t.value;if("aspect_ratio"===t.configValue&&t.value&&(i+="%"),e.detail&&e.detail.entities)this._config.entities=e.detail.entities,this._configEntities=Object(r.a)(this._config.entities);else if(t.configValue){if(this[`_${t.configValue}`]===i||this[`_${t.configValue}`]===t.config)return;""===i?delete this._config[t.configValue]:this._config=Object.assign(Object.assign({},this._config),{[t.configValue]:i||t.config})}Object(c.a)(this,"config-changed",{config:this._config})}};Object(a.c)([Object(n.g)()],h.prototype,"hass",void 0),Object(a.c)([Object(n.g)()],h.prototype,"_config",void 0),Object(a.c)([Object(n.g)()],h.prototype,"_configEntities",void 0),h=Object(a.c)([Object(n.d)("hui-picture-glance-card-editor")],h)}}]);
//# sourceMappingURL=chunk.c2999d1fee851c81ec1a.js.map