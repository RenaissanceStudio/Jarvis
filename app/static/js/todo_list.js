Vue.component(
    'page-header',
    {
        template: `
            <div id='menu' style='display: flex; justify-content: space-between; height: 100%; width: 100%'>
                <div id='left-menu'></div>
                <div id='right-menu' style='display: flex; height: 44px; padding: 0 12px;'>
                    <el-tooltip :visible-arrow="true" :popper-options="{'offset': [5, 0]}" content="Logout" placement="bottom" effect="light">
                        <el-button class='right-menu-button' type="primary" @click="logOut()" style="border: none; background-color: transparent">
                            <i class="fi  fi-rr-sign-out"/>
                        </el-button>
                    </el-tooltip>
                </div>
            </div>
        `,
        props: {
            logout_url: {
                type: String
            }
        },
        methods: {
            logOut() {
                let api = '/login/logout';
                location.href = api;
            }
        }
    }
)

let vue = new Vue({
    el: '#page-header',
    data: {},
    methods: {},
    created: function () {
    }
});
