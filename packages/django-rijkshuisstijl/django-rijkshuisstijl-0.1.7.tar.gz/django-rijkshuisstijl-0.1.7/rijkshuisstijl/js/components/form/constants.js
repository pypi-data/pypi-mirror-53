import BEM from 'bem.js';

/** @const {string} Form control block name. */
export const BLOCK_FORM_CONTROL = 'form-control';

/** @const {NodeList} Form controls. */
export const FORM_CONTROLS = BEM.getBEMNodes(BLOCK_FORM_CONTROL);

/** @const {string} Input block name. */
export const BLOCK_INPUT = 'input';

/** @const {string} Filepicker element name. */
export const ELEMENT_FILEPICKER = 'filepicker';

/** @const {NodeList} File pickers. */
export const INPUT_FILEPICKERS = BEM.getBEMNodes(BLOCK_INPUT, ELEMENT_FILEPICKER);

/** {string} Select block name. */
export const BLOCK_SELECT = 'select';

/** {string} Modifier indicating a select should trigger a navigation. */
export const MODIFIER_LINK = 'link';

/** {NodeList} Link selects. */
export const LINK_SELECTS = BEM.getBEMNodes(BLOCK_SELECT, false, MODIFIER_LINK);
