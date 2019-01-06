<template>
  <div style="padding: 10px;">
    <Breadcrumb :style="{margin: '20px 0'}">
      <BreadcrumbItem to="/">服务树</BreadcrumbItem>
      <BreadcrumbItem>Admin</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <p>{{ msg }}</p>
    </Card>
  </div>
</template>

<script>
  export default {
    name: 'Help',
    data() {
      return {
        msg: '定义一些接口wiki文档.'
      }
    },
    mounted() {
    }
  }
</script>

<style scoped>
.ivu-card-body {
  padding: 16px;
}
</style>
