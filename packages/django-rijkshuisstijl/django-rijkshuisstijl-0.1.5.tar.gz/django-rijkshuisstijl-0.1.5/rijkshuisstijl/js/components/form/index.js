//jshint ignore:start
import {INPUT_FILEPICKERS} from './constants';

// Start!
if (INPUT_FILEPICKERS.length) {
    import(/* webpackChunkName: 'input-filepicker' */ './input-filepicker');
}
