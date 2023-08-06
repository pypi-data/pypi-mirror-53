//jshint ignore:start
import {STICKY_NAVIGATION_BARS} from './constants';

// Start!
if (STICKY_NAVIGATION_BARS.length) {
    import(/* webpackChunkName: 'sticky-navigation-bar' */ './sticky-navigation-bar');
}
