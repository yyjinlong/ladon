<template>
  <div>
    <Row class="expand-row">
        <Col span="12">
            <span class="expand-key">Name: </span>
            <span class="expand-value">{{ row.name }}</span>
        </Col>
        <Col span="12">
            <span class="expand-key">Age: </span>
            <span class="expand-value">{{ row.age }}</span>
        </Col>
    </Row>
  </div>
</template>

<script>
export default {
  props: {
  	row: Object
  }
}
</script>

<style scoped>
  .expand-row{
  	margin-bottom: 16px;
  }
</style>
