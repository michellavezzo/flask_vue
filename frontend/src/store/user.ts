import { Module } from "vuex";
import axios from "axios";
import { User } from "@/types/userTypes";

interface UserState {
    users: User[];
}

const userModule: Module<UserState, any> = {
    namespaced: true, // Ensures module scoping
    state: {
        users: [],
    },
    mutations: {
        SET_USERS(state, users: User[]) {
            state.users = users;
        },
        ADD_USER(state, user: User) {
            state.users.push(user);
        },
        UPDATE_USER(state, updatedUser: User) {
            const index = state.users.findIndex(
                (u) => u.username === updatedUser.username
            );
            if (index !== -1) {
                state.users[index] = updatedUser;
            }
        },
        DELETE_USER(state, username: string) {
            state.users = state.users.filter(
                (user) => user.username !== username
            );
        },
    },
    actions: {
        async fetchUsers({ commit }) {
            try {
                const response = await axios.get("http://127.0.0.1:5000/users");
                commit("SET_USERS", response.data);
            } catch (error) {
                window.alert(`Error fetching users: ${error}`);
                console.log(error);
                // throw error;
            }
        },
        async addUser({ commit }, user: User) {
            try {
                const response = await axios.post(
                    "http://127.0.0.1:5000/users",
                    user
                );
                commit("ADD_USER", response.data);
            } catch (error) {
                // window.alert(`Error adding user, ${error}`);
                console.log(error);
                throw error;
            }
        },
        async updateUser({ commit }, user: User) {
            try {
                await axios.put(
                    `http://127.0.0.1:5000/users/${user.username}`,
                    user
                );
                commit("UPDATE_USER", user);
            } catch (error) {
                // window.alert(`Error updating user, ${error}`);
                console.log(error);
                throw error;
            }
        },
        async deleteUser({ commit }, username: string) {
            try {
                await axios.delete(`http://127.0.0.1:5000/users/${username}`);
                commit("DELETE_USER", username);
            } catch (error) {
                // window.alert(`Error deleting user, ${error}`);
                console.log(error);
                throw error;
            }
        },
    },
    getters: {
        getUsers: (state) => state.users,
        getUserByUsername: (state) => (username: string) =>
            state.users.find((user) => user.username === username),
    },
};

export default userModule;
