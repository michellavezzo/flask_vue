<template>
    <v-dialog v-model="dialog" max-width="500px">
        <v-card>
            <v-card-title>
                {{ isEditMode ? "Edit User" : "Create User" }}
            </v-card-title>
            <v-card-text>
                <v-form ref="form" v-model="valid">
                    <v-text-field
                        v-model="localUser.username"
                        label="Username"
                        :rules="[rules.required]"
                        :required="!isEditMode"
                        :disabled="isEditMode"
                    ></v-text-field>
                    <v-text-field
                        v-model="localUser.password"
                        label="Password"
                        type="password"
                        :rules="[rules.requiredOnCreate]"
                        :required="!isEditMode"
                    ></v-text-field>
                    <v-combobox
                        v-model="localUser.roles"
                        label="Roles"
                        multiple
                        :items="['admin', 'manager', 'tester']"
                        :rules="[rules.required, rules.roles]"
                    ></v-combobox>
                    <v-select
                        v-model="localUser.preferences.timezone"
                        :items="timezones"
                        label="Timezone"
                        outlined
                        :rules="[rules.required]"
                    ></v-select>
                    <v-switch
                        v-model="localUser.active"
                        label="Active"
                    ></v-switch>
                </v-form>
            </v-card-text>
            <v-card-actions>
                <v-btn color="blue" @click="saveUser">Save</v-btn>
                <v-btn color="grey" @click="closeDialog">Cancel</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script setup lang="ts">
import { defineProps, defineEmits, ref, watch, computed } from "vue";
import { useStore } from "vuex";
import { User } from "@/types/userTypes";
import { SubmitEventPromise } from "vuetify/lib/framework.mjs";

const store = useStore();
const props = defineProps<{ modelValue: boolean; user?: User }>();
const emit = defineEmits(["update:modelValue", "save"]);
const valid = ref(false);
const form = ref<{
    validate: () => Promise<boolean>;
    reset: () => void;
} | null>(null);

const defaultUser = (): User => ({
    username: "",
    password: "",
    roles: [],
    preferences: { timezone: "" },
    active: true,
    created_ts: Date.now() / 1000,
});

const localUser = ref<User>(props.user ? { ...props.user } : defaultUser());
const timezones = ref(Intl.supportedValuesOf("timeZone"));
const isEditMode = computed(() => !!props.user);
const dialog = computed({
    get: () => props.modelValue,
    set: (val: boolean) => emit("update:modelValue", val),
});

watch(
    () => props.user,
    (newVal) => {
        localUser.value = newVal ? { ...newVal } : defaultUser();
    }
);

const rules = {
    required: (value: string | any[]) => !!value || "This field is required",
    roles: (value: string[]) =>
        value.length > 0 || "At least one role must be selected",
    requiredOnCreate: (value: string) =>
        (!isEditMode.value && !!value) ||
        isEditMode.value ||
        "This field is required",
    minLength: (length: number) => (value: string) =>
        (value && value.length >= length) ||
        `Minimum length is ${length} characters`,
};

const saveUser = async (submitEventPromise: SubmitEventPromise) => {
    try {
        if (!form.value) return;
        const isValid = (await form.value.validate()) && valid.value;
        if (!isValid) return;

        if (isEditMode.value) {
            if (confirm("Are you sure?")) {
                await store.dispatch("user/updateUser", localUser.value);
                emit("save");
                closeDialog();
            }
        } else {
            if (confirm("Are you sure?")) {
                await store.dispatch("user/addUser", localUser.value);
                emit("save");
                closeDialog();
            }
        }
    } catch (error) {
        window.alert(error);
        console.error(error);
    }
};

const closeDialog = () => {
    resetForm();
    emit("update:modelValue", false);
};

const resetForm = () => {
    localUser.value = props.user ? { ...props.user } : defaultUser();
    form.value?.reset();
};
</script>
