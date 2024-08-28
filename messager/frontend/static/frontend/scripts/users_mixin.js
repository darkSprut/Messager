const users_mixin = {
    methods: {
        getUsers: function(id) {
            if (!id) {
                axios.get("/api/get-users/")
                .then(resp => {
                    this.users = resp.data
                    this.users_filled = true
                })
            } else {
                axios.get(`/api/get-users/${id}`)
                .then(resp => {
                    this.one_user = resp.data
                    this.one_user_filled = true
                    document.cookie = `id_one_user=${this.one_user.pk}`
                })
            }
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
            one_user: {
                profile: {
                    avatar: {

                    },
                },
            },
            users_filled: false,
            one_user_filled: false,
            username: null,
            input_username_search: "#search-username-input",
        }
    },
    mounted() {
        this.defaulSettingsAxios()
        this.searchUsername()
    }
}

export {users_mixin}