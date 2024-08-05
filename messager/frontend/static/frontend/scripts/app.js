import { profile_mixin } from "./profile_mixin.js";
import { users_mixin } from "./users_mixin.js";

const x = Vue.createApp(
    {
        delimiters: ['${', '}$'],
        mixins: [profile_mixin, users_mixin],
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

        },

        data() {
            return {
                // username: "main app",
            }
        },

        mounted() {
            this.defaulSettingsAxios()
        },
    }
).mount('#body');