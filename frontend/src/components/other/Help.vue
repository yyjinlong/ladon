<template>
  <div>
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
