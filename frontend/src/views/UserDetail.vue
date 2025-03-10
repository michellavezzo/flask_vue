<template>
    <v-container>
        <v-card v-if="user" :key="user.last_updated_at">
            <v-card-title>User Details</v-card-title>
            <v-card-text>
                <div class="user-details">
                    <p><strong>Username:</strong> {{ user.username }}</p>
                    <p>
                        <strong>Roles:</strong>
                        <v-chip
                            v-for="role in user.roles"
                            :key="role"
                            variant="text"
                            :color="
                                chipRoles(user.roles).find(
                                    (r) => r.text === role
                                )?.color
                            "
                        >
                            <b class="chip-role">{{ role }}</b>
                        </v-chip>
                    </p>
                    <p :key="user.preferences.timezone">
                        <strong>Timezone:</strong>
                        {{ user.preferences.timezone }}
                    </p>
                    <p>
                        <strong>Active:</strong>
                        {{ user.active ? "Yes" : "No" }}
                        <v-icon
                            size="small"
                            :color="user.active ? 'green' : 'red'"
                            >{{
                                user.active ? "mdi-check" : "mdi-close"
                            }}</v-icon
                        >
                    </p>
                    <p>
                        <strong>Created At:</strong>
                        {{ new Date(user.created_ts * 1000).toLocaleString() }}
                    </p>
                    <p v-if="user.last_updated_at">
                        <strong>Last Update:</strong>
                        {{
                            new Date(
                                user.last_updated_at * 1000
                            ).toLocaleString()
                        }}
                    </p>
                </div>
            </v-card-text>
            <v-card-actions class="footer-actions">
                <div>
                    <v-btn
                        color="primary"
                        :aria-label="`Click to go back to users list`"
                        :title="`Click to go back to users list`"
                        @click="router.push('/')"
                        >Back</v-btn
                    >
                </div>
                <div class="d-flex justify-end">
                    <v-btn
                        color="red"
                        :aria-label="`Click to delete ${user.username}`"
                        :title="`Click to delete ${user.username}`"
                        @click="deleteUser"
                        >Delete</v-btn
                    >
                    <v-btn
                        color="blue"
                        :aria-label="`Click to edit ${user.username}`"
                        :title="`Click to edit ${user.username}`"
                        @click="openDialog"
                        >Edit User</v-btn
                    >
                </div>
            </v-card-actions>
        </v-card>
    </v-container>

    <UserDialog v-model="dialog" v-if="dialog" :user="user" @save="fetchUser" />
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

// should be moved to a utility file as is used in multiple components

const chipRoles = (roles: string[]) => {
    return roles.map((role) => ({
        text: role,
        color: role === "admin" ? "red" : role === "manager" ? "green" : "blue",
    }));
};

const openDialog = () => {
    dialog.value = true;
};

onMounted(fetchUser);
</script>

<style scoped>
.user-details {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}

.footer-actions {
    display: flex;
    justify-content: space-between;
}
</style>
