<template>
    <v-container>
        <div class="list-header">
            <!-- TODO: Input + Onchange search filter (on frontend) + debounce 500ms -->
            <v-btn color="primary" class="mb-4" @click="openDialog()">
                Create User
            </v-btn>
        </div>
        <v-data-table
            :headers="[
                { title: 'Username', key: 'username' },
                { title: 'Roles', key: 'roles' },
                { title: 'Timezone', key: 'preferences.timezone' },
                { title: 'Active', key: 'active' },
                { title: 'Created At', key: 'created_ts' },
                { title: 'Last Update', key: 'last_updated_at' },
                { title: 'Actions', key: 'actions', sortable: false },
            ]"
            :items="users"
        >
            <template v-slot:[`item.username`]="{ item }">
                <router-link :to="`/users/${(item as User).username}`">
                    <b>{{ (item as User).username }}</b>
                </router-link>
            </template>

            <template v-slot:[`item.roles`]="{ item }">
                <v-chip
                    v-for="role in (item as User).roles"
                    :key="role"
                    variant="text"
                    :color="chipRoles((item as User).roles).find((r) => r.text === role)?.color"
                >
                    <b class="chip-role">{{ role }}</b>
                </v-chip>
            </template>

            <template v-slot:[`item.created_ts`]="{ item }">
                {{ formatTimestamp((item as User).created_ts) }}
            </template>

            <template v-slot:[`item.last_updated_at`]="{ item }">
                {{
                    (item as User)?.last_updated_at !== undefined
                        ? formatTimestamp((item as User).last_updated_at!)
                        : ""
                }}
            </template>

            <template v-slot:[`item.active`]="{ item }">
                <v-icon :color="(item as User).active ? 'green' : 'red'">{{
                    (item as User).active ? "mdi-check" : "mdi-close"
                }}</v-icon>
            </template>

            <template v-slot:[`item.actions`]="{ item }">
                <v-btn
                    variant="plain"
                    aria-label="Edit this user"
                    color="blue"
                    icon="mdi-pencil"
                    @click="openDialog(item as User)"
                ></v-btn>
                <v-btn
                    variant="plain"
                    aria-label="Delete this user"
                    color="red"
                    icon="mdi-delete"
                    @click="deleteUser((item as User).username)"
                ></v-btn>
            </template>
        </v-data-table>
    </v-container>

    <UserDialog v-model="dialog" :user="selectedUser" @save="fetchUsers" />
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { useStore } from "vuex";
import { User } from "@/types/userTypes";
import { useRouter } from "vue-router";
import UserDialog from "@/components/UserDialog.vue";
import { format } from "date-fns";
import { toZonedTime } from "date-fns-tz";

const store = useStore();
const router = useRouter();

const users = computed(() => store.getters["user/getUsers"]);

const chipRoles = (roles: string[]) => {
    return roles.map((role) => ({
        text: role,
        color: role === "admin" ? "red" : role === "manager" ? "green" : "blue",
    }));
};

const dialog = ref(false);
const selectedUser = ref<User | undefined>(undefined);
const clientTimezone = ref(Intl.DateTimeFormat().resolvedOptions().timeZone);

const fetchUsers = async () => {
    console.log("aaaab");
    await store.dispatch("user/fetchUsers");
};

onMounted(fetchUsers);

const editUser = (username: string) => {
    router.push(`/users/${username}`);
};

const deleteUser = async (username: string) => {
    if (confirm("Are you sure?")) {
        await store.dispatch("user/deleteUser", username);
    }
};

const openDialog = (user?: User) => {
    selectedUser.value = user || undefined;
    dialog.value = true;
};

const formatTimestamp = (timestamp: number) => {
    const date = toZonedTime(new Date(timestamp * 1000), clientTimezone.value);
    return format(date, "EE, d/MM/yyyy | HH:mm:ss | 'GMT'XXX");
};
</script>

<style scoped>
.list-header {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}
.chip-role {
    text-transform: capitalize;
}
</style>
