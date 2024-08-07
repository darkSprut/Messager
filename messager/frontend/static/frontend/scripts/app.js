import { profile_mixin } from "./profile_mixin.js";
import { users_mixin } from "./users_mixin.js";
import { chats } from "./chats.js";

const x = Vue.createApp(
    {
        delimiters: ['${', '}$'],
        mixins: [profile_mixin, users_mixin, chats],
        methods: {
            defaulSettingsAxios: function() {
                axios.defaults.headers.common['X-CSRFToken'] = this.getCookie('csrftoken');
                axios.defaults.headers.post['Content-Type'] = 'application/json;charset=utf-8';
                axios.defaults.headers.put['Content-Type'] = 'application/json;charset=utf-8';
            },
            getCookie: function(key_cookie) {
                let cookies_data = {};
                let re = new RegExp('(?<key>.*)=(?<val>.*)')
                let cookies = document.cookie.split('; ');
    
                for (let i = 0; i < cookies.length; i++) {
    
                    let elem = cookies[i];
                    let result = elem.match(re);
                    cookies_data[result.groups.key] = result.groups.val;
                }
                return cookies_data[key_cookie] ? cookies_data[key_cookie] : null;
            },

            removeShowClass: function() {
                let sections = document.querySelectorAll(this.section_class);
                sections.forEach(element => {
                    element.classList.remove(this.show_section_class)
                });
            },

            addShowClass: function(elem_str) {
                this.removeShowClass()
                let elem = document.querySelector(elem_str)
                elem.classList.add(this.show_section_class)
            }

        },

        data() {
            return {
                show_section_class: "section--show",
                section_class: "section",
            }
        },

        mounted() {
            this.defaulSettingsAxios()
        },
    }
).mount('#body');