const users_mixin = {
    methods: {
        getUsers: function() {
            axios.get("/api/get-users/")
            .then(resp => {
                this.users = resp.data
                this.users_filled = true
            })
        },

        searchUsername: function() {
            let username_input = document.querySelector(`${this.input_username_search}`)
            username_input.addEventListener('keyup', (event) => {
                axios.get(`/api/get-users/?username=${this.username}`)
                .then(resp => {
                    this.users = resp.data
                    this.users_filled = true
                })
            }) 
        },
    },

    data() {
        return {
            users:[{
                profile: {
                    avatar: {

                    }
                }
            }],
            users_filled: false,
            username: null,
            input_username_search: "#search-username-input",
        }
    },
    mounted() {
        this.searchUsername()
    }
}

export {users_mixin}