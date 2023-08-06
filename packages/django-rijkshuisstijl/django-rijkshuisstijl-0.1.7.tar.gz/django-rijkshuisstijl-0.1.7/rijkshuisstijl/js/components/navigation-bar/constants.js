import BEM from 'bem.js';

/** @const {string} */
export const BLOCK_NAVIGATION_BAR = 'navigation-bar';

/** @const {string} */
export const MODIFIER_STICKY = 'sticky';

/** @const {string} */
export const MODIFIER_STUCK = 'stuck';

/** @const {NodeList} */
export const STICKY_NAVIGATION_BARS = BEM.getBEMNodes(BLOCK_NAVIGATION_BAR, false, MODIFIER_STICKY);
