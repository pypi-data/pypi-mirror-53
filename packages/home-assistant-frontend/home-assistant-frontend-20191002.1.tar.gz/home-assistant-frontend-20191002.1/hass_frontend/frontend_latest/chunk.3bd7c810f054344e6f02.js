(self.webpackJsonp=self.webpackJsonp||[]).push([[49],{713:function(t,e,a){"use strict";a.r(e),a.d(e,"HuiEmptyStateCard",function(){return n});var s=a(3),c=a(0);a(177);let n=class extends c.a{getCardSize(){return 2}setConfig(t){}render(){return this.hass?c.f`
      <ha-card
        .header="${this.hass.localize("ui.panel.lovelace.cards.empty_state.title")}"
      >
        <div class="card-content">
          ${this.hass.localize("ui.panel.lovelace.cards.empty_state.no_devices")}
        </div>
        <div class="card-actions">
          <a href="/config/integrations">
            <mwc-button>
              ${this.hass.localize("ui.panel.lovelace.cards.empty_state.go_to_integrations_page")}
            </mwc-button>
          </a>
        </div>
      </header-card>
    `:c.f``}static get styles(){return c.c`
      .content {
        margin-top: -1em;
        padding: 16px;
      }

      .card-actions a {
        text-decoration: none;
      }

      mwc-button {
        margin-left: -8px;
      }
    `}};Object(s.c)([Object(c.g)()],n.prototype,"hass",void 0),n=Object(s.c)([Object(c.d)("hui-empty-state-card")],n)}}]);
//# sourceMappingURL=chunk.3bd7c810f054344e6f02.js.map