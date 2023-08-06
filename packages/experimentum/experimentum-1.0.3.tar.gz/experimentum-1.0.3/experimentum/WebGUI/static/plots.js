/**
 * Migration Scripts
 */
import {createElementFromHTML} from './utils.js'

// Default options
const defaultOptions = {
    generateTrigger: '.generate-plots',
    errorClasses: 'red lighten-2',
    successClasses: 'green lighten-2'
}

export default class {
    /**
     * Set options and bind events.
     * @param {String} selector Migration list selector
     * @param {Object} options Configuration
     */
    constructor(selector, options={}) {
        this.el = $(selector);
        this.options = {...defaultOptions, ...options};

        // Bind events
        $('body').on('click', this.options.generateTrigger, this.action.bind(this))
    }

    /**
     * Event action.
     * @param {Event} e
     */
    action(e) {
        const target = e.target.href;

        e.preventDefault();
        e.target.setAttribute('disabled', 'disabled');

        fetch(target, { method: 'GET' })
            .then(response => response.json())
            .then(messages => {
                messages.forEach(msg => {
                    const html = msg['message'].trim().split('\n').join('<br />');
                    const classes = msg['status'] == 'error' ? this.options.errorClasses : this.options.successClasses;

                    this.el.append(
                        `<div class="col s12 m6">
                            <img class="materialboxed responsive-img" src="${msg['file']}">
                        </div>`
                    );

                    M.toast({html, classes});
                });

                // this.update_list();
                e.target.removeAttribute('disabled');
            });
    }

    /**
     * Updates the migration list.
     */
    update_list() {
        fetch(this.options.statusUrl)
            .then(response => response.json())
            .then(migration => {
                this.el.find(':first').replaceWith($(createElementFromHTML(migration)).find(':first'));
            });
    }
}
