import BEM from 'bem.js';


/** @const {string} */
export const BLOCK_INPUT = 'input';

/** @const {string} */
export const ELEMENT_FILEPICKER = 'filepicker';

/** @const {NodeList} */
export const INPUT_FILEPICKERS = BEM.getBEMNodes(BLOCK_INPUT, ELEMENT_FILEPICKER);
