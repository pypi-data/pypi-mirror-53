(self.webpackJsonp=self.webpackJsonp||[]).push([[60],{192:function(e,t,i){"use strict";var a=i(203);i.d(t,"a",function(){return n});const n=Object(a.a)({types:{"entity-id":function(e){return"string"!=typeof e?"entity id should be a string":!!e.includes(".")||"entity id should be in the format 'domain.entity'"},icon:function(e){return"string"!=typeof e?"icon should be a string":!!e.includes(":")||"icon should be in the format 'mdi:icon'"}}})},200:function(e,t,i){"use strict";i.d(t,"a",function(){return a});const a=i(0).f`
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
`},257:function(e,t,i){"use strict";i.d(t,"a",function(){return n}),i.d(t,"b",function(){return o});var a=i(192);const n=Object(a.a)({action:"string",navigation_path:"string?",url_path:"string?",service:"string?",service_data:"object?"}),o=a.a.union([{entity:"entity-id",name:"string?",icon:"icon?"},"entity-id"])},258:function(e,t,i){"use strict";var a=i(4),n=i(30),o=(i(108),i(93),i(143),i(207),i(118));customElements.define("ha-combo-box",class extends(Object(o.a)(n.a)){static get template(){return a.a`
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
    `}static get properties(){return{hass:{type:Object,observer:"_hassChanged"},_services:Array,value:{type:String,notify:!0}}}_hassChanged(e,t){if(!e)return void(this._services=[]);if(t&&e.services===t.services)return;const i=[];Object.keys(e.services).sort().forEach(t=>{const a=Object.keys(e.services[t]).sort();for(let e=0;e<a.length;e++)i.push(`${t}.${a[e]}`)}),this._services=i}})},316:function(e,t,i){"use strict";var a=i(3),n=i(0),o=(i(216),i(146),i(143),i(145),i(258),i(18));let s=class extends n.a{get _action(){return this.config.action||""}get _navigation_path(){return this.config.navigation_path||""}get _url_path(){return this.config.url_path||""}get _service(){return this.config.service||""}render(){return this.hass&&this.actions?n.f`
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
    `:n.f``}_valueChanged(e){if(!this.hass)return;const t=e.target;this[`_${t.configValue}`]!==t.value&&("action"===t.configValue&&(this.config={action:"none"}),t.configValue&&(this.config=Object.assign(Object.assign({},this.config),{[t.configValue]:t.value}),Object(o.a)(this,"action-changed")))}};Object(a.c)([Object(n.g)()],s.prototype,"config",void 0),Object(a.c)([Object(n.g)()],s.prototype,"label",void 0),Object(a.c)([Object(n.g)()],s.prototype,"actions",void 0),Object(a.c)([Object(n.g)()],s.prototype,"hass",void 0),s=Object(a.c)([Object(n.d)("hui-action-editor")],s)},703:function(e,t,i){"use strict";i.r(t),i.d(t,"HuiPictureCardEditor",function(){return u});var a=i(3),n=i(0),o=(i(93),i(316),i(192)),s=i(257),c=i(18),r=i(200);const l=Object(o.a)({type:"string",image:"string?",tap_action:o.a.optional(s.a),hold_action:o.a.optional(s.a)});let u=class extends n.a{setConfig(e){e=l(e),this._config=e}get _image(){return this._config.image||""}get _tap_action(){return this._config.tap_action||{action:"none"}}get _hold_action(){return this._config.hold_action||{action:"none"}}render(){if(!this.hass)return n.f``;const e=["navigate","url","call-service","none"];return n.f`
      ${r.a}
      <div class="card-config">
        <paper-input
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.image")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})"
          .value="${this._image}"
          .configValue="${"image"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
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
      </div>
    `}_valueChanged(e){if(!this._config||!this.hass)return;const t=e.target;this[`_${t.configValue}`]!==t.value&&this[`_${t.configValue}`]!==t.config&&(t.configValue&&(""===t.value?delete this._config[t.configValue]:this._config=Object.assign(Object.assign({},this._config),{[t.configValue]:t.value?t.value:t.config})),Object(c.a)(this,"config-changed",{config:this._config}))}};Object(a.c)([Object(n.g)()],u.prototype,"hass",void 0),Object(a.c)([Object(n.g)()],u.prototype,"_config",void 0),u=Object(a.c)([Object(n.d)("hui-picture-card-editor")],u)}}]);
//# sourceMappingURL=chunk.6d174f0d25de7cbd5a51.js.map