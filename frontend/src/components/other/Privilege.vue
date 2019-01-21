<template>
<div>
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
