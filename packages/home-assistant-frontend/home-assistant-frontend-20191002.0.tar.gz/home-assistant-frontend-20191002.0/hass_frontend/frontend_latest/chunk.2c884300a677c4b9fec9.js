/*! For license information please see chunk.2c884300a677c4b9fec9.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[34],{196:function(t,e,i){"use strict";i(195);var a=i(72),s=i(1),r=i(126);const n={getTabbableNodes:function(t){var e=[];return this._collectTabbableNodes(t,e)?r.a._sortByTabIndex(e):e},_collectTabbableNodes:function(t,e){if(t.nodeType!==Node.ELEMENT_NODE||!r.a._isVisible(t))return!1;var i,a=t,n=r.a._normalizedTabIndex(a),o=n>0;n>=0&&e.push(a),i="content"===a.localName||"slot"===a.localName?Object(s.a)(a).getDistributedNodes():Object(s.a)(a.shadowRoot||a.root||a).children;for(var d=0;d<i.length;d++)o=this._collectTabbableNodes(i[d],e)||o;return o}},o=customElements.get("paper-dialog"),d={get _focusableNodes(){return n.getTabbableNodes(this)}};customElements.define("ha-paper-dialog",class extends(Object(a.b)([d],o)){})},502:function(t,e,i){"use strict";i.r(e);var a=i(3),s=i(0),r=(i(211),i(93),i(196),i(201),i(56)),n=i(121),o=i(176),d=i(267);class l extends s.a{async showDialog(t){this._params=t,this._error=void 0,this._name=this._params.entry.name||"",this._platform=this._params.entry.platform,this._entityId=this._params.entry.entity_id,this._disabledBy=this._params.entry.disabled_by,await this.updateComplete}render(){if(!this._params)return s.f``;const t=this._params.entry,e=this.hass.states[t.entity_id],i=Object(n.a)(this._entityId.trim())!==Object(n.a)(this._params.entry.entity_id);return s.f`
      <ha-paper-dialog
        with-backdrop
        opened
        @opened-changed="${this._openedChanged}"
      >
        <h2>
          ${e?Object(o.a)(e):t.name||t.entity_id}
        </h2>
        <paper-dialog-scrollable>
          ${e?"":s.f`
                <div>
                  ${this.hass.localize("ui.panel.config.entity_registry.editor.unavailable")}
                </div>
              `}
          ${this._error?s.f`
                <div class="error">${this._error}</div>
              `:""}
          <div class="form">
            <paper-input
              .value=${this._name}
              @value-changed=${this._nameChanged}
              .label=${this.hass.localize("ui.dialogs.more_info_settings.name")}
              .placeholder=${e?Object(o.a)(e):""}
              .disabled=${this._submitting}
            ></paper-input>
            <paper-input
              .value=${this._entityId}
              @value-changed=${this._entityIdChanged}
              .label=${this.hass.localize("ui.dialogs.more_info_settings.entity_id")}
              error-message="Domain needs to stay the same"
              .invalid=${i}
              .disabled=${this._submitting}
            ></paper-input>
            <div class="row">
              <ha-switch
                .checked=${!this._disabledBy}
                @change=${this._disabledByChanged}
              >
                <div>
                  <div>
                    ${this.hass.localize("ui.panel.config.entity_registry.editor.enabled_label")}
                  </div>
                  <div class="secondary">
                    ${this._disabledBy&&"user"!==this._disabledBy?this.hass.localize("ui.panel.config.entity_registry.editor.enabled_cause","cause",this.hass.localize(`config_entry.disabled_by.${this._disabledBy}`)):""}
                    ${this.hass.localize("ui.panel.config.entity_registry.editor.enabled_description")}
                    <br />Note: this might not work yet with all integrations.
                  </div>
                </div>
              </ha-switch>
            </div>
          </div>
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          <mwc-button
            class="warning"
            @click="${this._deleteEntry}"
            .disabled=${this._submitting}
          >
            ${this.hass.localize("ui.panel.config.entity_registry.editor.delete")}
          </mwc-button>
          <mwc-button
            @click="${this._updateEntry}"
            .disabled=${i||this._submitting}
          >
            ${this.hass.localize("ui.panel.config.entity_registry.editor.update")}
          </mwc-button>
        </div>
      </ha-paper-dialog>
    `}_nameChanged(t){this._error=void 0,this._name=t.detail.value}_entityIdChanged(t){this._error=void 0,this._entityId=t.detail.value}async _updateEntry(){this._submitting=!0;try{await Object(d.d)(this.hass,this._entityId,{name:this._name.trim()||null,disabled_by:this._disabledBy,new_entity_id:this._entityId.trim()}),this._params=void 0}catch(t){this._error=t.message||"Unknown error"}finally{this._submitting=!1}}async _deleteEntry(){if(confirm(`${this.hass.localize("ui.panel.config.entity_registry.editor.confirm_delete")}\n\n${this.hass.localize("ui.panel.config.entity_registry.editor.confirm_delete2","platform",this._platform)}`)){this._submitting=!0;try{await Object(d.b)(this.hass,this._entityId),this._params=void 0}finally{this._submitting=!1}}}_openedChanged(t){t.detail.value||(this._params=void 0)}_disabledByChanged(t){this._disabledBy=t.target.checked?null:"user"}static get styles(){return[r.b,s.c`
        ha-paper-dialog {
          min-width: 400px;
          max-width: 450px;
        }
        .form {
          padding-bottom: 24px;
        }
        mwc-button.warning {
          margin-right: auto;
        }
        .error {
          color: var(--google-red-500);
        }
        .row {
          margin-top: 8px;
          color: var(--primary-text-color);
        }
        .secondary {
          color: var(--secondary-text-color);
        }
      `]}}Object(a.c)([Object(s.g)()],l.prototype,"hass",void 0),Object(a.c)([Object(s.g)()],l.prototype,"_name",void 0),Object(a.c)([Object(s.g)()],l.prototype,"_platform",void 0),Object(a.c)([Object(s.g)()],l.prototype,"_entityId",void 0),Object(a.c)([Object(s.g)()],l.prototype,"_disabledBy",void 0),Object(a.c)([Object(s.g)()],l.prototype,"_error",void 0),Object(a.c)([Object(s.g)()],l.prototype,"_params",void 0),Object(a.c)([Object(s.g)()],l.prototype,"_submitting",void 0),customElements.define("dialog-entity-registry-detail",l)}}]);
//# sourceMappingURL=chunk.2c884300a677c4b9fec9.js.map