//jshint ignore:start
import {FORM_CONTROLS, INPUT_FILEPICKERS, LINK_SELECTS} from './constants';

// Start!
if (FORM_CONTROLS.length) {
    import(/* webpackChunkName: 'form-control' */ './form-control');
}

if (INPUT_FILEPICKERS.length) {
    import(/* webpackChunkName: 'input-filepicker' */ './input-filepicker');
}

if (LINK_SELECTS.length) {
    import(/* webpackChunkName: 'link-select' */ './link-select');
}
