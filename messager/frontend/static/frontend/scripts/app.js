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

                this.rememberSection(elem.id)
                this.getMessages()
                this.updateCurrentChat(elem.id)
            },

            rememberSection: function(elem_id) {
                document.cookie = `current_section_id=${elem_id}`
            },

            currentSection: function() {

                /* функция, которая отображает последнюю просмотренную секцию перед обновлением страницы */
                
                let current_section_str = this.getCookie('current_section_id')
                if (current_section_str) {
                    this.addShowClass(`#${current_section_str}`)
                }
            },

            updateCurrentChat: function(elem_id) {

                /* если текущая секция это чат с пользователем, обновлять его */

                if (elem_id == this.chat_section) {
                    this.update_chat_interval_id = setInterval(
                        this.getMessages
                    , 4000)
                } else {
                    clearInterval(this.update_chat_interval_id)
                }
            }

        },

        data() {
            return {
                /* имя класса, при добавлении которого отображается вабранная секция */
                show_section_class: "section--show",
                /* имя класса всех секций */
                section_class: "section",
                /* id секции с текущем чатом и сообщениями в нём */
                chat_section: "send-message",
                /* id планировщика обновления чата */
                update_chat_interval_id: null,
            }
        },

        mounted() {
            this.defaulSettingsAxios()
            this.currentSection()
        },
    }
).mount('#body');