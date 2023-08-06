(self.webpackJsonp=self.webpackJsonp||[]).push([[54],{189:function(t,e,i){"use strict";var n=i(3),a=(i(108),i(93),i(184),i(180),i(207),i(123)),s=(i(185),i(176)),o=i(0),c=i(18);const l=(t,e,i)=>{t.firstElementChild||(t.innerHTML='\n      <style>\n        paper-icon-item {\n          margin: -10px;\n          padding: 0;\n        }\n      </style>\n      <paper-icon-item>\n        <state-badge state-obj="[[item]]" slot="item-icon"></state-badge>\n        <paper-item-body two-line="">\n          <div class=\'name\'>[[_computeStateName(item)]]</div>\n          <div secondary>[[item.entity_id]]</div>\n        </paper-item-body>\n      </paper-icon-item>\n    '),t.querySelector("state-badge").stateObj=i.item,t.querySelector(".name").textContent=Object(s.a)(i.item),t.querySelector("[secondary]").textContent=i.item.entity_id};class r extends o.a{constructor(){super(...arguments),this._getStates=Object(a.a)((t,e,i)=>{let n=[];if(!t)return[];let a=Object.keys(t.states);return e&&(a=a.filter(t=>t.substr(0,t.indexOf("."))===e)),n=a.sort().map(e=>t.states[e]),i&&(n=n.filter(t=>t.entity_id===this.value||i(t))),n})}updated(t){super.updated(t),t.has("hass")&&!this._opened&&(this._hass=this.hass)}render(){const t=this._getStates(this._hass,this.domainFilter,this.entityFilter);return o.f`
      <vaadin-combo-box-light
        item-value-path="entity_id"
        item-label-path="entity_id"
        .items=${t}
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
          ${this.value?o.f`
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
          ${t.length>0?o.f`
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
    `}get _value(){return this.value||""}_openedChanged(t){this._opened=t.detail.value}_valueChanged(t){t.detail.value!==this._value&&(this.value=t.detail.value,setTimeout(()=>{Object(c.a)(this,"value-changed",{value:this.value}),Object(c.a)(this,"change")},0))}static get styles(){return o.c`
      paper-input > paper-icon-button {
        width: 24px;
        height: 24px;
        padding: 2px;
        color: var(--secondary-text-color);
      }
      [hidden] {
        display: none;
      }
    `}}Object(n.c)([Object(o.g)({type:Boolean})],r.prototype,"autofocus",void 0),Object(n.c)([Object(o.g)({type:Boolean})],r.prototype,"disabled",void 0),Object(n.c)([Object(o.g)({type:Boolean,attribute:"allow-custom-entity"})],r.prototype,"allowCustomEntity",void 0),Object(n.c)([Object(o.g)()],r.prototype,"hass",void 0),Object(n.c)([Object(o.g)()],r.prototype,"label",void 0),Object(n.c)([Object(o.g)()],r.prototype,"value",void 0),Object(n.c)([Object(o.g)({attribute:"domain-filter"})],r.prototype,"domainFilter",void 0),Object(n.c)([Object(o.g)()],r.prototype,"entityFilter",void 0),Object(n.c)([Object(o.g)({type:Boolean})],r.prototype,"_opened",void 0),Object(n.c)([Object(o.g)()],r.prototype,"_hass",void 0),customElements.define("ha-entity-picker",r)},192:function(t,e,i){"use strict";var n=i(203);i.d(e,"a",function(){return a});const a=Object(n.a)({types:{"entity-id":function(t){return"string"!=typeof t?"entity id should be a string":!!t.includes(".")||"entity id should be in the format 'domain.entity'"},icon:function(t){return"string"!=typeof t?"icon should be a string":!!t.includes(":")||"icon should be in the format 'mdi:icon'"}}})},200:function(t,e,i){"use strict";i.d(e,"a",function(){return n});const n=i(0).f`
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
`},231:function(t,e,i){"use strict";var n=i(3),a=i(0),s=(i(108),i(18));i(189);let o=class extends a.a{render(){return this.entities?a.f`
      <h3>
        ${this.label||this.hass.localize("ui.panel.lovelace.editor.card.generic.entities")+" ("+this.hass.localize("ui.panel.lovelace.editor.card.config.required")+")"}
      </h3>
      <div class="entities">
        ${this.entities.map((t,e)=>a.f`
            <div class="entity">
              <ha-entity-picker
                .hass="${this.hass}"
                .value="${t.entity}"
                .index="${e}"
                @change="${this._valueChanged}"
                allow-custom-entity
              ></ha-entity-picker>
              <paper-icon-button
                title="Move entity down"
                icon="hass:arrow-down"
                .index="${e}"
                @click="${this._entityDown}"
                ?disabled="${e===this.entities.length-1}"
              ></paper-icon-button>
              <paper-icon-button
                title="Move entity up"
                icon="hass:arrow-up"
                .index="${e}"
                @click="${this._entityUp}"
                ?disabled="${0===e}"
              ></paper-icon-button>
            </div>
          `)}
        <ha-entity-picker
          .hass="${this.hass}"
          @change="${this._addEntity}"
        ></ha-entity-picker>
      </div>
    `:a.f``}_addEntity(t){const e=t.target;if(""===e.value)return;const i=this.entities.concat({entity:e.value});e.value="",Object(s.a)(this,"entities-changed",{entities:i})}_entityUp(t){const e=t.target,i=this.entities.concat();[i[e.index-1],i[e.index]]=[i[e.index],i[e.index-1]],Object(s.a)(this,"entities-changed",{entities:i})}_entityDown(t){const e=t.target,i=this.entities.concat();[i[e.index+1],i[e.index]]=[i[e.index],i[e.index+1]],Object(s.a)(this,"entities-changed",{entities:i})}_valueChanged(t){const e=t.target,i=this.entities.concat();""===e.value?i.splice(e.index,1):i[e.index]=Object.assign(Object.assign({},i[e.index]),{entity:e.value}),Object(s.a)(this,"entities-changed",{entities:i})}static get styles(){return a.c`
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
    `}};Object(n.c)([Object(a.g)()],o.prototype,"hass",void 0),Object(n.c)([Object(a.g)()],o.prototype,"entities",void 0),Object(n.c)([Object(a.g)()],o.prototype,"label",void 0),o=Object(n.c)([Object(a.d)("hui-entity-editor")],o)},271:function(t,e,i){"use strict";function n(t){return t.map(t=>"string"==typeof t?{entity:t}:t)}i.d(e,"a",function(){return n})},697:function(t,e,i){"use strict";i.r(e),i.d(e,"HuiHistoryGraphCardEditor",function(){return h});var n=i(3),a=i(0),s=(i(93),i(231),i(192)),o=i(18),c=i(271),l=i(200);const r=s.a.union([{entity:"entity-id",name:"string?"},"entity-id"]),d=Object(s.a)({type:"string",entities:[r],title:"string?",hours_to_show:"number?",refresh_interval:"number?"});let h=class extends a.a{setConfig(t){t=d(t),this._config=t,this._configEntities=Object(c.a)(t.entities)}get _entity(){return this._config.entity||""}get _title(){return this._config.title||""}get _hours_to_show(){return this._config.number||24}get _refresh_interval(){return this._config.number||0}render(){return this.hass?a.f`
      ${l.a}
      <div class="card-config">
        <paper-input
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.title")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .value="${this._title}"
          .configValue="${"title"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <div class="side-by-side">
          <paper-input
            type="number"
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.hours_to_show")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .value="${this._hours_to_show}"
            .configValue=${"hours_to_show"}
            @value-changed="${this._valueChanged}"
          ></paper-input>
          <paper-input
            type="number"
            .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.refresh_interval")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
            .value="${this._refresh_interval}"
            .configValue=${"refresh_interval"}
            @value-changed="${this._valueChanged}"
          ></paper-input>
        </div>
        <hui-entity-editor
          .hass="${this.hass}"
          .entities="${this._configEntities}"
          @entities-changed="${this._valueChanged}"
        ></hui-entity-editor>
      </div>
    `:a.f``}_valueChanged(t){if(!this._config||!this.hass)return;const e=t.target;if(t.detail||this[`_${e.configValue}`]!==e.value){if(t.detail&&t.detail.entities)this._config.entities=t.detail.entities,this._configEntities=Object(c.a)(this._config.entities);else if(e.configValue)if(""===e.value)delete this._config[e.configValue];else{let t=e.value;"number"===e.type&&(t=Number(t)),this._config=Object.assign(Object.assign({},this._config),{[e.configValue]:t})}Object(o.a)(this,"config-changed",{config:this._config})}}};Object(n.c)([Object(a.g)()],h.prototype,"hass",void 0),Object(n.c)([Object(a.g)()],h.prototype,"_config",void 0),Object(n.c)([Object(a.g)()],h.prototype,"_configEntities",void 0),h=Object(n.c)([Object(a.d)("hui-history-graph-card-editor")],h)}}]);
//# sourceMappingURL=chunk.5799dba07227e4f103f1.js.map