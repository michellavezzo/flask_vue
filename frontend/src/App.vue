<template>
    <nav class="main-nav">
        <div class="nav-wrapper">
            <div class="nav-logo">
                <v-icon color="black">mdi-account</v-icon>
                <span>User Management</span>
            </div>
            <div class="nav-routes">
                <router-link to="/">Home</router-link>
            </div>
        </div>
    </nav>
    <router-view />
</template>

<style lang="scss">
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #344a72;
    background-color: #f3f5f7;
    min-height: 100vh;
}

nav {
    padding: 30px;

    a {
        font-weight: bold;
        color: #344a72;

        &.router-link-exact-active {
            color: #1c57c1;
        }
    }
}

.main-nav {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1.2rem;
    background-color: #fff;
    box-shadow: 0 0px 5px rgba(0, 0, 0, 0.5);
}

.nav-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    flex: 1;

    .nav-logo {
        display: flex;
        align-items: center;
        justify-content: center;

        span {
            color: black;
            font-weight: bold;
            margin-left: 0.5rem;
        }
    }
}

/* 
    Media Queries following the .v-container width, 
    probably I should use a better way to handle this with calc()/margin/etc..., 
    but thats what we have for today ;) 
*/
@media screen and (min-width: 960px) {
    .nav-wrapper {
        max-width: 900px;
    }
}
@media screen and (min-width: 1280px) {
    .nav-wrapper {
        max-width: 1200px;
    }
}
@media screen and (min-width: 1920px) {
    .nav-wrapper {
        max-width: 1800px;
    }
}
@media screen and (min-width: 2560px) {
    .nav-wrapper {
        max-width: 2400px;
    }
}
</style>
