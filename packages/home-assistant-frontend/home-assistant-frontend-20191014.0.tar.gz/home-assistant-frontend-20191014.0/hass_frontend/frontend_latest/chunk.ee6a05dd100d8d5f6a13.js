/*! For license information please see chunk.ee6a05dd100d8d5f6a13.js.LICENSE */
(self.webpackJsonp=self.webpackJsonp||[]).push([[22],{122:function(t,i,o){"use strict";o(5);const n={properties:{animationConfig:{type:Object},entryAnimation:{observer:"_entryAnimationChanged",type:String},exitAnimation:{observer:"_exitAnimationChanged",type:String}},_entryAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.entry=[{name:this.entryAnimation,node:this}]},_exitAnimationChanged:function(){this.animationConfig=this.animationConfig||{},this.animationConfig.exit=[{name:this.exitAnimation,node:this}]},_copyProperties:function(t,i){for(var o in i)t[o]=i[o]},_cloneConfig:function(t){var i={isClone:!0};return this._copyProperties(i,t),i},_getAnimationConfigRecursive:function(t,i,o){var n;if(this.animationConfig)if(this.animationConfig.value&&"function"==typeof this.animationConfig.value)this._warn(this._logf("playAnimation","Please put 'animationConfig' inside of your components 'properties' object instead of outside of it."));else if(n=t?this.animationConfig[t]:this.animationConfig,Array.isArray(n)||(n=[n]),n)for(var e,a=0;e=n[a];a++)if(e.animatable)e.animatable._getAnimationConfigRecursive(e.type||t,i,o);else if(e.id){var s=i[e.id];s?(s.isClone||(i[e.id]=this._cloneConfig(s),s=i[e.id]),this._copyProperties(s,e)):i[e.id]=e}else o.push(e)},getAnimationConfig:function(t){var i={},o=[];for(var n in this._getAnimationConfigRecursive(t,i,o),i)o.push(i[n]);return o}};o.d(i,"a",function(){return e});const e=[n,{_configureAnimations:function(t){var i=[],o=[];if(t.length>0)for(let a,s=0;a=t[s];s++){let t=document.createElement(a.name);if(t.isNeonAnimation){let i=null;t.configure||(t.configure=function(t){return null}),i=t.configure(a),o.push({result:i,config:a,neonAnimation:t})}else console.warn(this.is+":",a.name,"not found!")}for(var n=0;n<o.length;n++){let t=o[n].result,a=o[n].config,s=o[n].neonAnimation;try{"function"!=typeof t.cancel&&(t=document.timeline.play(t))}catch(e){t=null,console.warn("Couldnt play","(",a.name,").",e)}t&&i.push({neonAnimation:s,config:a,animation:t})}return i},_shouldComplete:function(t){for(var i=!0,o=0;o<t.length;o++)if("finished"!=t[o].animation.playState){i=!1;break}return i},_complete:function(t){for(var i=0;i<t.length;i++)t[i].neonAnimation.complete(t[i].config);for(i=0;i<t.length;i++)t[i].animation.cancel()},playAnimation:function(t,i){var o=this.getAnimationConfig(t);if(o){this._active=this._active||{},this._active[t]&&(this._complete(this._active[t]),delete this._active[t]);var n=this._configureAnimations(o);if(0!=n.length){this._active[t]=n;for(var e=0;e<n.length;e++)n[e].animation.onfinish=function(){this._shouldComplete(n)&&(this._complete(n),delete this._active[t],this.fire("neon-animation-finish",i,{bubbles:!1}))}.bind(this)}else this.fire("neon-animation-finish",i,{bubbles:!1})}},cancelAnimation:function(){for(var t in this._active){var i=this._active[t];for(var o in i)i[o].animation.cancel()}this._active={}}}]},186:function(t,i,o){"use strict";o.d(i,"b",function(){return a}),o.d(i,"a",function(){return s});o(5);var n=o(87),e=o(1);const a={hostAttributes:{role:"dialog",tabindex:"-1"},properties:{modal:{type:Boolean,value:!1},__readied:{type:Boolean,value:!1}},observers:["_modalChanged(modal, __readied)"],listeners:{tap:"_onDialogClick"},ready:function(){this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.__readied=!0},_modalChanged:function(t,i){i&&(t?(this.__prevNoCancelOnOutsideClick=this.noCancelOnOutsideClick,this.__prevNoCancelOnEscKey=this.noCancelOnEscKey,this.__prevWithBackdrop=this.withBackdrop,this.noCancelOnOutsideClick=!0,this.noCancelOnEscKey=!0,this.withBackdrop=!0):(this.noCancelOnOutsideClick=this.noCancelOnOutsideClick&&this.__prevNoCancelOnOutsideClick,this.noCancelOnEscKey=this.noCancelOnEscKey&&this.__prevNoCancelOnEscKey,this.withBackdrop=this.withBackdrop&&this.__prevWithBackdrop))},_updateClosingReasonConfirmed:function(t){this.closingReason=this.closingReason||{},this.closingReason.confirmed=t},_onDialogClick:function(t){for(var i=Object(e.a)(t).path,o=0,n=i.indexOf(this);o<n;o++){var a=i[o];if(a.hasAttribute&&(a.hasAttribute("dialog-dismiss")||a.hasAttribute("dialog-confirm"))){this._updateClosingReasonConfirmed(a.hasAttribute("dialog-confirm")),this.close(),t.stopPropagation();break}}}},s=[n.a,a]},193:function(t,i,o){"use strict";o(5),o(45),o(42),o(54),o(86);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML='<dom-module id="paper-dialog-shared-styles">\n  <template>\n    <style>\n      :host {\n        display: block;\n        margin: 24px 40px;\n\n        background: var(--paper-dialog-background-color, var(--primary-background-color));\n        color: var(--paper-dialog-color, var(--primary-text-color));\n\n        @apply --paper-font-body1;\n        @apply --shadow-elevation-16dp;\n        @apply --paper-dialog;\n      }\n\n      :host > ::slotted(*) {\n        margin-top: 20px;\n        padding: 0 24px;\n      }\n\n      :host > ::slotted(.no-padding) {\n        padding: 0;\n      }\n\n      \n      :host > ::slotted(*:first-child) {\n        margin-top: 24px;\n      }\n\n      :host > ::slotted(*:last-child) {\n        margin-bottom: 24px;\n      }\n\n      /* In 1.x, this selector was `:host > ::content h2`. In 2.x <slot> allows\n      to select direct children only, which increases the weight of this\n      selector, so we have to re-define first-child/last-child margins below. */\n      :host > ::slotted(h2) {\n        position: relative;\n        margin: 0;\n\n        @apply --paper-font-title;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-top. */\n      :host > ::slotted(h2:first-child) {\n        margin-top: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      /* Apply mixin again, in case it sets margin-bottom. */\n      :host > ::slotted(h2:last-child) {\n        margin-bottom: 24px;\n        @apply --paper-dialog-title;\n      }\n\n      :host > ::slotted(.paper-dialog-buttons),\n      :host > ::slotted(.buttons) {\n        position: relative;\n        padding: 8px 8px 8px 24px;\n        margin: 0;\n\n        color: var(--paper-dialog-button-color, var(--primary-color));\n\n        @apply --layout-horizontal;\n        @apply --layout-end-justified;\n      }\n    </style>\n  </template>\n</dom-module>',document.head.appendChild(n.content)},195:function(t,i,o){"use strict";o(5),o(193);var n=o(122),e=o(186),a=o(6),s=o(4);Object(a.a)({_template:s.a`
    <style include="paper-dialog-shared-styles"></style>
    <slot></slot>
`,is:"paper-dialog",behaviors:[e.a,n.a],listeners:{"neon-animation-finish":"_onNeonAnimationFinish"},_renderOpened:function(){this.cancelAnimation(),this.playAnimation("entry")},_renderClosed:function(){this.cancelAnimation(),this.playAnimation("exit")},_onNeonAnimationFinish:function(){this.opened?this._finishRenderOpened():this._finishRenderClosed()}})},197:function(t,i,o){"use strict";o(195);var n=o(72),e=o(1),a=o(127);const s={getTabbableNodes:function(t){var i=[];return this._collectTabbableNodes(t,i)?a.a._sortByTabIndex(i):i},_collectTabbableNodes:function(t,i){if(t.nodeType!==Node.ELEMENT_NODE||!a.a._isVisible(t))return!1;var o,n=t,s=a.a._normalizedTabIndex(n),l=s>0;s>=0&&i.push(n),o="content"===n.localName||"slot"===n.localName?Object(e.a)(n).getDistributedNodes():Object(e.a)(n.shadowRoot||n.root||n).children;for(var r=0;r<o.length;r++)l=this._collectTabbableNodes(o[r],i)||l;return l}},l=customElements.get("paper-dialog"),r={get _focusableNodes(){return s.getTabbableNodes(this)}};customElements.define("ha-paper-dialog",class extends(Object(n.b)([r],l)){})},209:function(t,i,o){"use strict";o(5),o(45),o(42);var n=o(186),e=o(6),a=o(4);Object(e.a)({_template:a.a`
    <style>

      :host {
        display: block;
        @apply --layout-relative;
      }

      :host(.is-scrolled:not(:first-child))::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      :host(.can-scroll:not(.scrolled-to-bottom):not(:last-child))::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: var(--divider-color);
      }

      .scrollable {
        padding: 0 24px;

        @apply --layout-scroll;
        @apply --paper-dialog-scrollable;
      }

      .fit {
        @apply --layout-fit;
      }
    </style>

    <div id="scrollable" class="scrollable" on-scroll="updateScrollState">
      <slot></slot>
    </div>
`,is:"paper-dialog-scrollable",properties:{dialogElement:{type:Object}},get scrollTarget(){return this.$.scrollable},ready:function(){this._ensureTarget(),this.classList.add("no-padding")},attached:function(){this._ensureTarget(),requestAnimationFrame(this.updateScrollState.bind(this))},updateScrollState:function(){this.toggleClass("is-scrolled",this.scrollTarget.scrollTop>0),this.toggleClass("can-scroll",this.scrollTarget.offsetHeight<this.scrollTarget.scrollHeight),this.toggleClass("scrolled-to-bottom",this.scrollTarget.scrollTop+this.scrollTarget.offsetHeight>=this.scrollTarget.scrollHeight)},_ensureTarget:function(){this.dialogElement=this.dialogElement||this.parentElement,this.dialogElement&&this.dialogElement.behaviors&&this.dialogElement.behaviors.indexOf(n.b)>=0?(this.dialogElement.sizingTarget=this.scrollTarget,this.scrollTarget.classList.remove("fit")):this.dialogElement&&this.scrollTarget.classList.add("fit")}})},721:function(t,i,o){"use strict";o.r(i),o.d(i,"DialogManageCloudhook",function(){return s});var n=o(0),e=(o(85),o(93),o(209),o(197),o(56));const a="Public URL – Click to copy to clipboard";class s extends n.a{static get properties(){return{_params:{}}}async showDialog(t){this._params=t,await this.updateComplete,this._dialog.open()}render(){if(!this._params)return n.f``;const{webhook:t,cloudhook:i}=this._params,o="automation"===t.domain?"https://www.home-assistant.io/docs/automation/trigger/#webhook-trigger":`https://www.home-assistant.io/integrations/${t.domain}/`;return n.f`
      <ha-paper-dialog with-backdrop>
        <h2>
          ${this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.webhook_for","name",t.name)}
        </h2>
        <div>
          <p>
            ${this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.available_at")}
          </p>
          <paper-input
            label="${a}"
            value="${i.cloudhook_url}"
            @click="${this._copyClipboard}"
            @blur="${this._restoreLabel}"
          ></paper-input>
          <p>
            ${i.managed?n.f`
                  ${this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.managed_by_integration")}
                `:n.f`
                  ${this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.info_disable_webhook")}
                  <button class="link" @click="${this._disableWebhook}">
                    ${this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.link_disable_webhook")}</button
                  >.
                `}
          </p>
        </div>

        <div class="paper-dialog-buttons">
          <a href="${o}" target="_blank">
            <mwc-button
              >${this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.view_documentation")}</mwc-button
            >
          </a>
          <mwc-button @click="${this._closeDialog}"
            >${this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.close")}</mwc-button
          >
        </div>
      </ha-paper-dialog>
    `}get _dialog(){return this.shadowRoot.querySelector("ha-paper-dialog")}get _paperInput(){return this.shadowRoot.querySelector("paper-input")}_closeDialog(){this._dialog.close()}async _disableWebhook(){confirm(this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.confirm_disable"))&&(this._params.disableHook(),this._closeDialog())}_copyClipboard(t){const i=t.currentTarget,o=i.inputElement.inputElement;o.setSelectionRange(0,o.value.length);try{document.execCommand("copy"),i.label=this.hass.localize("ui.panel.config.cloud.dialog_cloudhook.copied_to_clipboard")}catch(n){}}_restoreLabel(){this._paperInput.label=a}static get styles(){return[e.a,n.c`
        ha-paper-dialog {
          width: 650px;
        }
        paper-input {
          margin-top: -8px;
        }
        button.link {
          color: var(--primary-color);
        }
        .paper-dialog-buttons a {
          text-decoration: none;
        }
      `]}}customElements.define("dialog-manage-cloudhook",s)}}]);
//# sourceMappingURL=chunk.ee6a05dd100d8d5f6a13.js.map