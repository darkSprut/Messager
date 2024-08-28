const chats = {
    methods: {
        sendMessage: function(id) {
            let obj = {
                message: this.message,
                recipient: id,
            }
            axios.post(`/api/messages/`, obj)
            .then(resp => {
                this.message = null
                let recipient = resp.data.recipient
                this.getMessages(recipient)
            })
        },

        getMessages: function(id) {
            axios.get(`/api/messages/?recipient=${id}`)
            .then(resp => {
                this.messages = resp.data.messages
                this.scrollBottom()
            })
        },

        getChats: function() {
            axios.get(`/api/chats/`)
            .then(resp => {
                this.chats = resp.data
                this.total_new_message = 0
                this.totalNewMessage(this.chats)
            })
        },

        scrollBottom: function() {
            setTimeout(() => {
                let message_list = document.querySelector(this.messages_list_selector)
                message_list.scrollTop = message_list.scrollHeight;
            }, 500)
        },

        totalNewMessage: function(chats) {
            for (let i = 0; chats.length > i; i += 1) {
                this.total_new_message += chats[i].new_message_count
            }
        },

        chatsUpdate: function() {
            setInterval(() => {
                this.getChats()
            }, this.chat_update_interval_ms);
        },
    },

    data() {
        return {
            message: null,
            messages: [],
            messages_list_selector: "#message-list",
            chats: [
                {
                    created_at: null,
                    users: [
                        {
                            profile: {
                                avatar: {

                                },
                            },
                        },
                    ]
                },
            ],
            total_new_message: 0,
            chat_update_interval_ms: 5000,
        }
    },
    mounted() {
        this.defaulSettingsAxios()
        this.getChats()
        this.chatsUpdate()
    }
}

export {chats}