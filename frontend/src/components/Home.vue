<template>
  <div class="layout">
    <Layout>
      <Header :style="{position: 'fixed', width: '100%', 'z-index': '100'}">
        <Menu mode="horizontal" theme="dark" active-name="stree" @on-select="jump">
          <div class="layout-logo">
            <img src="../assets/logo.png" style="width: 105px; height: 46px;" />
          </div>
          <div class="layout-nav">
            <MenuItem name="stree">
              <Icon type="md-git-network"></Icon><strong>主页</strong>
            </MenuItem>
            <MenuItem name="privilege">
              <Icon type="md-eye"></Icon><strong>权限</strong>
            </MenuItem>
            <MenuItem name="admin">
              <Icon type="ios-paper"></Icon><strong>管理</strong>
            </MenuItem>
            <MenuItem name="help">
              <Icon type="ios-bulb"></Icon><strong>帮助</strong>
            </MenuItem>
     	  </div>
        </Menu>
      </Header>
      <Content :style="{padding: '66px 0 1px', background: '#fff', minHeight: '650px'}">
        <transition mode="out-in">
          <router-view></router-view>
        </transition>
      </Content>
      <Footer class="layout-footer-center" :style="{'z-index': 100}">
        <div class="footer-top">
          <a href="#">主页</a> |
          <a href="#">权限</a> |
          <a href="#">管理</a>
        </div>
        <div class="footer-copyright">
          Copyright &copy; 平台开发组
        </div>
      </Footer>
    </Layout>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    jump(name) {
      this.$router.replace(name);
    },
    end_time() {
      var cur_date = new Date();
      return cur_date.getFullYear();
    }
  },
  mounted() {
  }
}
</script>
<style scoped>
.layout{
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
}
.layout-logo{
    width: 110px;
    height: 46px;
    /* background: #5b6270; */
    border-radius: 3px;
    float: left;
    position: relative;
    top: 3px;
    left: 10px;
}
.layout-nav{
    width: 420px;
    margin: 0 auto;
    margin-right: 20px;
}
.layout-footer-center{
    text-align: center;
}
.ivu-layout-header {
    background: #515a6e;
    padding: 0 0;
    height: 52px;
    line-height: 52px;
}
.ivu-menu-horizontal {
    height: 52px;
    line-height: 52px;
}
.ivu-layout-footer {
    border-top: 1px solid #d7dde4;
    background: #fff;
    padding: 10px 50px;
    color: #515a6e;
    font-size: 13px;
}
.footer-top {
    height: 22px;
    line-height: 16px;
    overflow: hidden;
    color: #CDCDCD;
}
.footer-copyright {
    color: #666;
}
.footer-top a {
    margin: 0 10px;
    color: #444;
    text-decoration: none;
}
</style>
