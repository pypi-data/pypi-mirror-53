/**
 * Adds "/static/js/compat.js" to DOM if browser fails checks.
 * @class
 */
export class Compat {
    /**
     * Constructor method.
     */
    constructor() {
        this.checks = [this.isDateSupported];
        this.runChecks();
    }

    /**
     * Calls this.addCompat() if any of this.checks fails.
     */
    runChecks() {
        if (!this.checks.every(fn => fn())) {
            this.addCompat();
        }
    }

    /**
     * Returns whether date inputs are supported by the browser.
     * @return {boolean}
     */
    isDateSupported() {
        let input = document.createElement('input');
        let value = 'a';
        input.setAttribute('type', 'date');
        input.setAttribute('value', value);
        return (input.value !== value);
    }

    /**
     * Adds "/static/js/compat.js" to DOM.
     */
    addCompat() {
        let script = document.createElement('script');
        let publicPath = __webpack_public_path__ || '/static/js/';  // jshint ignore:line
        script.src = publicPath + 'compat.js';
        document.body.appendChild(script);
    }
}

new Compat();
