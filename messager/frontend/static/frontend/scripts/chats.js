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

        scrollBottom: function() {
            setTimeout(() => {
                let message_list = document.querySelector(this.messages_list_selector)
                message_list.scrollTop = message_list.scrollHeight;
            }, 500)
        }
    },

    data() {
        return {
            message: null,
            messages: [],
            messages_list_selector: "#message-list",
        }
    },
    mounted() {

    }
}

export {chats}