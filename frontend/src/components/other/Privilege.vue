<template>
  <div style="padding: 10px;">
    <Breadcrumb :style="{margin: '20px 0'}">
      <BreadcrumbItem to="/">服务树</BreadcrumbItem>
      <BreadcrumbItem>Privilege</BreadcrumbItem>
    </Breadcrumb>
    <Card>
      <p>{{ msg }}</p>
    </Card>
  </div>
</template>

<script>
export default {
  name: 'Admin',
  data() {
    return {
      msg: 'service tree privilege mange config.'
    }
  },
  methods: {
  }
}
</script>

<style scoped>
.ivu-card-body {
  padding: 16px;
}
</style>
