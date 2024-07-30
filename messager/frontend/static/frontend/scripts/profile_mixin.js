const profile_mixin = {
    methods: {
        getProfile: function() {
            axios.get("/api/profile/")
            .then(resp => {
                this.user = resp.data.user
                this.profile = resp.data
                this.avatar = resp.data.avatar
            })

        },
        changeProfile: function() {
            let data = {
                name: this.profile.name,
                age: this.profile.age,
                bio: this.profile.bio,
            }
            axios.post("/api/profile/", JSON.stringify({...data}))
            .then(resp => {
                if (resp.status == 200) {
                    let event = new Event("change-profile-ok", {
                        bubbles: true,
                    })
                    document.dispatchEvent(event)
                    this.errors = null
                    this.getProfile()
                }
            }).catch(err => {
                let err_data = err.response.data.errors
                this.errors = ""
                for (let key in err_data) {
                    this.errors += `${key}: ${err_data[key]}`
                }
            })
        },
        changeAvatar: function() {
            let form = document.querySelector("#form-avatar")
            let formData = new FormData(form);
            // axios.defaults.headers.common['X-CSRFToken'] = this.getCookie('csrftoken');
            // axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';
            axios.post("/api/change-avatar/", formData, {
                "headers": {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": this.getCookie('csrftoken'),
                }
            }).then(resp => {
                this.getProfile()
            }).catch(err => {

            })

        },

        
    },
    data() {
        return {
            user: {},
            profile: {},
            avatar: {},
            name: null,
            age: null,
            bio: null,
            errors: null,
            avatar_form: null,
        }
    },
    mounted() {
        this.getProfile()
    }
}

export {profile_mixin}