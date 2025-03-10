import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import UserList from "../views/UserList.vue";
import UserDetail from "../views/UserDetail.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "UserList",
        component: UserList,
    },
    {
        path: "/users/:username",
        name: "UserDetail",
        component: UserDetail,
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
