const profile_mixin = {
    methods: {
        getUser: function() {
            axios.get("/api/get-change-profile/")
            .then(resp => {
                this.user = resp.data
            })

        },
        changeProfile: function() {
            let data = {
                name: this.user.profile.name,
                age: this.user.profile.age,
                bio: this.user.profile.bio,
            }
            axios.put("/api/get-change-profile/", JSON.stringify({...data}))
            .then(resp => {
                if (resp.status == 200) {
                    this.addShowClass(this.profile_section)
                    this.errors = {}
                    this.getUser()
                }
            }).catch(err => {
                this.errors = err.response.data
            })
        },
        changeAvatar: function() {
            let form = document.querySelector("#form-avatar")
            let formData = new FormData(form);
            axios.post("/api/change-avatar/", formData, {
                "headers": {
                    "Content-Type": "multipart/form-data",
                    "X-CSRFToken": this.getCookie('csrftoken'),
                }
            }).then(resp => {
                this.getUser()
            }).catch(err => {
                console.log(err)
            })

        },
    },
    data() {
        return {
            user: {
                profile: {
                    avatar: {

                    },
                    name: null,
                    age: null,
                    bio: null,
                },
            },
            errors: {},
            avatar_form: null,
            profile_section: "#profile-section",
        }
    },
    mounted() {
        this.defaulSettingsAxios()
        this.getUser()
    }
}

export {profile_mixin}