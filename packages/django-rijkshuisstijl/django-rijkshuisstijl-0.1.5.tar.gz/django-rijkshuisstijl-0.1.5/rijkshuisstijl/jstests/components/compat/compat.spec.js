import {assert} from 'chai';
import sinon from 'sinon';
import {Compat} from '../../../js/components/compat/compat';
import {Utils} from '../../utils';

describe('compat/compat.js - Compat', function () {
    before(() => {
        this.Compat = Utils.createTestableClass(Compat);
    });

    afterEach(() => {
        sinon.restore();
    });

    it('should construct', () => {
        sinon.replace(Compat.prototype, 'isDateSupported', () => true);
        let compat = new this.Compat();
        assert(compat);
    });

    it('should call runChecks() when constructor is called', () => {
        sinon.replace(this.Compat.prototype, 'isDateSupported', () => true);
        let compat = new this.Compat();
        sinon.spy(compat, 'runChecks');
        compat.constructor();
        assert.equal(compat.runChecks.callCount, 1);
    });

    it('should return true when isDateSupported is called when date input is supported', () => {
        class HTMLInputElementMock {
            setAttribute(attribute, value) {
                this[attribute] = value;
            }
            set value(value) {
                this._value = value;
            }

            get value() {
                return "";  // When date is supported, value "a" is not valid for date type and rejected as value.
            }
        }
        sinon.replace(document, 'createElement', sinon.fake.returns(new HTMLInputElementMock()));
        let compat = new this.Compat();
        assert.equal(compat.isDateSupported(), true);
    });

    it('should return false when isDateSupported is called when date input is not supported', () => {
        class HTMLInputElementMock {
            setAttribute(attribute, value) {
                this[attribute] = value;
            }
            set value(value) {
                this._value = value;
            }

            get value() {
                return this._value;  // When date is not supported, value "a" is valid for default type (text) and and accepted value.
            }
        }
        sinon.replace(document, 'createElement', sinon.fake.returns(new HTMLInputElementMock()));
        let compat = new this.Compat();
        assert.equal(compat.isDateSupported(), false);
    });

    it('should call addCompat() when date input is not supported', () => {
        sinon.replace(Compat.prototype, 'isDateSupported', () => false);
        let compat = new this.Compat();
        sinon.spy(compat, 'addCompat');
        compat.constructor();
        compat.runChecks();
        assert.equal(compat.addCompat.callCount, 2);
    });

    it('should call addCompat() when date input is not supported', () => {
        sinon.replace(Compat.prototype, 'isDateSupported', () => true);
        let compat = new this.Compat();
        sinon.spy(compat, 'addCompat');
        compat.constructor();
        compat.runChecks();
        assert.equal(compat.addCompat.callCount, 0);
    });

    it('should add compat.js when addCompat() is called', () => {
        sinon.spy(document.body, 'appendChild');
        let compat = new this.Compat();
        compat.addCompat();
        assert.equal(document.body.appendChild.callCount, 1);
        console.log(document.body.appendChild.getCall(0).args[0].src);
        assert.match(document.body.appendChild.getCall(0).args[0].src, /compat.js/);
    });
});
