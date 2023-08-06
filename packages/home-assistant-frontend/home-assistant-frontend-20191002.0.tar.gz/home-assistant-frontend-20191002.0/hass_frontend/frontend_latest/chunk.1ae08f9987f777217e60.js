(self.webpackJsonp=self.webpackJsonp||[]).push([[58],{192:function(e,t,i){"use strict";var n=i(203);i.d(t,"a",function(){return a});const a=Object(n.a)({types:{"entity-id":function(e){return"string"!=typeof e?"entity id should be a string":!!e.includes(".")||"entity id should be in the format 'domain.entity'"},icon:function(e){return"string"!=typeof e?"icon should be a string":!!e.includes(":")||"icon should be in the format 'mdi:icon'"}}})},200:function(e,t,i){"use strict";i.d(t,"a",function(){return n});const n=i(0).f`
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
`},701:function(e,t,i){"use strict";i.r(t),i.d(t,"HuiMarkdownCardEditor",function(){return r});var n=i(3),a=i(0),c=(i(93),i(216),i(192)),o=i(18),s=i(200);const l=Object(c.a)({type:"string",title:"string?",content:"string"});let r=class extends a.a{setConfig(e){e=l(e),this._config=e}get _title(){return this._config.title||""}get _content(){return this._config.content||""}render(){return this.hass?a.f`
      ${s.a}
      <div class="card-config">
        <paper-input
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.generic.title")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.optional")})"
          .value="${this._title}"
          .configValue="${"title"}"
          @value-changed="${this._valueChanged}"
        ></paper-input>
        <paper-textarea
          .label="${this.hass.localize("ui.panel.lovelace.editor.card.markdown.content")} (${this.hass.localize("ui.panel.lovelace.editor.card.config.required")})"
          .value="${this._content}"
          .configValue="${"content"}"
          @value-changed="${this._valueChanged}"
          autocapitalize="none"
          autocomplete="off"
          spellcheck="false"
        ></paper-textarea>
      </div>
    `:a.f``}_valueChanged(e){if(!this._config||!this.hass)return;const t=e.target;this[`_${t.configValue}`]!==t.value&&(t.configValue&&(""===t.value?delete this._config[t.configValue]:this._config=Object.assign(Object.assign({},this._config),{[t.configValue]:t.value})),Object(o.a)(this,"config-changed",{config:this._config}))}};Object(n.c)([Object(a.g)()],r.prototype,"hass",void 0),Object(n.c)([Object(a.g)()],r.prototype,"_config",void 0),r=Object(n.c)([Object(a.d)("hui-markdown-card-editor")],r)}}]);
//# sourceMappingURL=chunk.1ae08f9987f777217e60.js.map