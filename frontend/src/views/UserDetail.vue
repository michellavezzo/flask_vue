<template>
    <v-container>
        <v-card v-if="user">
            <v-card-title>User Details</v-card-title>
            <v-card-text>
                <p><strong>Username:</strong> {{ user.username }}</p>
                <p><strong>Roles:</strong> {{ user.roles.join(", ") }}</p>
                <p>
                    <strong>Timezone:</strong> {{ user.preferences.timezone }}
                </p>
                <p><strong>Active:</strong> {{ user.active ? "Yes" : "No" }}</p>
                <p>
                    <strong>Created At:</strong>
                    {{ new Date(user.created_ts * 1000).toLocaleString() }}
                </p>
            </v-card-text>
            <v-card-actions>
                <v-btn color="red" @click="deleteUser">Delete</v-btn>
                <v-btn color="blue" @click="openDialog">Edit User</v-btn>
            </v-card-actions>
        </v-card>
    </v-container>

    <UserDialog v-model="dialog" :user="user" @save="fetchUser" />
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import { User } from "@/types/userTypes";
import UserDialog from "@/components/UserDialog.vue";

const store = useStore();
const route = useRoute();
const router = useRouter();

const dialog = ref(false);

const user = computed(() =>
    store.getters["user/getUserByUsername"](route.params.username as string)
);

const fetchUser = async () => {
    if (!user.value) {
        await store.dispatch("user/fetchUsers");
    }
};

const deleteUser = async () => {
    if (confirm("Are you sure?")) {
        await store.dispatch("user/deleteUser", route.params.username);
        router.push("/");
    }
};

const openDialog = () => {
    dialog.value = true;
};

onMounted(fetchUser);
</script>
