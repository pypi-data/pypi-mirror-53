import {LINK_SELECTS} from './constants';

/**
 * Navigates to selected value of select on change.
 * @class
 */
export class LinkSelect {
    /**
     * Constructor method.
     * @param {HTMLElement} node
     */
    constructor(node) {
        /** {HTMLElement} */
        this.node = node;
        this.bindEvents();
    }

    /**
     * Binds events to callbacks.
     */
    bindEvents() {
        this.node.addEventListener('change', () => {
            location.href = this.node.value || this.node.dataset.value;
        });
    }
}


// Start!
[...LINK_SELECTS].forEach(node => new LinkSelect(node));
