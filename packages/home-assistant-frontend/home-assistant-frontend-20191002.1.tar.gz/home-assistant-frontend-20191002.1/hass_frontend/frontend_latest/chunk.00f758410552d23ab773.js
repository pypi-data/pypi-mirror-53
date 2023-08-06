(self.webpackJsonp=self.webpackJsonp||[]).push([[52],{189:function(e,t,i){"use strict";var a=i(3),n=(i(108),i(93),i(184),i(180),i(207),i(123)),s=(i(185),i(176)),c=i(0),o=i(18);const l=(e,t,i)=>{e.firstElementChild||(e.innerHTML='\n      <style>\n        paper-icon-item {\n          margin: -10px;\n          padding: 0;\n        }\n      </style>\n      <paper-icon-item>\n        <state-badge state-obj="[[item]]" slot="item-icon"></state-badge>\n        <paper-item-body two-line="">\n          <div class=\'name\'>[[_computeStateName(item)]]</div>\n          <div secondary>[[item.entity_id]]</div>\n        </paper-item-body>\n      </paper-icon-item>\n    '),e.querySelector("state-badge").stateObj=i.item,e.querySelector(".name").textContent=Object(s.a)(i.item),e.querySelector("[secondary]").textContent=i.item.entity_id};class r extends c.a{constructor(){super(...arguments),this._getStates=Object(n.a)((e,t,i)=>{let a=[];if(!e)return[];let n=Object.keys(e.states);return t&&(n=n.filter(e=>e.substr(0,e.indexOf("."))===t)),a=n.sort().map(t=>e.states[t]),i&&(a=a.filter(e=>e.entity_id===this.value||i(e))),a})}updated(e){super.updated(e),e.has("hass")&&!this._opened&&(this._hass=this.hass)}render(){const e=this._getStates(this._hass,this.domainFilter,this.entityFilter);return c.f`
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
          ${this.value?c.f`
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
          ${e.length>0?c.f`
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
    `}get _value(){return this.value||""}_openedChanged(e){this._opened=e.detail.value}_valueChanged(e){e.detail.value!==this._value&&(this.value=e.detail.value,setTimeout(()=>{Object(o.a)(this,"value-changed",{value:this.value}),Object(o.a)(this,"change")},0))}static get styles(){return c.c`
      paper-input > paper-icon-button {
        width: 24px;
        height: 24px;
        padding: 2px;
        color: var(--secondary-text-color);
      }
      [hidden] {
        display: none;
      }
    `}}Object(a.c)([Object(c.g)({type:Boolean})],r.prototype,"autofocus",void 0),Object(a.c)([Object(c.g)({type:Boolean})],r.prototype,"disabled",void 0),Object(a.c)([Object(c.g)({type:Boolean,attribute:"allow-custom-entity"})],r.prototype,"allowCustomEntity",void 0),Object(a.c)([Object(c.g)()],r.prototype,"hass",void 0),Object(a.c)([Object(c.g)()],r.prototype,"label",void 0),Object(a.c)([Object(c.g)()],r.prototype,"value",void 0),Object(a.c)([Object(c.g)({attribute:"domain-filter"})],r.prototype,"domainFilter",void 0),Object(a.c)([Object(c.g)()],r.prototype,"entityFilter",void 0),Object(a.c)([Object(c.g)({type:Boolean})],r.prototype,"_opened",void 0),Object(a.c)([Object(c.g)()],r.prototype,"_hass",void 0),customElements.define("ha-entity-picker",r)},192:function(e,t,i){"use strict";var a=i(203);i.d(t,"a",function(){return n});const n=Object(a.a)({types:{"entity-id":function(e){return"string"!=typeof e?"entity id should be a string":!!e.includes(".")||"entity id should be in the format 'domain.entity'"},icon:function(e){return"string"!=typeof e?"icon should be a string":!!e.includes(":")||"icon should be in the format 'mdi:icon'"}}})},200:function(e,t,i){"use strict";i.d(t,"a",function(){return a});const a=i(0).f`
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
`},231:function(e,t,i){"use strict";var a=i(3),n=i(0),s=(i(108),i(18));i(189);let c=class extends n.a{render(){return this.entities?n.f`
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
    `:n.f``}_addEntity(e){const t=e.target;if(""===t.value)return;const i=this.entities.concat({entity:t.value});t.value="",Object(s.a)(this,"entities-changed",{entities:i})}_entityUp(e){const t=e.target,i=this.entities.concat();[i[t.index-1],i[t.index]]=[i[t.index],i[t.index-1]],Object(s.a)(this,"entities-changed",{entities:i})}_entityDown(e){const t=e.target,i=this.entities.concat();[i[t.index+1],i[t.index]]=[i[t.index],i[t.index+1]],Object(s.a)(this,"entities-changed",{entities:i})}_valueChanged(e){const t=e.target,i=this.entities.concat();""===t.value?i.splice(t.index,1):i[t.index]=Object.assign(Object.assign({},i[t.index]),{entity:t.value}),Object(s.a)(this,"entities-changed",{entities:i})}static get styles(){return n.c`
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
    `}};Object(a.c)([Object(n.g)()],c.prototype,"hass",void 0),Object(a.c)([Object(n.g)()],c.prototype,"entities",void 0),Object(a.c)([Object(n.g)()],c.prototype,"label",void 0),c=Object(a.c)([Object(n.d)("hui-entity-editor")],c)},246:function(e,t,i){"use strict";var a=i(3),n=i(0),s=(i(85),i(18));let c=class extends n.a{render(){const e=["Backend-selected","default"].concat(Object.keys(this.hass.themes.themes).sort());return n.f`
      <paper-dropdown-menu
        .label=${this.label||this.hass.localize("ui.panel.lovelace.editor.card.generic.theme")+" ("+this.hass.localize("ui.panel.lovelace.editor.card.config.optional")+")"}
        dynamic-align
        @value-changed="${this._changed}"
      >
        <paper-listbox
          slot="dropdown-content"
          .selected="${this.value}"
          attr-for-selected="theme"
        >
          ${e.map(e=>n.f`
              <paper-item theme="${e}">${e}</paper-item>
            `)}
        </paper-listbox>
      </paper-dropdown-menu>
    `}static get styles(){return n.c`
      paper-dropdown-menu {
        width: 100%;
      }
    `}_changed(e){this.hass&&""!==e.target.value&&(this.value=e.target.value,Object(s.a)(this,"theme-changed"))}};Object(a.c)([Object(n.g)()],c.prototype,"value",void 0),Object(a.c)([Object(n.g)()],c.prototype,"label",void 0),Object(a.c)([Object(n.g)()],c.prototype,"hass",void 0),c=Object(a.c)([Object(n.d)("hui-theme-select-editor")],c)},711:function(e,t,i){"use strict";i.r(t),i.d(t,"HuiGaugeCardEditor",function(){return r});var a=i(3),n=i(0),s=(i(93),i(246),i(231),i(201),i(192)),c=i(18),o=i(200);const l=Object(s.a)({type:"string",name:"string?",entity:"string?",unit:"string?",min:"number?",max:"number?",severity:"object?",theme:"string?"});let r=class extends n.a{setConfig(e){e=l(e),this._useSeverity=!!e.severity,this._config=e}get _name(){return this._config.name||""}get _entity(){return this._config.entity||""}get _unit(){return this._config.unit||""}get _theme(){return this._config.theme||"default"}get _min(){return this._config.number||0}get _max(){return this._config.max||100}get _severity(){return this._config.severity||void 0}render(){return this.hass?n.f`
      ${o.a}
      <div class="card-config">
        <ha-entity-picker
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.entity")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})"
          .hass="${this.hass}"
          .value="${this._entity}"
          .configValue=${"entity"}
          domain-filter="sensor"
          @change="${this._valueChanged}"
          allow-custom-entity
        ></ha-entity-picker>
        <paper-input
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.name")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .value="${this._name}"
          .configValue=${"name"}
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <div class="side-by-side">
          <paper-input
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.unit")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .value="${this._unit}"
            .configValue=${"unit"}
            @value-changed="${this._valueChanged}"
          ></paper-input>
          <hui-theme-select-editor
            .hass="${this.hass}"
            .value="${this._theme}"
            .configValue="${"theme"}"
            @theme-changed="${this._valueChanged}"
          ></hui-theme-select-editor>
        </div>
        <div class="side-by-side">
          <paper-input
            type="number"
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.minimum")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .value="${this._min}"
            .configValue=${"min"}
            @value-changed="${this._valueChanged}"
          ></paper-input>
          <paper-input
            type="number"
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.maximum")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .value="${this._max}"
            .configValue=${"max"}
            @value-changed="${this._valueChanged}"
          ></paper-input>
        </div>
        <ha-switch
          ?checked="${!1!==this._useSeverity}"
          @change="${this._toggleSeverity}"
          >${this.hass.localize("ui.panel.lovelace.editor.card.gauge.severity.define")}</ha-switch
        >
        ${this._useSeverity?n.f`
            <div class="severity side-by-side">
              <paper-input
                type="number"
                .label="${this.hass.localize("ui.panel.lovelace.editor.card.gauge.severity.green")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})"
                .value="${this._severity?this._severity.green:0}"
                .configValue=${"green"}
                @value-changed="${this._severityChanged}"
              ></paper-input>
              <paper-input
                type="number"
                .label="${this.hass.localize("ui.panel.lovelace.editor.card.gauge.severity.yellow")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})"
                .value="${this._severity?this._severity.yellow:0}"
                .configValue=${"yellow"}
                @value-changed="${this._severityChanged}"
              ></paper-input>
              <paper-input
                type="number"
                .label="${this.hass.localize("ui.panel.lovelace.editor.card.gauge.severity.red")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})"
                .value="${this._severity?this._severity.red:0}"
                .configValue=${"red"}
                @value-changed="${this._severityChanged}"
              ></paper-input>
            </div>
          </div>
          `:""}
      </div>
    `:n.f``}static get styles(){return n.c`
      .severity {
        display: none;
        width: 100%;
        padding-left: 16px;
        flex-direction: row;
        flex-wrap: wrap;
      }
      .severity > * {
        flex: 1 0 30%;
        padding-right: 4px;
      }
      ha-switch[checked] ~ .severity {
        display: flex;
      }
    `}_toggleSeverity(e){if(!this._config||!this.hass)return;const t=e.target;this._config.severity=t.checked?{green:0,yellow:0,red:0}:void 0,Object(c.a)(this,"config-changed",{config:this._config})}_severityChanged(e){if(!this._config||!this.hass)return;const t=e.target,i=Object.assign(Object.assign({},this._config.severity),{[t.configValue]:Number(t.value)});this._config=Object.assign(Object.assign({},this._config),{severity:i}),Object(c.a)(this,"config-changed",{config:this._config})}_valueChanged(e){if(!this._config||!this.hass)return;const t=e.target;if(t.configValue)if(""===t.value||"number"===t.type&&isNaN(Number(t.value)))delete this._config[t.configValue];else{let e=t.value;"number"===t.type&&(e=Number(e)),this._config=Object.assign(Object.assign({},this._config),{[t.configValue]:e})}Object(c.a)(this,"config-changed",{config:this._config})}};Object(a.c)([Object(n.g)()],r.prototype,"hass",void 0),Object(a.c)([Object(n.g)()],r.prototype,"_config",void 0),r=Object(a.c)([Object(n.d)("hui-gauge-card-editor")],r)}}]);
//# sourceMappingURL=chunk.00f758410552d23ab773.js.map