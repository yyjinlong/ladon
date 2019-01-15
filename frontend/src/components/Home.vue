<template>
  <div class="layout">
    <Layout>
      <Header :style="{position: 'fixed', width: '100%', 'z-index': '100'}">
        <Menu mode="horizontal" theme="dark" active-name="1" @on-select="jump">
          <div class="layout-logo"></div>
          <div class="layout-nav">
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
      <Content :style="{padding: '66px 0 1px', background: '#fff', minHeight: '500px'}">
        <transition mode="out-in">
          <router-view></router-view>
        </transition>
      </Content>
      <Footer class="layout-footer-center" :style="{'z-index': 100}">Copyright &copy; 2019-{{ end_time() }} 服务树</Footer>
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
    border: 1px solid #d7dde4;
    background: #f5f7f9;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
}
.layout-logo{
    width: 100px;
    height: 30px;
    background: #5b6270;
    border-radius: 3px;
    float: left;
    position: relative;
    top: 15px;
    left: 20px;
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
    padding: 0 50px;
    height: 52px;
    line-height: 52px;
}
.ivu-menu-horizontal {
    height: 52px;
    line-height: 52px;
}
</style>
