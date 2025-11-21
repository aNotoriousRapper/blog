import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => ({
        username: localStorage.getItem('username') || '',
        user_id: localStorage.getItem('user_id') || -1,
        access_token: null,
    }),
    getters: {
        isLoggedIn: (state) => !!state.username
    },
    actions: {
        login(username, user_id, access_token) {
            // 实际项目中应通过API验证
            this.username = username
            this.user_id = user_id
            this.access_token = access_token
            localStorage.setItem('username', username)
            localStorage.setItem('user_id', user_id)
        },
        setAccessToken(token) {
            this.access_token = token
        },
        logout() {
            this.username = ''
            this.user_id = -1
            this.access_token = null
            localStorage.removeItem('username')
            localStorage.removeItem("user_id")
        }
    }
})
