/*! For license information please see chunk.3e56d29df4b6a15c587c.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[26],{196:function(t,e,i){"use strict";i(195);var s=i(72),o=i(1),a=i(126);const r={getTabbableNodes:function(t){var e=[];return this._collectTabbableNodes(t,e)?a.a._sortByTabIndex(e):e},_collectTabbableNodes:function(t,e){if(t.nodeType!==Node.ELEMENT_NODE||!a.a._isVisible(t))return!1;var i,s=t,r=a.a._normalizedTabIndex(s),c=r>0;r>=0&&e.push(s),i="content"===s.localName||"slot"===s.localName?Object(o.a)(s).getDistributedNodes():Object(o.a)(s.shadowRoot||s.root||s).children;for(var n=0;n<i.length;n++)c=this._collectTabbableNodes(i[n],e)||c;return c}},c=customElements.get("paper-dialog"),n={get _focusableNodes(){return r.getTabbableNodes(this)}};customElements.define("ha-paper-dialog",class extends(Object(s.b)([n],c)){})},201:function(t,e,i){"use strict";var s=i(3),o=i(0),a=(i(235),i(212));const r=customElements.get("mwc-switch");let c=class extends r{firstUpdated(){super.firstUpdated(),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)"),this.classList.toggle("slotted",Boolean(this._slot.assignedNodes().length))}static get styles(){return[a.a,o.c`
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
      `]}};Object(s.c)([Object(o.h)("slot")],c.prototype,"_slot",void 0),c=Object(s.c)([Object(o.d)("ha-switch")],c)},722:function(t,e,i){"use strict";i.r(e);var s=i(3),o=i(0),a=(i(211),i(93),i(196),i(201),i(315)),r=i(56);let c=class extends o.a{async showDialog(t){this._params=t,this._error=void 0,this._loading=!0;const e=await Object(a.c)(this.hass,t.entry.entry_id);this._loading=!1,this._disableNewEntities=e.disable_new_entities,await this.updateComplete}render(){return this._params?o.f`
      <ha-paper-dialog
        with-backdrop
        opened
        @opened-changed="${this._openedChanged}"
      >
        <h2>
          ${this.hass.localize("ui.dialogs.config_entry_system_options.title")}
        </h2>
        <paper-dialog-scrollable>
          ${this._loading?o.f`
                <div class="init-spinner">
                  <paper-spinner-lite active></paper-spinner-lite>
                </div>
              `:o.f`
                ${this._error?o.f`
                      <div class="error">${this._error}</div>
                    `:""}
                <div class="form">
                  <ha-switch
                    .checked=${!this._disableNewEntities}
                    @change=${this._disableNewEntitiesChanged}
                    .disabled=${this._submitting}
                  >
                    <div>
                      ${this.hass.localize("ui.dialogs.config_entry_system_options.enable_new_entities_label")}
                    </div>
                    <div class="secondary">
                      ${this.hass.localize("ui.dialogs.config_entry_system_options.enable_new_entities_description")}
                    </div>
                  </ha-switch>
                </div>
              `}
        </paper-dialog-scrollable>
        ${this._loading?"":o.f`
              <div class="paper-dialog-buttons">
                <mwc-button
                  @click="${this._updateEntry}"
                  .disabled=${this._submitting}
                >
                  ${this.hass.localize("ui.panel.config.entity_registry.editor.update")}
                </mwc-button>
              </div>
            `}
      </ha-paper-dialog>
    `:o.f``}_disableNewEntitiesChanged(t){this._error=void 0,this._disableNewEntities=!t.target.checked}async _updateEntry(){this._submitting=!0;try{await Object(a.d)(this.hass,this._params.entry.entry_id,{disable_new_entities:this._disableNewEntities}),this._params=void 0}catch(t){this._error=t.message||"Unknown error"}finally{this._submitting=!1}}_openedChanged(t){t.detail.value||(this._params=void 0)}static get styles(){return[r.b,o.c`
        ha-paper-dialog {
          min-width: 400px;
          max-width: 500px;
        }
        .init-spinner {
          padding: 50px 100px;
          text-align: center;
        }

        .form {
          padding-top: 6px;
          padding-bottom: 24px;
          color: var(--primary-text-color);
        }

        .secondary {
          color: var(--secondary-text-color);
        }

        .error {
          color: var(--google-red-500);
        }
      `]}};Object(s.c)([Object(o.g)()],c.prototype,"hass",void 0),Object(s.c)([Object(o.g)()],c.prototype,"_disableNewEntities",void 0),Object(s.c)([Object(o.g)()],c.prototype,"_error",void 0),Object(s.c)([Object(o.g)()],c.prototype,"_params",void 0),Object(s.c)([Object(o.g)()],c.prototype,"_loading",void 0),Object(s.c)([Object(o.g)()],c.prototype,"_submitting",void 0),c=Object(s.c)([Object(o.d)("dialog-config-entry-system-options")],c)}}]);
//# sourceMappingURL=chunk.3e56d29df4b6a15c587c.js.map